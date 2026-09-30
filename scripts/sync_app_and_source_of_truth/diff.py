"""Find what changed in the sheet since the last sync, and duplicate rows within a tab.

Used by: the sync_app_and_source_of_truth task only (called from sync.py in this folder).

- diff() compares the freshly fetched sheet with data/sheet_rows.json (the snapshot from
  the previous sync). It reports new, changed and removed rows. Changed rows are listed
  field by field in the PR for manual reconciliation.
- find_duplicates() looks inside each tab for rows that repeat each other.
"""
from __future__ import annotations

from collections import defaultdict

from common import CORE, SCHEMA, card_id


def _fields(row: dict) -> dict:
    """The row's column values without the row number."""
    return {f: row[f] for f in SCHEMA}


def _changes(before: dict, after: dict) -> dict:
    """{field: [before value, after value]} for every column that differs."""
    return {f: [before[f], after[f]] for f in SCHEMA if before[f] != after[f]}


def diff(prev: dict[str, list[dict]], curr: dict[str, list[dict]]) -> dict:
    """Classify rows as new / changed / removed, per tab.

    Because the card id is derived from hanzi + pinyin + english + type, editing one of
    those fields looks like "one row removed, another added". To report it as a change,
    rows are matched in three passes:
      1. same card id               -> changed only if notes / examples / measure_word differ
      2. same hanzi                 -> pinyin, english or type was edited
      3. same row number, >= 2 of the 4 identity fields equal -> the hanzi itself was edited
    Anything still unmatched is new (in curr) or removed (in prev).

    A changed row whose id moved produces an alias old_id -> new_id, so study progress
    can follow it.

    Returns {"new": [...], "changed": [...], "removed": [...], "aliases": {old: new}}.
    """
    out = {"new": [], "changed": [], "removed": [], "aliases": {}}
    for tab in list(dict.fromkeys([*prev, *curr])):  # every tab in either version, order kept
        # reversed() so that for duplicate ids the *first* row in the tab wins.
        prev_rows = {card_id(r): r for r in reversed(prev.get(tab, []))}
        curr_rows = {card_id(r): r for r in reversed(curr.get(tab, []))}

        # Pass 1: same id; only non-identity columns can differ.
        for cid in curr_rows.keys() & prev_rows.keys():
            changes = _changes(prev_rows[cid], curr_rows[cid])
            if changes:
                out["changed"].append({"tab": tab, "row": curr_rows[cid]["row"],
                                       "hanzi": curr_rows[cid]["hanzi"], "id": cid,
                                       "old_id": cid, "changes": changes})

        added = [cid for cid in curr_rows if cid not in prev_rows]
        gone = {cid: prev_rows[cid] for cid in prev_rows if cid not in curr_rows}

        def match(cid, predicate):
            # Pair a new row with the one removed row that satisfies `predicate`. Only an
            # unambiguous (single) match counts; otherwise the rows stay new/removed.
            candidates = [pid for pid, p in gone.items() if predicate(curr_rows[cid], p)]
            if len(candidates) != 1:
                return False
            pid = candidates[0]
            row = curr_rows[cid]
            out["changed"].append({"tab": tab, "row": row["row"], "hanzi": row["hanzi"], "id": cid,
                                   "old_id": pid, "changes": _changes(gone.pop(pid), row)})
            out["aliases"][pid] = cid
            return True

        # Pass 2 (same hanzi), then pass 3 (same row number + mostly the same identity).
        leftovers = [cid for cid in added if not match(cid, lambda c, p: c["hanzi"] == p["hanzi"])]
        leftovers = [cid for cid in leftovers if not match(
            cid, lambda c, p: c["row"] == p["row"] and sum(c[f] == p[f] for f in CORE) >= 2)]
        for cid in leftovers:
            row = curr_rows[cid]
            out["new"].append({"tab": tab, "row": row["row"], "hanzi": row["hanzi"], "id": cid,
                               "fields": _fields(row)})
        for pid, row in gone.items():
            out["removed"].append({"tab": tab, "row": row["row"], "hanzi": row["hanzi"], "id": pid,
                                   "fields": _fields(row)})
    return out


def find_duplicates(tabs: dict[str, list[dict]]) -> dict:
    """Find rows that repeat each other within one tab.

    exact:     same card id and identical in every column, or a leftover partial copy
               (every filled cell matches a fuller row) -> the extra row is proposed for removal
    conflicts: same card id but measure_word / notes / examples differ -> you merge by hand
    similar:   same hanzi but a different id (pinyin/english/type differ). The README says
               hanzi must be unique within a tab, so this is flagged.
    """
    out = {"exact": [], "conflicts": [], "similar": []}
    for tab, rows in tabs.items():
        by_id, by_hanzi = defaultdict(list), defaultdict(list)
        for r in rows:
            by_id[card_id(r)].append(r)
            by_hanzi[r["hanzi"]].append(r)

        # Same id: the first row is kept, and each later row is an exact duplicate or a conflict.
        for cid, group in by_id.items():
            keep = group[0]
            for dup in group[1:]:
                changes = _changes(keep, dup)
                if changes:
                    out["conflicts"].append({"tab": tab, "hanzi": keep["hanzi"], "id": cid,
                                             "rows": [keep["row"], dup["row"]], "changes": changes})
                else:
                    out["exact"].append({"tab": tab, "hanzi": keep["hanzi"], "id": cid,
                                         "keep_row": keep["row"], "dup_row": dup["row"],
                                         "fields": _fields(dup)})

        # Same hanzi, different id.
        for hanzi, group in by_hanzi.items():
            if not hanzi or len({card_id(r) for r in group}) < 2:
                continue
            # A row whose filled cells all agree with a fuller row is a leftover partial copy
            # (e.g. only hanzi + pinyin filled in). That's safe to remove, like an exact duplicate.
            partial = set()
            for r in group:
                filled = [f for f in SCHEMA if r[f]]
                fuller = next((o for o in group if o is not r and o["row"] not in partial
                               and sum(bool(o[f]) for f in SCHEMA) > len(filled)
                               and all(o[f] == r[f] for f in filled)), None)
                if fuller:
                    partial.add(r["row"])
                    out["exact"].append({"tab": tab, "hanzi": hanzi, "id": card_id(r),
                                         "keep_row": fuller["row"], "dup_row": r["row"],
                                         "fields": _fields(r), "partial": True})
            # Whatever isn't a partial copy is a real conflict of meaning: flag it.
            rest = [r for r in group if r["row"] not in partial]
            if len({card_id(r) for r in rest}) > 1:
                out["similar"].append({"tab": tab, "hanzi": hanzi, "rows": [r["row"] for r in rest]})
    return out
