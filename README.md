# Chinesey: Mandarin Vocabulary Flashcard Application

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
- Duplicate ids within a tab fail the build.
- Study progress is keyed on `id`, so editing any of those four fields in the sheet resets progress for that card.

## App requirements
- One flashcard per unique card id; a card in multiple tabs shows all its group tags.
- Hosting: static site on GitHub Pages; scheduled GitHub Action pulls the sheet, validates schema, writes JSON, deploys. Bad data fails the build, not the live app.
- Progress stored per device (localStorage) unless sync is requested later.
