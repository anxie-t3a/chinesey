"""Download the Google Sheet, read its group tabs into rows, and validate each row.

Used by:
  - sync_app_and_source_of_truth (scripts/sync_app_and_source_of_truth/sync.py):
      fetch + read + validate the live sheet
  - build (scripts/global_use/build.py, which publish_changes_to_source_of_truth runs):
      re-validate the committed snapshot before building cards.json, so blocked rows
      stay out of the app at publish time too

A "row" everywhere in the pipeline is a dict:
    {"row": <sheet row number>, "hanzi": ..., "pinyin": ..., ..., "examples": ...}
with every value already normalized to a string (see common.norm).
"""
from __future__ import annotations

import io
import re
import urllib.request

import openpyxl

from common import MEASURE_WORD_RE, REQUIRED, SCHEMA, TYPES, norm, parse_examples

# Exporting the whole workbook as xlsx gets every tab in one request, so new tabs
# are picked up automatically. Works without credentials because the sheet is link-shared.
EXPORT_URL = "https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"


def fetch_xlsx(sheet_id: str) -> bytes:
    """Download the sheet as an .xlsx file and return its bytes.

    Raises RuntimeError when Google returns something other than an xlsx file (usually a
    sign-in page, meaning the sheet isn't shared as "anyone with the link can view").
    """
    with urllib.request.urlopen(EXPORT_URL.format(sheet_id=sheet_id), timeout=60) as resp:
        data = resp.read()
    # xlsx files are zip archives, and every zip file starts with the bytes "PK".
    if not data.startswith(b"PK"):
        raise RuntimeError(
            "Sheet export did not return an xlsx file. Is the sheet shared as "
            "'anyone with the link can view'?"
        )
    return data


def read_tabs(xlsx: bytes) -> tuple[dict[str, list[dict]], list[str]]:
    """Read every group tab into rows. Returns ({tab name: [row, ...]}, structural_errors).

    - Tabs whose name starts with `_` are metadata (readme, changelog...) and are skipped.
    - A tab whose header doesn't match SCHEMA exactly is a structural error. The caller
      stops the whole run, because we can't trust which column is which.
    - Completely blank rows are dropped; the row number is kept so edits can target it.
    """
    # read_only is faster for big sheets; data_only returns formula results, not formulas.
    wb = openpyxl.load_workbook(io.BytesIO(xlsx), read_only=True, data_only=True)
    tabs: dict[str, list[dict]] = {}
    errors: list[str] = []
    for ws in wb.worksheets:
        if ws.title.startswith("_"):
            continue
        it = ws.iter_rows(values_only=True)
        header = [norm(c) for c in next(it, ())]
        while header and not header[-1]:
            header.pop()  # ignore empty trailing header cells
        if header != SCHEMA:
            errors.append(f"{ws.title}: header must be {SCHEMA}, got {header}")
            continue
        rows = []
        for number, values in enumerate(it, start=2):  # row 1 is the header
            values = list(values) + [None] * len(SCHEMA)  # pad short rows
            if any(norm(v) for v in values[len(SCHEMA):]):
                errors.append(f"{ws.title} row {number}: data outside the {len(SCHEMA)} schema columns")
            cells = [norm(v) for v in values[: len(SCHEMA)]]
            if any(cells):
                rows.append({"row": number, **dict(zip(SCHEMA, cells))})
        tabs[ws.title] = rows
    return tabs, errors


def validate(tabs: dict[str, list[dict]]) -> tuple[list[dict], set[tuple[str, int]]]:
    """Check each row against the schema rules. Returns (issues, blocked).

    issues:  [{"level": "error"|"warning", "tab", "row", "hanzi", "field", "message"}]
    blocked: {(tab, row number)} for rows with at least one error. Blocked rows are left
             out of cards.json and listed in the PR report until they're fixed in the sheet.
    Warnings are reported but don't block anything.
    """
    issues: list[dict] = []
    blocked: set[tuple[str, int]] = set()

    def add(level, tab, row, field, message):
        # Record one issue; an error also blocks the row.
        issues.append({"level": level, "tab": tab, "row": row["row"], "hanzi": row["hanzi"],
                       "field": field, "message": message})
        if level == "error":
            blocked.add((tab, row["row"]))

    for tab, rows in tabs.items():
        for row in rows:
            # --- errors: the row can't be shown correctly in the app ---
            for field in REQUIRED:
                if not row[field]:
                    add("error", tab, row, field, "required field is empty")
            if row["type"] and row["type"] not in TYPES:
                add("error", tab, row, "type", f"'{row['type']}' is not an allowed type")
            if row["measure_word"] and not MEASURE_WORD_RE.match(row["measure_word"]):
                add("error", tab, row, "measure_word",
                    f"'{row['measure_word']}' should look like '张 (zhāng)'")
            if row["examples"]:
                try:
                    parse_examples(row["examples"])
                except ValueError as e:
                    add("error", tab, row, "examples", str(e))
            # --- warnings: probably a typo, but the row still works ---
            if re.search(r"\d", row["pinyin"]):
                add("warning", tab, row, "pinyin", "contains digits (use tone marks)")
            if re.search(r"[A-Za-z]", row["hanzi"]):
                add("warning", tab, row, "hanzi", "contains Latin letters")
            if row["measure_word"] and row["type"] and row["type"] != "noun":
                add("warning", tab, row, "measure_word", f"measure word on a '{row['type']}'")
    return issues, blocked
