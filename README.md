# Chinesey: Mandarin Vocabulary Flashcards

## Source of truth

Google Sheet: https://docs.google.com/spreadsheets/d/1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE/edit

- Shared as "anyone with the link can view", so no API key is needed.
- Build pulls the whole workbook
- New tabs (vocab groups) are picked up automatically.

## Schema
| column | required | description | format / rules | example |
|---|---|---|---|---|
| `hanzi` | yes | The Chinese word or phrase| Alternatives separated by ` / `; grammar patterns use `……`; must be unique within a tab | `理发店 / 美发店` |
| `pinyin` | yes | Pronunciation | Tone marks, not numbers; alternatives in the same order as `hanzi`, separated by ` / `; utilizes spaces if multi words | `lǐfàdiàn / měifàdiàn` |
| `english` | yes | Short meaning shown on the card | Keep it brief; longer explanation goes in `notes` | `hair salon` |
| `type` | yes | Part of speech / word function | One of: `noun`, `verb`, `VOV`, `adjective`, `adverb`, `position`, `preposition`, `conjunction`, `time`, `frequency`, `sequence`, `measure_word`, `phrase`, `question`, `pattern` | `noun` |
| `measure_word` | no | Classifier used with the noun | Nouns only; format `字 (pīnyīn)` | `家 (jiā)` |
| `notes` | no | Usage notes, nuance, related words | Free text; may differ between tabs for the same card | `理发店 is the everyday word…` |
| `examples` | yes | Example phrases or sentences | Each example is `hanzi \| pinyin \| english`; separate examples with ` ; ` | `一张纸 \| yì zhāng zhǐ \| a sheet of paper ; 一张票 \| yì zhāng piào \| a ticket` |


## Card identity
- The build derives each card's `id` in the JSON from `hanzi + pinyin + english + type`, after trimming and normalizing quotes.
- Rows with the same id in different tabs become one card, tagged with every tab. `measure_word` must match across those rows. `notes` and `examples` may differ and are kept per tab.
- Duplicates within a tab are reported in the sync PR. Exact duplicates and leftover partial copies are proposed for removal. Conflicting duplicates are flagged for you to merge.
- Study progress is keyed on `id`. When one of those four fields changes, the old id is kept as an alias in `cards.json` so progress carries over.

## App requirements
- One flashcard per unique card id; a card in multiple tabs shows all its group tags.
- Hosting: static site on GitHub Pages; a scheduled GitHub Action pulls the sheet, validates it and opens a PR. Merging the PR deploys the app. Bad rows are blocked from the app, never shipped.
- Progress stored per device (localStorage) unless sync is requested later.

## Sync pipeline

```mermaid
flowchart LR
  S[Google Sheet] -->|daily 6am EDT: sync_app_and_source_of_truth.yml| V[validate + diff + dedupe]
  V --> C[Claude review]
  C --> PR[sync PR: cards.json + report + proposed edits]
  PR -->|merge: publish_changes_to_source_of_truth.yml| W[write approved edits to sheet]
  W --> D[deploy to GitHub Pages]
```

**Sync (`.github/workflows/sync_app_and_source_of_truth.yml`, daily at 6am EDT or on demand).** `scripts/sync_app_and_source_of_truth/sync.py`:
1. Downloads the sheet and validates every row. A row with an error is **blocked**: it's left out of the app and listed in the PR.
2. Diffs against the last snapshot (`data/sheet_rows.json`) to find **new**, **changed** and **removed** rows. Changed rows are listed field by field for manual reconciliation.
3. Finds **duplicates within a tab**:
   - exact duplicates and partial copies are proposed for removal
   - conflicting duplicates are flagged
   - a repeated hanzi is flagged
4. Has **Claude review** every card whose content changed since its last review (all cards on the first run). Unchanged cards are skipped. A manual run with **review_all** ticked re-reviews every card. Claude checks accuracy (hanzi, pinyin, gloss, type, measure word) and completeness (e.g. a noun missing its measure word), and writes an **example sentence** for cards that have none. Sentences may use only vocab from the sheet plus the function words in `data/allowed_words.txt`. Code enforces this and rejects sentences that break it.
5. Writes `data/cards.json` with the proposed edits applied, plus a report, and opens or updates one PR (`sync/sheet`).

**Review the PR.** Sheet changes already happened in the sheet; fix them there if they're wrong. Claude's and dedupe's proposed edits are in `data/sheet_edits.json`. To reject one, set its `"status"` to `"rejected"`; it won't be proposed again.

**Merge.** `.github/workflows/publish_changes_to_source_of_truth.yml` writes every remaining proposed edit back to the Google Sheet. Before writing, it checks that each cell still holds its "before" value, and skips any cell someone has changed since. It then rebuilds `cards.json` and deploys to GitHub Pages.

### One-time setup
Step-by-step instructions: [docs/SETUP.md](docs/SETUP.md).

| where | name | value |
|---|---|---|
| repo variable | `SHEET_ID` | `1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE` |
| repo secret | `ANTHROPIC_API_KEY` | Claude API key (review is skipped without it) |
| repo secret | `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON key of a Google Cloud service account with the Sheets API enabled. Share the sheet with the service account's email as **Editor**. |
| Settings → Actions → General | Workflow permissions | "Read and write" + "Allow GitHub Actions to create and approve pull requests" |
| Settings → Pages | Source | GitHub Actions |

### Local
```sh
poetry install
poetry run pytest
poetry run python scripts/sync_app_and_source_of_truth/sync.py --sheet-id <ID> --no-review   # no API calls
```
