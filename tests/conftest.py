"""pytest setup shared by all tests.

Makes the modules in scripts/global_use, scripts/sync_app_and_source_of_truth and
scripts/publish_changes_to_source_of_truth importable by their plain names (e.g. `import build`), the same way the entry-point scripts import them. Also
provides the `row` fixture for building sheet rows.
"""
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
for folder in ("global_use", "sync_app_and_source_of_truth", "publish_changes_to_source_of_truth"):
    sys.path.insert(0, str(SCRIPTS / folder))

from common import SCHEMA  # noqa: E402


def make_row(n, hanzi, pinyin="", english="", type="noun", measure_word="", notes="", examples=""):
    """A sheet row as the pipeline represents it: row number plus every schema column."""
    values = dict(hanzi=hanzi, pinyin=pinyin, english=english, type=type,
                  measure_word=measure_word, notes=notes, examples=examples)
    return {"row": n, **{f: values[f] for f in SCHEMA}}


@pytest.fixture
def row():
    """Fixture form of make_row, e.g. row(2, "茶", "chá", "tea")."""
    return make_row
