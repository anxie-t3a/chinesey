"""Render the sync results as Markdown for the sync PR.

Used by: the sync_app_and_source_of_truth task (called from sync.py in this folder).
The full report is saved to reports/sync-report.md on the PR branch, and a length-limited
copy becomes the PR description.

Section order follows what needs attention first: blocked rows, changed rows (need
reconciliation), new/removed rows, duplicates, proposed edits, Claude's flags, warnings.
"""
from __future__ import annotations

# GitHub rejects PR bodies over 65,536 characters; stay safely under that.
PR_BODY_LIMIT = 60000


def _cell(value) -> str:
    """Make a value safe inside a Markdown table cell ("·" marks an empty cell)."""
    text = str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")
    return text or "·"


def _table(headers, rows) -> list[str]:
    """A Markdown table as a list of lines."""
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(_cell(c) for c in row) + " |" for row in rows]
    return lines


def _changes(changes: dict) -> str:
    """Show {field: [before, after]} as "**field**: before → after; ..."."""
    return "; ".join(f"**{f}**: {_cell(b)} → {_cell(a)}" for f, (b, a) in changes.items())


def build_report(ctx: dict) -> str:
    """Build the full Markdown report from the results sync.py collected.

    ctx keys: baseline, diff, duplicates, edits, issues, blocked, card_count,
              reviewed_total, reviewed_now, review_note, reviews_for_report
    Sections with nothing to show are left out.
    """
    d, dups, edits = ctx["diff"], ctx["duplicates"], ctx["edits"]
    errors = [i for i in ctx["issues"] if i["level"] == "error"]
    warnings = [i for i in ctx["issues"] if i["level"] == "warning"]
    by_source = lambda s: [e for e in edits if e["source"] == s]  # noqa: E731
    review_edits = by_source("review")
    out = ["## Vocab sync", ""]

    # --- Summary ---
    if ctx["baseline"]:
        out += ["First sync: this run sets the baseline snapshot, so every row counts as existing "
                "(no new/changed/removed list).", ""]
    out += _table(["", "count"], [
        ["cards in app", ctx["card_count"]],
        ["new rows", len(d["new"])],
        ["changed rows (need reconciliation)", len(d["changed"])],
        ["removed rows", len(d["removed"])],
        ["blocked rows (validation errors)", len(ctx["blocked"])],
        ["duplicate rows", f"{len(dups['exact'])} exact, {len(dups['conflicts'])} conflicting, "
                           f"{len(dups['similar'])} same-hanzi"],
        ["proposed sheet edits", sum(e["status"] != "rejected" for e in edits)],
        ["cards reviewed by Claude", f"{ctx['reviewed_total']}/{ctx['card_count']} "
                                     f"({ctx['reviewed_now']} this run)"],
    ])
    if ctx["review_note"]:
        out += ["", f"> **Review:** {ctx['review_note']}"]

    # --- Instructions for the reviewer ---
    out += ["", "### How to use this PR",
            "- **Sheet changes** (new / changed / removed) already happened in the Google Sheet. "
            "If one is wrong, fix it in the sheet; the next sync updates this PR.",
            "- **Proposed sheet edits** are in `data/sheet_edits.json`. To reject one, set its "
            '`"status"` to `"rejected"` (edit the file in this PR). Rejected edits are never proposed again.',
            "- **Merging** writes every remaining `proposed` edit back to the Google Sheet, then deploys the app.",
            "- A card whose hanzi/pinyin/english/type changed gets a new id. The old id is kept as an alias, "
            "so study progress follows it."]

    # --- Rows the app can't use until fixed ---
    if errors:
        out += ["", "### Blocked rows: fix in the sheet", "These rows are left out of the app until fixed.", ""]
        out += _table(["tab", "row", "hanzi", "field", "problem"],
                      [[i.get("tab", ""), i.get("row", ""), i["hanzi"], i["field"], i["message"]] for i in errors])

    # --- What changed in the sheet since the last sync ---
    if d["changed"]:
        out += ["", "### Changed rows: needs reconciliation", ""]
        out += _table(["tab", "row", "hanzi", "changes", "id"],
                      [[c["tab"], c["row"], c["hanzi"], _changes(c["changes"]),
                        "same" if c["id"] == c["old_id"] else f"{c['old_id']} → {c['id']}"]
                       for c in d["changed"]])
    if d["new"]:
        out += ["", "### New rows", ""]
        out += _table(["tab", "row", "hanzi", "pinyin", "english", "type"],
                      [[n["tab"], n["row"], n["hanzi"], n["fields"]["pinyin"], n["fields"]["english"],
                        n["fields"]["type"]] for n in d["new"]])
    if d["removed"]:
        out += ["", "### Removed rows", ""]
        out += _table(["tab", "was row", "hanzi", "english"],
                      [[r["tab"], r["row"], r["hanzi"], r["fields"]["english"]] for r in d["removed"]])

    # --- Duplicates within a tab ---
    if dups["exact"] or dups["conflicts"] or dups["similar"]:
        out += ["", "### Duplicates within a tab", ""]
        rows = [[x["tab"], x["hanzi"], f"{x['keep_row']}, {x['dup_row']}",
                 f"{'partial copy' if x.get('partial') else 'exact'}: row {x['dup_row']} will be removed"]
                for x in dups["exact"]]
        rows += [[x["tab"], x["hanzi"], ", ".join(map(str, x["rows"])),
                  "conflict, merge manually: " + _changes(x["changes"])] for x in dups["conflicts"]]
        rows += [[x["tab"], x["hanzi"], ", ".join(map(str, x["rows"])),
                  "same hanzi, different pinyin/english/type: hanzi must be unique within a tab"]
                 for x in dups["similar"]]
        out += _table(["tab", "hanzi", "rows", "action"], rows)

    # --- Edits that will be written to the sheet on merge ---
    if review_edits or by_source("dedupe"):
        out += ["", "### Proposed sheet edits", ""]
        out += _table(["key", "status", "tab", "row", "hanzi", "field", "before", "after", "conf.", "why"],
                      [[e["key"], e["status"], e["tab"], e["row"], e["hanzi"], e["field"],
                        "" if e["op"] == "clear_row" else e["before"],
                        "(remove row)" if e["op"] == "clear_row" else e["after"],
                        e["confidence"], e["reason"]] for e in edits])

    # --- Claude findings without a concrete fix, and cards still missing an example ---
    flags = [(r["hanzi"], i) for r in ctx["reviews_for_report"] for i in r["issues"] if not i["suggested"]
             or i["field"] == "notes"]
    if flags:
        out += ["", "### Claude flags (no automatic fix)", ""]
        out += _table(["hanzi", "field", "current", "note", "conf."],
                      [[h, i["field"], i["current"], i["reason"], i["confidence"]] for h, i in flags])
    failed = [r for r in ctx["reviews_for_report"] if r.get("example_error")]
    if failed:
        out += ["", "### No valid example sentence yet", ""]
        out += _table(["hanzi", "why"], [[r["hanzi"], r["example_error"]] for r in failed])

    # --- Warnings, collapsed because they're informational ---
    if warnings:
        out += ["", "<details><summary>Warnings (" + str(len(warnings)) + ")</summary>", ""]
        out += _table(["where", "hanzi", "field", "warning"],
                      [[f"{i['tab']} row {i['row']}" if "tab" in i else "cross-tab", i["hanzi"], i["field"],
                        i["message"]] for i in warnings])
        out += ["", "</details>"]
    return "\n".join(out) + "\n"


def pr_body(report: str) -> str:
    """The report, cut at a line boundary if it's too long for a PR description."""
    if len(report) <= PR_BODY_LIMIT:
        return report
    cut = report[:PR_BODY_LIMIT].rsplit("\n", 1)[0]
    return cut + "\n\n…truncated. Full report: `reports/sync-report.md` in this PR.\n"
