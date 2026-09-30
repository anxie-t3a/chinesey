"""Shared constants and small helpers used by every part of the vocab pipeline.

Used by both tasks, sync_app_and_source_of_truth (scripts/sync_app_and_source_of_truth/) and
publish_changes_to_source_of_truth (scripts/publish_changes_to_source_of_truth/), and by the
other global_use modules.
Nothing here talks to the network. It defines:
  - where the pipeline's files live (data/, reports/)
  - the sheet schema (column names, required fields, allowed `type` values)
  - text normalization and the derived card id
  - parsing/formatting of the `examples` column
  - JSON read/write helpers
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths. This file lives at scripts/global_use/common.py, so the repo root is 3 levels up.
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"          # committed pipeline state + cards.json
REPORTS = ROOT / "reports"    # the human-readable sync report shown in the PR

# ---------------------------------------------------------------------------
# Sheet schema. Every group tab must have exactly these columns, in this order.
# ---------------------------------------------------------------------------
SCHEMA = ["hanzi", "pinyin", "english", "type", "measure_word", "notes", "examples"]
REQUIRED = ["hanzi", "pinyin", "english", "type"]
# Fields that make up a card's identity. Changing any of them changes the card id.
CORE = ["hanzi", "pinyin", "english", "type"]
# Allowed values for the `type` column (mirrors the sheet's dropdown).
TYPES = {
    "noun", "verb", "VOV", "adjective", "adverb", "position", "preposition",
    "conjunction", "time", "frequency", "sequence", "measure_word", "phrase",
    "question", "pattern",
}

# Unicode ranges for Chinese characters (CJK Unified Ideographs + extensions + compatibility).
# Python's `re` has no \p{Han}, so we spell the ranges out.
HAN = "㐀-䶿一-鿿豈-﫿\U00020000-\U0002ffff"
HAN_RUN = re.compile(f"[{HAN}]+")                      # a stretch of consecutive Chinese characters
MEASURE_WORD_RE = re.compile(f"^[{HAN}] \\(.+\\)$")     # e.g. "张 (zhāng)"
ALT_SEP = " / "                                         # separates alternatives, e.g. "理发店 / 美发店"

# Curly quotes are normalized to straight ones so "don’t" and "don't" compare equal.
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})


def norm(value) -> str:
    """Turn a raw cell value into a clean string: trimmed, straight quotes, "" for empty.

    Spreadsheet numbers arrive as floats (e.g. 3.0), so whole numbers are printed without ".0".
    """
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).translate(_QUOTES).strip()


def card_id(row: dict) -> str:
    """The card's stable id, derived from hanzi + pinyin + english + type.

    The id is never stored in the sheet (by design, nobody maintains ids by hand). Study
    progress in the app is keyed on it. When one of these fields changes, the pipeline
    records an alias (old id -> new id) so progress follows the card.
    """
    # \x1f (ASCII "unit separator") can't appear in cell text, so field boundaries are unambiguous.
    key = "\x1f".join(row[f] for f in CORE)
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def short_hash(*parts) -> str:
    """A short, deterministic fingerprint of any values (used for edit keys and review hashes)."""
    return hashlib.sha1("\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:12]


def parse_examples(text: str) -> list[dict]:
    """Parse the `examples` column into [{"hanzi", "pinyin", "english"}, ...].

    Format: `hanzi | pinyin | english`, with multiple examples separated by `;`.
    Raises ValueError when an example doesn't have exactly three non-empty parts.
    """
    examples = []
    for chunk in text.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue  # tolerate a trailing ";" or empty cell
        parts = [p.strip() for p in chunk.split("|")]
        if len(parts) != 3 or not all(parts):
            raise ValueError(f"expected 'hanzi | pinyin | english', got {chunk!r}")
        examples.append(dict(zip(["hanzi", "pinyin", "english"], parts)))
    return examples


def format_example(ex: dict) -> str:
    """The inverse of parse_examples for one example: dict -> `hanzi | pinyin | english`."""
    return f"{ex['hanzi']} | {ex['pinyin']} | {ex['english']}"


def read_json(path: Path, default):
    """Load a JSON file, or return `default` if the file doesn't exist yet (e.g. first run)."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def write_json(path: Path, obj) -> None:
    """Write JSON with Chinese characters kept readable (not \\u-escaped), for clean PR diffs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
