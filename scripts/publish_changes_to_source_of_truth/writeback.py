"""PUBLISH_CHANGES_TO_SOURCE_OF_TRUTH task: after a sync PR is merged, write the approved
edits back to the Google Sheet (the source of truth).

When it runs: .github/workflows/publish_changes_to_source_of_truth.yml runs it on every push to main (merging the sync
PR is a push to main), before rebuilding cards.json and deploying the app. With no pending
edits it does nothing.

Run locally (checks the edits against the live sheet without writing anything):
    GOOGLE_SERVICE_ACCOUNT_JSON="$(cat key.json)" \
        poetry run python scripts/publish_changes_to_source_of_truth/writeback.py --sheet-id <ID> --dry-run

Needs GOOGLE_SERVICE_ACCOUNT_JSON: the JSON key of a Google service account that has
Editor access to the sheet (see docs/SETUP.md).

Safety: each edit is checked against the live sheet first. If the target cell no longer
holds the edit's "before" value (someone edited the sheet after the PR was opened), the
edit is skipped and logged as a "conflict" instead of overwriting their change.

Afterwards:
  - processed edits move from data/sheet_edits.json to data/edit_decisions.json
    (applied / rejected / conflict), and rejected ones are never proposed again
  - data/sheet_rows.json (the snapshot) is updated to match the sheet, so the next sync
    doesn't report these edits as changes someone made
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

# Modules shared between tasks live in scripts/global_use/. The scripts are run as plain files
# (not as a package), so add that folder to the import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "global_use"))

from build import ALIASES_FILE, DECISIONS_FILE, EDITS_FILE, SNAPSHOT_FILE  # noqa: E402
from common import SCHEMA, card_id, norm, read_json, write_json  # noqa: E402
from edits import APPLY_STATUSES  # noqa: E402


def locate(values: list[list], edit: dict) -> int | None:
    """Find the sheet row (1-based) an edit should change, or None if it's no longer safe.

    values: every cell of the tab, as returned by gspread's get_all_values()

    The edit's recorded row number is tried first. If rows were inserted or deleted since
    the sync, the tab is searched for the one row that still matches. Zero or several
    matches means the sheet changed underneath us, so the edit becomes a conflict.
    """
    def matches(n):
        # Does sheet row n still look the way the edit expects?
        cells = [norm(c) for c in (values[n - 1] + [""] * len(SCHEMA))[: len(SCHEMA)]] if n <= len(values) else []
        if not cells:
            return False
        row = dict(zip(SCHEMA, cells))
        if edit["op"] == "clear_row":
            return row == edit["before"]  # removing a row: the whole row must be unchanged
        return row["hanzi"] == edit["hanzi"] and row[edit["field"]] == edit["before"]

    if matches(edit["row"]):
        return edit["row"]
    candidates = [n for n in range(2, len(values) + 1) if matches(n)]  # row 1 is the header
    return candidates[0] if len(candidates) == 1 else None


def main(argv=None) -> int:
    """Write pending edits to the sheet and record the outcome. Returns the exit code.

    Exits with 1 when there are edits to write but no credentials. The publish workflow
    then stops before deploying, so the app never gets ahead of the sheet.
    """
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sheet-id", required=True)
    p.add_argument("--dry-run", action="store_true", help="check edits against the sheet but write nothing")
    args = p.parse_args(argv)

    edits = read_json(EDITS_FILE, [])
    pending = [e for e in edits if e["status"] in APPLY_STATUSES]
    rejected = [e for e in edits if e["status"] == "rejected"]
    if not edits:
        print("No sheet edits to write back.")
        return 0

    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    decisions = read_json(DECISIONS_FILE, {})
    for e in rejected:
        decisions[e["key"]] = {"status": "rejected", "at": now, "edit": e}

    applied, conflicts = [], []
    if pending:
        creds = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not creds:
            print("GOOGLE_SERVICE_ACCOUNT_JSON is not set, so approved edits can't be written to the sheet. "
                  "Add the secret and re-run this workflow.", file=sys.stderr)
            return 1
        import gspread  # imported here so the rest of the pipeline doesn't need it

        book = gspread.service_account_from_dict(json.loads(creds)).open_by_key(args.sheet_id)

        # Group by tab: one read and one batched write per tab keeps us well under the
        # Sheets API rate limits.
        by_tab: dict[str, list[dict]] = {}
        for e in pending:
            by_tab.setdefault(e["tab"], []).append(e)
        for tab, tab_edits in by_tab.items():
            ws = book.worksheet(tab)
            values = ws.get_all_values()
            updates = []
            for e in tab_edits:
                row = locate(values, e)
                if row is None:
                    conflicts.append(e)
                    continue
                e = {**e, "row": row}  # the row may have moved
                if e["op"] == "clear_row":
                    # Blank every schema column (A..G). Blank rows are ignored by the pipeline,
                    # and deleting the row would shift the row numbers of the other edits.
                    updates.append({"range": f"A{row}:{chr(64 + len(SCHEMA))}{row}", "values": [[""] * len(SCHEMA)]})
                else:
                    col = chr(65 + SCHEMA.index(e["field"]))  # 0 -> "A", 1 -> "B", ...
                    updates.append({"range": f"{col}{row}", "values": [[e["after"]]]})
                applied.append(e)
            if updates and not args.dry_run:
                # RAW: store text exactly as given (no auto-formatting of numbers or dates).
                ws.batch_update(updates, value_input_option="RAW")

    for e in applied:
        decisions[e["key"]] = {"status": "applied", "at": now, "edit": e}
    for e in conflicts:
        decisions[e["key"]] = {"status": "conflict", "at": now, "edit": e}

    summary = (f"Sheet write-back: {len(applied)} applied, {len(conflicts)} conflicts "
               f"(sheet changed since the PR), {len(rejected)} rejected")
    print(summary)
    for e in conflicts:
        print(f"  conflict: {e['tab']} row {e['row']} {e['hanzi']} {e['field']}", file=sys.stderr)
    if args.dry_run:
        return 0

    # Mirror the applied edits in the snapshot, so it still matches the sheet. Also record
    # aliases for identity changes, so study progress follows the card.
    tabs = read_json(SNAPSHOT_FILE, {})
    aliases = read_json(ALIASES_FILE, {})
    for e in applied:
        rows = tabs.get(e["tab"], [])
        target = next((r for r in rows if r["row"] == e["row"]), None)
        if target is None:
            continue
        if e["op"] == "clear_row":
            rows.remove(target)
        else:
            old = card_id(target)
            target[e["field"]] = e["after"]
            if card_id(target) != old:
                aliases[old] = card_id(target)
    write_json(SNAPSHOT_FILE, tabs)
    write_json(ALIASES_FILE, dict(sorted(aliases.items())))
    write_json(EDITS_FILE, [])  # every edit is now processed; conflicts are re-proposed next sync if still relevant
    write_json(DECISIONS_FILE, decisions)

    # Show the outcome on the workflow run's summary page in GitHub.
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"### {summary}\n")
            for e in conflicts:
                f.write(f"- conflict: {e['tab']} row {e['row']} {e['hanzi']} `{e['field']}`\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
