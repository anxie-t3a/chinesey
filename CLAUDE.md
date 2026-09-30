# Chinese Vocab Flashcards

A static flashcard web app built from a Google Sheet of Mandarin vocab. The sheet is the source of truth. A scheduled GitHub Action pulls it, checks it, turns it into JSON, and deploys the app to GitHub Pages.

Owner: T. Works iteratively and content-first; prefers minimal, targeted changes over big refactors.

---

## Source data

- **Google Sheet (source of truth):** https://docs.google.com/spreadsheets/d/1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE/edit (ID `1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE`). The normalized data lives in this sheet.
- Access: link-shared "anyone with the link can view". No API key needed.

### Tabs = groups

Every tab whose name does **not** start with `_` is a flashcard group. The current 13 groups, in sheet order:

`Measure Words, Objects, Places, Familiar People, Professional, Body, Activities, Verbs, Directions, Descriptions, Food, Transition Words, Daily Life`

Tabs starting with `_` are metadata and are ignored by the app. As of 2026-09-30 the live sheet has none. The `_readme`, `_review`, `_changelog` and `_lists` tabs exist only in `vocab_normalized.xlsx`.

New tabs must be picked up automatically, so don't hardcode the tab list in the app.

### Schema (identical columns on every group tab)

| column | required | rules |
|---|---|---|
| `hanzi` | yes | Alternatives are separated by ` / ` (e.g. `理发店 / 美发店`). Grammar patterns use `……` (e.g. `要是……就……`). |
| `pinyin` | yes | Tone marks, not tone numbers. Alternatives follow the same order and ` / ` separator as `hanzi`. |
| `english` | yes | Short gloss shown on the card. |
| `type` | yes | One of: `noun, verb, VOV, adjective, adverb, position, preposition, conjunction, time, frequency, sequence, measure_word, phrase, question, pattern` (`VOV` = verb-object compound, T's term) |
| `measure_word` | no | Nouns only. Format `字 (pīnyīn)`, e.g. `张 (zhāng)`. Regex: `^\p{Script=Han} \(.+\)$` |
| `notes` | no | Free text. |
| `examples` | no | `hanzi \| pinyin \| english`, with multiple examples separated by ` ; `. Currently only filled on Measure Words. |

### Card identity and multi-group tagging

- **T does not want to maintain a `card_id` in the sheet.** Don't add one or suggest one.
- **card id** is derived at build time from `hanzi + pinyin + english + type`, after normalization. It is written only to JSON. This distinguishes `家` (measure word) from `家` (home) without any sheet column.
- Each non-header row with content is one membership. Rows with the same card id in different tabs become **one card** tagged with **every** tab it appears in.
- Across rows sharing a card id, `measure_word` **must match exactly**, or the build fails. `notes` and `examples` may differ between tabs: keep all distinct values, labelled by tab.
- A card id must be unique **within** a tab, or the build fails.
- Warn, but don't fail, when the same `hanzi` produces different ids in different tabs. That is often a typo silently splitting one card into two.
- Tradeoff: progress is keyed on id, so editing hanzi, pinyin, english or type resets that card's progress.

Current counts after normalization: 673 rows, 654 unique cards. 23 words appear in more than one tab.

---

## Ingest and validation (`scripts/sync_app_and_source_of_truth/sync.py`)

Pull the whole workbook in one request, so new tabs appear automatically:

```
https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=xlsx
```

Parse it with openpyxl in Python, or SheetJS in Node. The fallback, one request per tab, is `…/gviz/tq?tqx=out:csv&sheet=<Tab Name>`, but that needs the tab names known in advance.

**Validation.** A broken tab header fails the job. Row errors **block that row**: it's left out of `cards.json` and listed in the PR report with its tab, row and field.
1. Every group tab's header matches the schema exactly, in order.
2. The required fields are non-empty on every non-blank row.
3. `type` is in the allowed list.
4. `measure_word` matches the format when present.
5. `examples` parse into `hanzi | pinyin | english` triples when present.
6. Duplicates within a tab (`scripts/sync_app_and_source_of_truth/diff.py`): exact duplicates and partial copies get a proposed `clear_row` edit. Conflicting duplicates and a repeated hanzi are flagged.
7. `measure_word` is consistent across rows sharing a card id.
8. Warn, but don't fail, if pinyin contains digits or hanzi contains Latin letters, or if the same hanzi produces different ids across tabs.

Before comparing, trim whitespace and normalize curly quotes/apostrophes (`’` → `'`).

**Output:** `data/cards.json`, roughly:
```json
{
  "generated_at": "ISO-8601",
  "groups": ["Measure Words", "Objects", "..."],
  "cards": [
    {
      "id": "<derived from hanzi+pinyin+english+type>",
      "hanzi": "地铁", "pinyin": "dìtiě", "english": "subway",
      "type": "noun", "measure_word": "",
      "groups": ["Objects", "Places"],
      "notes": [{"group": "Objects", "text": "..."}, {"group": "Places", "text": "..."}],
      "examples": [{"hanzi": "...", "pinyin": "...", "english": "...", "group": "Objects"}],
      "aliases": ["<old ids, so study progress survives identity edits>"]
    }
  ]
}
```

---

## App behavior

- **One flashcard per card.** You can filter by group, by several groups at once, or show all.
- **Study modes:**
  - hanzi → pinyin + english (default)
  - english → hanzi
  - measure-word cloze: nouns with a `measure_word`, e.g. `一___纸` → `张`
- **Back of card:** pinyin, english, type, measure word, notes, examples, and group tags.
- **Audio:** Web Speech API, `zh-CN` voice, on the hanzi and on each example.
- **Spaced repetition:** Again / Hard / Good / Easy, SM-2 style, keyed on card `id`. Include "due today" and "new only" filters, plus shuffle.
- **Progress:** stored in `localStorage` per device. Wrap every read/write in try/catch, and the app must still work if storage is unavailable. Include export/import of progress as JSON so moving devices doesn't lose history. Cross-device sync is out of scope for now.
- Mobile-first, installable as a PWA (manifest + service worker caching `cards.json`).
- Must build and deploy as a plain static site. No runtime backend.

---

## Hosting / CI (Option A, chosen): PR-gated, two-way sync

The README "Sync pipeline" section covers setup. How it works:
- `sync_app_and_source_of_truth.yml` runs daily at 10:00 UTC (6am EDT; 5am during EST, since GitHub cron is UTC-only) and on manual dispatch. It runs `scripts/sync_app_and_source_of_truth/sync.py`, which fetches the sheet, then validates, diffs, dedupes, runs the Claude review and builds. It then force-pushes branch `sync/sheet` and opens or updates one PR.
  - The job carries over `reviews.json` and `sheet_edits.json` from the open PR. That avoids re-reviewing cards and keeps the reviewer's `"rejected"` statuses.
- `publish_changes_to_source_of_truth.yml` runs on push to `main`. `scripts/publish_changes_to_source_of_truth/writeback.py` pushes `proposed` edits to the sheet with gspread and a service account. Each edit first checks that the cell still holds its "before" value. Then the job runs `scripts/global_use/build.py`, commits, and deploys to Pages.
- Committed state lives in `data/`:
  - `sheet_rows.json`: the sheet snapshot, used as the diff baseline. It mirrors the sheet, including after write-back.
  - `cards.json`: the app data.
  - `reviews.json`: Claude review cache, keyed by card id plus review hash.
  - `sheet_edits.json`: pending edits.
  - `edit_decisions.json`: applied, rejected and conflicting edits. Anything rejected is never re-proposed.
  - `id_aliases.json`: old id → new id.
  - `allowed_words.txt`: extra words example sentences may use.
- Claude review (`scripts/sync_app_and_source_of_truth/review.py`): `claude-opus-5-5` at effort high, structured JSON output, `fallbacks: "default"`, batches of 20, no per-run cap. Reviews every card whose `review_hash` (id + measure word + notes + examples + groups) differs from its cache entry in `data/reviews.json`. `--review-all` (workflow_dispatch input `review_all`) ignores the cache. Example sentences must pass `vocab.unknown_parts`, which segments them into sheet vocab plus `allowed_words.txt`, and must contain the card's word. A failed sentence gets one retry.
- Claude never edits notes; it only flags them.

---

## Repo layout

```
/scripts/global_use/                          # used by both tasks: common, sheet (fetch/read/validate), edits, build (cards.json; also a CLI)
/scripts/sync_app_and_source_of_truth/        # sync task: sync.py (entry point), diff, review (Claude), vocab (sentence check), report
/scripts/publish_changes_to_source_of_truth/  # publish task: writeback.py (approved edits -> Google Sheet)
    # The folders aren't Python packages; entry scripts add scripts/global_use to sys.path.
    # Every file has a header docstring (purpose, when it runs); every function has a docstring.
/tests/          # pytest (poetry run pytest); fakes for Claude + Sheets, no network
/data/           # committed pipeline state (see above)
/app/            # static front end (not built yet)
/.github/workflows/sync_app_and_source_of_truth.yml, publish_changes_to_source_of_truth.yml
```
Python deps are managed with Poetry (`package-mode = false`).

---

## History / decisions

- 2026-09-30: one-time normalization of the original sheet into the schema above (`vocab_normalized.xlsx`).
  - **Type** and **Measure Word** columns were scrambled in Objects, Places, Directions and Daily Life. It looked like a partial-column sort. Clearly wrong values were corrected; acceptable-but-not-ideal ones were left alone.
  - Four duplicates within a tab were merged: 地铁站 in Places, 健身 in Activities, 不一定 in Transition Words, 到 in Directions.
  - `object` / `place` types were renamed to `noun`, since the tab already carries the semantic group.
  - The Measure Words tab got short meanings plus examples with pinyin. Its commentary was moved out of Examples into Notes.
  - Every change (720) is logged in the sheet's `_changelog` tab.
- Hosting: Option A (GitHub Pages + scheduled Action) chosen over live client-side fetch and a Claude Artifact.
- 2026-09-30: sync is PR-gated. Claude's corrections and example sentences are proposed in the PR and written back to the sheet on merge, so the sheet stays the source of truth. Example sentences use only sheet vocab plus `data/allowed_words.txt`. `cards.json` is committed.

## Open items

- [x] Normalized data is in the source sheet (confirmed 2026-09-30: 13 tabs, 7-column schema, no `card_id`).
- 2026-09-30: dropped `card_id` from the sheet schema. The id is now derived in the build.
- [ ] T to review the `_review` tab (e.g. 本来 gloss, 长路口/短路口, 急转, 赚 living in Food).
- [x] Repo made public (needed for free GitHub Pages).
- [ ] T to set up the repo variable and secrets, the service account, and Pages (docs/SETUP.md).
- [ ] Build the front end in `/app/`.