"""Build data/cards.json (the app's data file) from sheet rows plus any pending edits.

Used by:
  - sync_app_and_source_of_truth (scripts/sync_app_and_source_of_truth/sync.py):
      build_cards() and write_cards() produce the PR's cards.json
  - publish_changes_to_source_of_truth (.github/workflows/publish_changes_to_source_of_truth.yml):
      run as a command after write-back, so what gets deployed matches the committed
      snapshot minus any rejected edits

Run directly to rebuild from the committed files (no network needed):
    poetry run python scripts/global_use/build.py

This module also defines the paths of the committed pipeline-state files in data/.
"""
from __future__ import annotations

import datetime as dt

from common import CORE, DATA, card_id, parse_examples, read_json, write_json
from edits import apply_edits
from sheet import validate

# Committed pipeline state (see README "Sync pipeline").
CARDS_FILE = DATA / "cards.json"                # the app data
SNAPSHOT_FILE = DATA / "sheet_rows.json"        # the sheet as last fetched; baseline for the next diff
EDITS_FILE = DATA / "sheet_edits.json"          # edits pending write-back to the sheet
ALIASES_FILE = DATA / "id_aliases.json"         # old card id -> new card id
DECISIONS_FILE = DATA / "edit_decisions.json"   # history of applied / rejected / conflicting edits


def build_cards(tabs, blocked, aliases) -> tuple[dict, list[dict]]:
    """Merge rows into cards: one card per id, tagged with every tab it appears in.

    tabs:    {tab: [row]}
    blocked: {(tab, row number)} rows to leave out (validation errors)
    aliases: {old id: new id}; each live card gets the old ids that lead to it

    Returns ({"groups": [...], "cards": [...]}, issues). Issues are cross-tab problems such
    as a measure word that differs between tabs.
    """
    cards: dict[str, dict] = {}
    issues: list[dict] = []
    for tab, rows in tabs.items():
        seen = set()
        for row in rows:
            cid = card_id(row)
            if (tab, row["row"]) in blocked or cid in seen:
                continue  # blocked rows and within-tab duplicates are reported elsewhere
            seen.add(cid)
            card = cards.setdefault(cid, {"id": cid, **{f: row[f] for f in CORE},
                                          "measure_word": row["measure_word"], "groups": [],
                                          "notes": [], "examples": [], "aliases": []})
            card["groups"].append(tab)

            # measure_word must agree across tabs: two different values is an error (the
            # first tab wins); filled in one tab but blank in another is only a warning.
            mw = row["measure_word"]
            if mw and card["measure_word"] and mw != card["measure_word"]:
                issues.append({"level": "error", "id": cid, "hanzi": row["hanzi"], "field": "measure_word",
                               "message": f"'{card['measure_word']}' in {card['groups'][0]} but "
                                          f"'{mw}' in {tab}; using the first"})
            elif mw != card["measure_word"]:
                issues.append({"level": "warning", "id": cid, "hanzi": row["hanzi"], "field": "measure_word",
                               "message": f"measure word only filled in some tabs ({card['groups'][0]}, {tab})"})
                card["measure_word"] = card["measure_word"] or mw

            # Notes and examples may differ per tab; keep each distinct one, labelled by tab.
            if row["notes"] and row["notes"] not in [n["text"] for n in card["notes"]]:
                card["notes"].append({"group": tab, "text": row["notes"]})
            for ex in parse_examples(row["examples"]):
                if ex["hanzi"] not in [e["hanzi"] for e in card["examples"]]:
                    card["examples"].append({**ex, "group": tab})

    # Same hanzi but different ids across tabs is often a typo that splits one card in two.
    by_hanzi: dict[str, set[str]] = {}
    for card in cards.values():
        by_hanzi.setdefault(card["hanzi"], set()).add(card["id"])
    for hanzi, ids in by_hanzi.items():
        if len(ids) > 1:
            groups = sorted({g for i in ids for g in cards[i]["groups"]})
            issues.append({"level": "warning", "id": "", "hanzi": hanzi, "field": "hanzi",
                           "message": f"{len(ids)} different cards share this hanzi ({', '.join(groups)}): "
                                      "check for a typo splitting one card in two"})

    # Attach aliases. Follow chains (A -> B -> C) to the id that's live now; `seen` guards
    # against loops if an edit was later reverted.
    for old, new in aliases.items():
        final, seen = new, {old}
        while final in aliases and final not in cards and final not in seen:
            seen.add(final)
            final = aliases[final]
        if final in cards and old not in cards:
            cards[final]["aliases"].append(old)

    return {"groups": list(tabs), "cards": list(cards.values())}, issues


def prune_aliases(aliases: dict, live_ids) -> dict:
    """Drop aliases whose old id is a live card again (e.g. an edit was reverted)."""
    live = set(live_ids)
    return {old: new for old, new in sorted(aliases.items()) if old not in live and old != new}


def write_cards(cards_json: dict) -> bool:
    """Write cards.json. Returns True if the content changed.

    generated_at is only bumped when the content actually changes. Otherwise every run would
    produce a diff, and the sync would open a PR with nothing in it.
    """
    existing = read_json(CARDS_FILE, {})
    if {k: v for k, v in existing.items() if k != "generated_at"} == cards_json:
        return False
    stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    write_json(CARDS_FILE, {"generated_at": stamp, **cards_json})
    return True


def build_from_files() -> dict:
    """Rebuild cards.json from the committed snapshot, pending edits and aliases.

    This is what publish runs after write-back. Rejected edits aren't applied, so the
    deployed app never shows an edit the reviewer turned down.
    """
    tabs = read_json(SNAPSHOT_FILE, None)
    if tabs is None:
        raise SystemExit(f"{SNAPSHOT_FILE} not found: run scripts/sync_app_and_source_of_truth/sync.py first")
    edited, edit_aliases = apply_edits(tabs, read_json(EDITS_FILE, []))
    _, blocked = validate(edited)  # re-check, since edits could in theory fix or break rows
    aliases = {**read_json(ALIASES_FILE, {}), **edit_aliases}
    cards_json, issues = build_cards(edited, blocked, aliases)
    write_cards(cards_json)
    return {"cards": len(cards_json["cards"]), "blocked_rows": len(blocked), "issues": issues}


if __name__ == "__main__":
    result = build_from_files()
    print(f"cards.json: {result['cards']} cards, {result['blocked_rows']} blocked rows")
