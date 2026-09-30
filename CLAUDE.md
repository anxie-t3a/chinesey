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

## Ingest and validation (build step)

Pull the whole workbook in one request, so new tabs appear automatically:

```
https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=xlsx
```

Parse it with openpyxl in Python, or SheetJS in Node. The fallback, one request per tab, is `…/gviz/tq?tqx=out:csv&sheet=<Tab Name>`, but that needs the tab names known in advance.

**Validation: fail the build with a clear message naming tab + row + field**
1. Every group tab's header matches the schema exactly, in order.
2. The required fields are non-empty on every non-blank row.
3. `type` is in the allowed list.
4. `measure_word` matches the format when present.
5. `examples` parse into `hanzi | pinyin | english` triples when present.
6. No duplicate card id within a tab.
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
      "examples": [{"hanzi": "...", "pinyin": "...", "english": "..."}]
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

## Hosting / CI (Option A, chosen)

GitHub Pages plus a GitHub Actions workflow:
- Triggers: `schedule` (e.g. every 6h), `workflow_dispatch`, and `push` to `main`.
- Steps: fetch the xlsx → validate → write `data/cards.json` → build → deploy to Pages.
- A validation failure fails the job, so the live site keeps serving the last good build.
- Put the sheet ID in a repo variable (`SHEET_ID`), not hardcoded.

---

## Suggested repo layout

```
/scripts/ingest.(py|ts)     # fetch + validate + emit data/cards.json
/scripts/normalize.py       # one-time normalization used on the original sheet (reference only)
/data/cards.json            # generated; commit it or build it in CI (decide)
/data/source_snapshot.json  # raw pull of the original 13 tabs on 2026-09-30 (baseline)
/app/                       # static front end
/.github/workflows/deploy.yml
```

---

## History / decisions

- 2026-09-30: one-time normalization of the original sheet into the schema above (`vocab_normalized.xlsx`).
  - **Type** and **Measure Word** columns were scrambled in Objects, Places, Directions and Daily Life. It looked like a partial-column sort. Clearly wrong values were corrected; acceptable-but-not-ideal ones were left alone.
  - Four duplicates within a tab were merged: 地铁站 in Places, 健身 in Activities, 不一定 in Transition Words, 到 in Directions.
  - `object` / `place` types were renamed to `noun`, since the tab already carries the semantic group.
  - The Measure Words tab got short meanings plus examples with pinyin. Its commentary was moved out of Examples into Notes.
  - Every change (720) is logged in the sheet's `_changelog` tab.
- Hosting: Option A (GitHub Pages + scheduled Action) chosen over live client-side fetch and a Claude Artifact.

## Open items

- [x] Normalized data is in the source sheet (confirmed 2026-09-30: 13 tabs, 7-column schema, no `card_id`).
- 2026-09-30: dropped `card_id` from the sheet schema. The id is now derived in the build.
- [ ] T to review the `_review` tab (e.g. 本来 gloss, 长路口/短路口, 急转, 赚 living in Food).
- [ ] Decide whether `data/cards.json` is committed or built only in CI.