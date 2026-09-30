"""SYNC_APP_AND_SOURCE_OF_TRUTH task entry point: pull the Google Sheet (the source of truth),
check it, have Claude review it, and write the app data plus the PR report.

When it runs: daily from .github/workflows/sync_app_and_source_of_truth.yml (6am EDT), or by
hand from the Actions tab. The workflow then commits the results to branch sync/sheet and
opens or updates the sync PR. Nothing reaches the live app or the sheet until that PR is merged.

Claude reviews every card whose content changed since its last review (all of them on the
first run). --review-all makes it review every card in the sheet regardless.

Run locally:
    poetry run python scripts/sync_app_and_source_of_truth/sync.py --sheet-id <ID> --no-review
    poetry run python scripts/sync_app_and_source_of_truth/sync.py --xlsx vocab.xlsx --no-review
(--no-review makes no API calls; --xlsx reads a downloaded file instead of fetching the sheet.)

Steps (folder of the module that does each one):
  1. download + read the sheet     global_use/sheet.py
  2. validate rows                 global_use/sheet.py                  -> blocked rows
  3. diff against last snapshot    sync_app_and_source_of_truth/diff.py   -> new / changed / removed
  4. find duplicates in each tab   sync_app_and_source_of_truth/diff.py
  5. Claude review                 sync_app_and_source_of_truth/review.py -> accuracy, completeness, examples
  6. turn findings into edits      global_use/edits.py
  7. build cards.json              global_use/build.py
  8. write report                  sync_app_and_source_of_truth/report.py

Writes (all under data/ unless noted):
  sheet_rows.json   snapshot of the sheet exactly as fetched (baseline for the next diff)
  reviews.json      Claude review cache, keyed by card id
  sheet_edits.json  edits proposed for the sheet (applied on merge by
                    publish_changes_to_source_of_truth/writeback.py)
  id_aliases.json   old card id -> new card id, so study progress survives identity edits
  cards.json        app data: the sheet with the proposed edits applied
  reports/sync-report.md, and --pr-body if given
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Modules shared between tasks live in scripts/global_use/. The scripts are run as plain files
# (not as a package), so add that folder to the import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "global_use"))

from build import (ALIASES_FILE, DECISIONS_FILE, EDITS_FILE, SNAPSHOT_FILE,  # noqa: E402
                   build_cards, prune_aliases, write_cards)
from common import DATA, REPORTS, read_json, write_json  # noqa: E402
from diff import diff, find_duplicates  # noqa: E402
from edits import apply_edits, derive_edits  # noqa: E402
from report import build_report, pr_body  # noqa: E402
from sheet import fetch_xlsx, read_tabs, validate  # noqa: E402
from vocab import build_lexicon, load_allowed_words  # noqa: E402

REVIEWS_FILE = DATA / "reviews.json"


def main(argv=None) -> int:
    """Run one sync. Returns the process exit code (0 = ok, 1 = the sheet's structure is broken)."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--sheet-id", help="Google Sheet ID to download")
    src.add_argument("--xlsx", type=Path, help="local xlsx export instead of downloading")
    p.add_argument("--carry", type=Path, help="directory with reviews.json / sheet_edits.json from the open sync PR")
    review = p.add_mutually_exclusive_group()
    review.add_argument("--review-all", action="store_true",
                        help="have Claude review every card, not just cards whose content changed")
    review.add_argument("--no-review", action="store_true", help="skip the Claude review")
    p.add_argument("--pr-body", type=Path, help="also write the (length-limited) PR body here")
    args = p.parse_args(argv)

    # 1-2. Read and validate the sheet. A broken header stops everything: we can't tell
    #      which column is which, so writing anything could corrupt the data.
    xlsx = args.xlsx.read_bytes() if args.xlsx else fetch_xlsx(args.sheet_id)
    tabs, structural = read_tabs(xlsx)
    if structural:
        print("Sheet structure is broken; nothing was written:", *structural, sep="\n  ", file=sys.stderr)
        return 1
    issues, blocked = validate(tabs)

    # 3-4. Compare with the previous snapshot (none on the very first run), and find duplicates.
    prev = read_json(SNAPSHOT_FILE, None)
    changes = diff(prev, tabs) if prev is not None else {"new": [], "changed": [], "removed": [], "aliases": {}}
    duplicates = find_duplicates(tabs)
    aliases = {**read_json(ALIASES_FILE, {}), **changes["aliases"]}

    # Cards as they are in the sheet right now (before any proposed edits). These are what
    # Claude reviews.
    cards_json, _ = build_cards(tabs, blocked, aliases)
    cards = cards_json["cards"]

    # 5. Claude review. Start from main's cache, then take anything newer from the open PR's
    #    branch (--carry), so a card isn't reviewed (and paid for) twice.
    carry = args.carry if args.carry and args.carry.is_dir() else None
    reviews = read_json(REVIEWS_FILE, {})
    if carry:
        for cid, rec in read_json(carry / "reviews.json", {}).items():
            if rec.get("reviewed_at", "") >= reviews.get(cid, {}).get("reviewed_at", ""):
                reviews[cid] = rec
    live = {c["id"] for c in cards}
    reviews = {cid: rec for cid, rec in reviews.items() if cid in live}  # forget cards that are gone

    reviewed_now, review_note = 0, ""
    if args.no_review:
        review_note = "skipped (--no-review)."
    elif not os.environ.get("ANTHROPIC_API_KEY"):
        review_note = "skipped: ANTHROPIC_API_KEY is not set."
    else:
        from review import Reviewer, needs_review  # imported here so offline runs don't need the SDK

        # Every card whose content changed since its last review (or every card, with
        # --review-all). There's no per-run cap, so nothing is left waiting for a later run.
        todo = needs_review(cards, reviews, review_all=args.review_all)
        touched = {x["id"] for x in changes["new"] + changes["changed"]}
        todo.sort(key=lambda c: c["id"] not in touched)  # sheet edits first, in case the API stops partway
        allowed = load_allowed_words()
        lexicon = build_lexicon([c["hanzi"] for c in cards], allowed)
        results, review_note = Reviewer(cards, allowed, lexicon).review(todo)
        reviews.update(results)
        reviewed_now = len(results)
        # Cards not reached (API outage) stay unreviewed in the cache, so the next run picks them up.
        if not review_note:
            scope = "all cards (--review-all)" if args.review_all else "cards changed since their last review"
            review_note = f"reviewed {reviewed_now} {scope}." if todo else "no card content changed; nothing to review."

    # 6. Turn dedupe + review findings into proposed sheet edits, keeping the reviewer's
    #    "rejected" choices from the open PR and from past merges.
    decisions = read_json(DECISIONS_FILE, {})
    carried = read_json(carry / "sheet_edits.json", []) if carry else []
    edits = derive_edits(tabs, blocked, duplicates, reviews, decisions, carried)

    # 7. cards.json shows the app as it will look after merge: the sheet with the edits applied.
    edited, edit_aliases = apply_edits(tabs, edits)
    _, edited_blocked = validate(edited)
    final_cards, card_issues = build_cards(edited, edited_blocked, {**aliases, **edit_aliases})

    # Save state. The snapshot is the sheet *as fetched* (without the proposed edits), because
    # it has to mirror the real sheet for the next diff.
    write_json(SNAPSHOT_FILE, tabs)
    write_json(REVIEWS_FILE, dict(sorted(reviews.items())))
    write_json(EDITS_FILE, edits)
    write_json(ALIASES_FILE, prune_aliases(aliases, (c["id"] for c in cards)))
    write_cards(final_cards)

    # 8. Report for the PR.
    report = build_report({
        "baseline": prev is None, "diff": changes, "duplicates": duplicates, "edits": edits,
        "issues": issues + card_issues, "blocked": blocked, "card_count": len(final_cards["cards"]),
        "reviewed_total": len(reviews), "reviewed_now": reviewed_now, "review_note": review_note,
        "reviews_for_report": list(reviews.values()),
    })
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "sync-report.md").write_text(report, encoding="utf-8")
    if args.pr_body:
        args.pr_body.write_text(pr_body(report), encoding="utf-8")

    print(f"{len(final_cards['cards'])} cards | new {len(changes['new'])}, changed {len(changes['changed'])}, "
          f"removed {len(changes['removed'])} | blocked rows {len(blocked)} | edits {len(edits)} | "
          f"reviewed {reviewed_now} this run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
