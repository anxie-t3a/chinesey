"""Proposed edits to the Google Sheet: how they're created, and how they're applied to rows.

Used by:
  - sync_app_and_source_of_truth (scripts/sync_app_and_source_of_truth/sync.py):
      derive_edits() builds the list for the sync PR; apply_edits() previews them in cards.json
  - build (scripts/global_use/build.py): apply_edits() when rebuilding cards.json at publish time
  - publish_changes_to_source_of_truth (scripts/publish_changes_to_source_of_truth/writeback.py):
      APPLY_STATUSES decides which edits get written

Where edits come from:
  - dedupe: an exact duplicate or leftover partial copy of a row within a tab -> remove that row
  - review: Claude's fixes (corrected field, missing measure word) and new example sentences

Lifecycle: an edit starts as "proposed" in data/sheet_edits.json on the sync PR. The reviewer
may change its "status" to "rejected". On merge, writeback.py writes every proposed edit to
the sheet and records the outcome in data/edit_decisions.json. A rejected edit is never
proposed again.

Edit shape:
    {"key", "op": "set"|"clear_row", "tab", "row", "hanzi", "field", "before", "after",
     "source": "review"|"dedupe", "reason", "confidence", "status"}
"""
from __future__ import annotations

import copy

from common import CORE, MEASURE_WORD_RE, SCHEMA, TYPES, card_id, format_example, short_hash

# Statuses that mean "apply this edit". "approved" isn't set by the pipeline; it's accepted
# in case a reviewer wants to mark an edit explicitly.
APPLY_STATUSES = {"proposed", "approved"}
# Columns Claude is allowed to change. Notes are only ever flagged, never rewritten.
EDITABLE = [*CORE, "measure_word"]
# When Claude reports several fixes for the same field, the most confident one wins.
_CONFIDENCE_RANK = {"high": 0, "medium": 1, "low": 2}


def _edit(op, tab, row, field, before, after, source, reason, confidence=""):
    """Create one edit dict targeting `row` in `tab`.

    The key is deterministic (same edit -> same key on every run), which lets a reviewer's
    "rejected" status be matched up again on later runs.
    """
    return {
        # set edits are identified by what they change to; row removals by the row itself.
        "key": short_hash(op, tab, row["hanzi"], field, after if op == "set" else row["row"]),
        "op": op, "tab": tab, "row": row["row"], "hanzi": row["hanzi"], "field": field,
        "before": before, "after": after, "source": source, "reason": reason,
        "confidence": confidence, "status": "proposed",
    }


def suggestion_is_valid(field: str, value: str) -> bool:
    """True if Claude's suggested value obeys the schema (e.g. an allowed type, measure-word format)."""
    if not value:
        return False
    if field == "type":
        return value in TYPES
    if field == "measure_word":
        return bool(MEASURE_WORD_RE.match(value))
    return True


def derive_edits(tabs, blocked, duplicates, reviews, decisions, carried) -> list[dict]:
    """Build the full list of proposed edits from the current sheet state.

    tabs:       {tab: [row]} as read from the sheet
    blocked:    rows with validation errors (not reviewed, so no review edits for them)
    duplicates: output of diff.find_duplicates
    reviews:    {card id: review record} from data/reviews.json
    decisions:  {key: {"status": ...}} history; anything "rejected" is never proposed again
    carried:    edits from the open sync PR, so a reviewer's "rejected" survives re-runs

    The list is rebuilt from scratch every run, so an edit that no longer applies (the sheet
    was fixed by hand, or changed since the review) simply disappears.
    """
    edits: list[dict] = []
    rows_by_tab = {tab: {r["row"]: r for r in rows} for tab, rows in tabs.items()}

    # 1) Dedupe: remove the duplicate row (the first occurrence is kept).
    for dup in duplicates["exact"]:
        row = rows_by_tab[dup["tab"]][dup["dup_row"]]
        before = {f: row[f] for f in SCHEMA}  # the full row, so write-back can verify it before clearing
        kind = "partial copy" if dup.get("partial") else "exact duplicate"
        edits.append(_edit("clear_row", dup["tab"], row, "*", before, None, "dedupe",
                           f"{kind} of row {dup['keep_row']}"))

    # 2) Map each card id to the (tab, row) pairs it appears in. Review edits to identity
    #    fields must be applied to every one of them, or the card would split in two.
    memberships: dict[str, list[tuple[str, dict]]] = {}
    for tab, rows in tabs.items():
        seen = set()
        for r in rows:
            cid = card_id(r)
            if (tab, r["row"]) in blocked or cid in seen:
                continue  # skip blocked rows and within-tab duplicates
            seen.add(cid)
            memberships.setdefault(cid, []).append((tab, r))

    # 3) Review: turn Claude's findings into edits.
    for cid, review in reviews.items():
        members = memberships.get(cid)
        if not members:
            continue  # card no longer exists in the sheet
        first_row = members[0][1]
        issues = sorted(review.get("issues", []),
                        key=lambda i: _CONFIDENCE_RANK.get(i.get("confidence"), 3))
        touched = set()  # fields already given an edit for this card
        for issue in issues:
            field, after = issue["field"], issue.get("suggested", "")
            # Only concrete, schema-valid fixes to editable fields become edits;
            # everything else shows up in the report as a flag.
            if field not in EDITABLE or field in touched or not suggestion_is_valid(field, after):
                continue
            if first_row[field] == after or first_row[field] != issue.get("current", first_row[field]):
                continue  # already fixed, or the sheet changed since the review
            touched.add(field)
            # Identity fields and measure words must stay consistent across tabs,
            # so the edit goes to every row of the card.
            for tab, row in members:
                edits.append(_edit("set", tab, row, field, row[field], after, "review",
                                   issue.get("reason", ""), issue.get("confidence", "")))
        example = review.get("example")
        # Only add an example if the card has none anywhere; it goes on the card's first row.
        if example and not any(r["examples"] for _, r in members):
            tab, row = members[0]
            edits.append(_edit("set", tab, row, "examples", "", format_example(example), "review",
                               "generated example sentence (uses only app vocab + allowed words)"))

    # 4) Drop previously rejected edits, and keep the reviewer's status from the open PR.
    carried_status = {e["key"]: e["status"] for e in carried}
    result = []
    for e in edits:
        if decisions.get(e["key"], {}).get("status") == "rejected":
            continue
        e["status"] = carried_status.get(e["key"], e["status"])
        result.append(e)
    return result


def apply_edits(tabs, edits) -> tuple[dict, dict]:
    """Apply the edits whose status is in APPLY_STATUSES to a copy of the rows.

    Returns (edited tabs, {old card id: new card id}) — the second part covers edits that
    changed a card's identity, so cards.json can carry an alias for study progress.
    The input `tabs` is not modified.
    """
    out = copy.deepcopy(tabs)
    aliases = {}
    index = {(tab, r["row"]): r for tab, rows in out.items() for r in rows}
    cleared = set()
    for e in edits:
        if e["status"] not in APPLY_STATUSES:
            continue
        row = index.get((e["tab"], e["row"]))
        if row is None:
            continue  # row no longer exists
        if e["op"] == "clear_row":
            cleared.add((e["tab"], e["row"]))
        elif e["op"] == "set":
            old = card_id(row)
            row[e["field"]] = e["after"]
            if card_id(row) != old:
                aliases[old] = card_id(row)
    for tab in out:
        out[tab] = [r for r in out[tab] if (tab, r["row"]) not in cleared]
    return out, aliases
