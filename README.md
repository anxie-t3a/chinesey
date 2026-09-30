# Chinese vocab flashcard app

## Source of truth

Google Sheet: https://docs.google.com/spreadsheets/d/1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE/edit

- Sheet ID: `1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE` (stored as the `SHEET_ID` repo variable in CI)
- Shared as "anyone with the link can view", so no API key is needed.
- Build pulls the whole workbook: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=xlsx`
- Every tab not starting with `_` is a flashcard group. New tabs are picked up automatically.

## Schema (every group tab)
hanzi | pinyin | english | type | measure_word | notes | examples
- type from controlled list: noun, verb, VOV, adjective, adverb, position, preposition, conjunction, time, frequency, sequence, measure_word, phrase, question, pattern
- measure_word format: 字 (pinyin)
- examples: `hanzi | pinyin | english ; ...`
- No `card_id` column. The sheet does not maintain IDs.

## Card identity
- The build derives each card's `id` in the JSON from `hanzi + pinyin + english + type`, after trimming and normalizing quotes.
- Rows with the same id in different tabs become one card, tagged with every tab. `measure_word` must match across those rows. `notes` and `examples` may differ and are kept per tab.
- Duplicate ids within a tab fail the build.
- Study progress is keyed on `id`, so editing any of those four fields in the sheet resets progress for that card.

## App requirements
- One flashcard per unique card id; a card in multiple tabs shows all its group tags.
- Hosting: static site on GitHub Pages; scheduled GitHub Action pulls the sheet, validates schema, writes JSON, deploys. Bad data fails the build, not the live app.
- Progress stored per device (localStorage) unless sync is requested later.
