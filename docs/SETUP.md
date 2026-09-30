# Setup guide

Everything needed, once, to get the daily sheet sync running. Do the steps in order: the
code gets pushed last (step 7), after GitHub, Claude and Google are ready for it.

Total time: about 30–45 minutes. Step 6 (Google) takes the longest.

| # | Step | Where | Time |
|---|---|---|---|
| 1 | ~~Make GitHub Pages possible for this repo~~ (done: repo is public) | GitHub | – |
| 2 | Turn on GitHub Pages | GitHub | 1 min |
| 3 | Let workflows push and open PRs | GitHub | 1 min |
| 4 | Add the `SHEET_ID` variable | GitHub | 1 min |
| 5 | Create a Claude API key | Claude Console + GitHub | 5 min |
| 6 | Create a Google service account | Google Cloud + Google Sheets + GitHub | 15 min |
| 7 | Push the code | Terminal | 2 min |
| 8 | Run the first sync | GitHub | 5–10 min |
| 9 | Review and merge the first PR | GitHub | 10 min |
| 10 | Fix the issues found so far | Google Sheets | 5 min |

All GitHub settings pages below are under **https://github.com/anxie-t3a/chinesey → Settings**.

---

## 1. Make GitHub Pages possible for this repo ✅ done

The repo is now **public**, which is what free GitHub Pages needs. Nothing else to do here.
Remember that everything committed is readable by anyone. **Secrets (steps 5–6) stay
hidden**: they are never shown in the repo or in logs.

## 2. Turn on GitHub Pages

1. Settings → **Pages** (left sidebar, under "Code and automation").
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. That's it: no branch to pick. After the first publish, the site is at
   **https://anxie-t3a.github.io/chinesey/**.

## 3. Let workflows push and open PRs

1. Settings → **Actions** → **General**.
2. **Actions permissions**: leave "Allow all actions and reusable workflows" selected.
3. Scroll to **Workflow permissions**:
   - select **Read and write permissions**
   - tick **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**.

Without this, the sync fails with *"GitHub Actions is not permitted to create or approve pull requests"*.

## 4. Add the `SHEET_ID` variable

1. Settings → **Secrets and variables** → **Actions** → **Variables** tab.
2. **New repository variable**:
   - Name: `SHEET_ID`
   - Value: `1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE`
3. **Add variable**.

Or from the terminal: `gh variable set SHEET_ID --body 1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE`

## 5. Create a Claude API key

This is what lets the sync ask Claude to review cards. Without it, the sync still runs;
it just skips the review.

1. Go to **https://platform.claude.com** (the Claude Console) and sign in or create an account.
   This is separate from a claude.ai chat subscription.
2. **Add credit**: Settings → **Billing** → add a payment method and buy credits
   ($10 is plenty to start).
3. **Cap the spend** (recommended): Settings → **Limits** → set a monthly spend limit, e.g. $20.
4. **Create the key**: Settings → **API keys** → **Create key** → name it `chinesey-github` →
   **Create** → **copy the key now** (it's shown only once; it starts with `sk-ant-`).
5. In GitHub: Settings → **Secrets and variables** → **Actions** → **Secrets** tab →
   **New repository secret**:
   - Name: `ANTHROPIC_API_KEY`
   - Secret: paste the key
   - **Add secret**

   Or from the terminal: `gh secret set ANTHROPIC_API_KEY` (it asks you to paste the key).
6. Don't save the key anywhere else. If it ever leaks, delete it in the Console and repeat
   steps 4–5.

**What it costs**: the first sync reviews all ~655 cards (roughly 33 requests of 20 cards).
My rough estimate is a few dollars, not measured. After that, each daily run reviews only
cards whose content changed, which usually costs cents or nothing. A manual "review all" run
(step 8) costs about the same as the first run. The Console's **Usage** page shows actual spend.

## 6. Create a Google service account (so merges can write to the sheet)

A service account is a robot Google user. You give it Editor access to the sheet, and the
publish workflow signs in as it to write approved edits. Reading the sheet doesn't need
it, because the sheet is link-shared.

> **Which Google account?** Any Google account can own the Cloud project; it doesn't have to
> own the sheet. Work Google accounts often block service-account keys (you'd see *"Service
> account key creation is disabled"* in step 6.5). If that happens, do this step with a
> personal Gmail account instead.

**6.1 Create a project**
1. Go to **https://console.cloud.google.com** and sign in.
2. Accept the terms if asked. No billing account is needed: the Sheets API is free.
3. Click the **project picker** (top left, next to "Google Cloud") → **New project**.
4. Project name: `chinesey` → **Create**.
5. When it's ready, make sure `chinesey` is selected in the project picker.

**6.2 Turn on the Google Sheets API**
1. ☰ menu → **APIs & Services** → **Library**.
2. Search **Google Sheets API** → click it → **Enable**.

**6.3 Create the service account**
1. ☰ menu → **IAM & Admin** → **Service Accounts** → **+ Create service account**.
2. Service account name: `chinesey-sync` (the ID fills in automatically) → **Create and continue**.
3. "Grant this service account access to project": **skip**, click **Continue**.
4. "Grant users access": **skip**, click **Done**.

**6.4 Note its email address**
In the Service Accounts list, copy the email of `chinesey-sync`. It looks like
`chinesey-sync@chinesey-123456.iam.gserviceaccount.com`.

**6.5 Create a key**
1. Click the `chinesey-sync` account → **Keys** tab → **Add key** → **Create new key**.
2. Choose **JSON** → **Create**. A `.json` file downloads. **Treat it like a password.**

**6.6 Share the sheet with the service account**
1. Open the sheet: https://docs.google.com/spreadsheets/d/1ez1xC1P4724rTk__B4eQWOHlru_p_sdq2l2FAwd8obE/edit
2. **Share** (top right) → paste the service account email from 6.4.
3. Set the role to **Editor**, untick **Notify people** → **Share**
   (Google may warn that the address can't receive email; that's fine).
4. Leave the existing "Anyone with the link can **view**" setting as it is. The daily sync
   reads the sheet through it.

**6.7 Add the key to GitHub**
1. Open the downloaded `.json` file in a text editor and copy **all** of it, from the first `{`
   to the last `}`.
2. GitHub: Settings → **Secrets and variables** → **Actions** → **Secrets** →
   **New repository secret**:
   - Name: `GOOGLE_SERVICE_ACCOUNT_JSON`
   - Secret: paste the whole JSON
   - **Add secret**

   Or from the terminal: `gh secret set GOOGLE_SERVICE_ACCOUNT_JSON < ~/Downloads/<the-file>.json`
3. **Delete the downloaded `.json` file** (and empty the trash). GitHub now holds the only
   copy you need. If it ever leaks: Google Cloud → the service account → Keys → delete that
   key, then repeat 6.5–6.7.

**Check**: Settings → Secrets and variables → Actions should now list two secrets
(`ANTHROPIC_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON`) and one variable (`SHEET_ID`).

## 7. Push the code

From the project folder:

```sh
cd ~/Documents/chinesey
git status                 # review what will be committed
git add -A
git commit -m "Add Google Sheet sync pipeline"
git push origin main
```

Pushing to `main` starts the **Publish changes to source of truth** workflow once (Actions tab). There's no data yet,
so it runs the tests and deploys an empty site; that's expected. If it fails at "Deploy",
recheck steps 1–2.

## 8. Run the first sync

The sync runs by itself every day at 6am EDT. To start it now:

1. Repo → **Actions** tab → **Sync app and source of truth** (left list) → **Run workflow** (right side).
2. Branch: `main`. Leave **"Have Claude review ALL cards"** unticked. The first run
   reviews every card anyway, because none has been reviewed yet.
3. **Run workflow**. Click the run to watch it. The first run can take **30–60 minutes**
   while Claude works through all ~655 cards; later daily runs take a few minutes.
4. When it's done, the **Pull requests** tab has **"Vocab sync: review sheet changes and
   Claude's edits"**.

The first run only sets the baseline, so its PR has no "new/changed rows" list. It does have
Claude's review of every card (expect a long list of proposed edits the first time), plus
the two duplicate-row removals found so far.

## 9. Review and merge the PR

1. Open the PR. The description is the report: summary, blocked rows, changes, duplicates,
   **proposed sheet edits**, and Claude's flags.
2. **To reject a proposed edit**:
   1. **Files changed** tab → find `data/sheet_edits.json` → **⋯** → **Edit file**.
   2. Find the edit by its `key` (shown in the report's table) and change
      `"status": "proposed"` to `"status": "rejected"`.
   3. **Commit changes** → "Commit directly to the `sync/sheet` branch" → **Commit changes**.

   Rejected edits aren't written, and they're never proposed again. The next daily sync
   rebuilds this PR but keeps your rejections.
3. Anything wrong in the **sheet** itself (a changed or new row that's a mistake): fix it in
   the Google Sheet. The next sync updates the PR.
4. When you're happy, click **Merge pull request** → **Confirm merge**.
5. Merging starts **Publish changes to source of truth** (Actions tab). It:
   - writes the remaining proposed edits into the Google Sheet (the run's summary page
     shows "N applied, N conflicts, N rejected")
   - rebuilds `cards.json` and deploys the site
6. Open the sheet to see the edits. A "conflict" means that cell changed after the PR was
   opened, so it was left alone; the next sync re-proposes it if it still applies.

## 10. Fix the issues found so far

These came up in an offline test run and are for you to decide in the sheet:

- **睡觉**: different pinyin, english or type in **Body** and **Daily Life**, so it's two
  cards. Make the rows match if it's one word.
- **一个小时** (Objects row 4): has a measure word but its type is `time`. Clear the measure
  word, or change the type if it should be a noun.
- **健身** (Activities row 62) and **急转** (Directions row 55): partial duplicate rows. The
  first PR proposes removing them; nothing to do unless you disagree.
- The `_review` items from the original normalization (本来 gloss, 长路口/短路口, 急转, 赚 in
  Food). Those notes aren't in the live sheet any more; they're in `vocab_normalized.xlsx`.

---

## Day to day

- **Each morning (6am EDT)** the sync runs. If the sheet or the review produced anything
  new, the PR is opened or updated. If nothing changed, nothing happens.
- **Review and merge whenever you like.** Nothing reaches the app or the sheet until you merge.
- **What Claude reviews**: each run reviews every card whose content changed since its last
  review: a new row, an edited field, notes or examples, or a card moved to another tab.
  Unchanged cards are skipped. (An example sentence added by an earlier review counts as a
  change, so that card gets one more review, which checks the new sentence.)
- **Review everything again** (e.g. after editing `data/allowed_words.txt`, or when you want
  a fresh pass): Actions → **Sync app and source of truth** → **Run workflow** → tick
  **"Have Claude review ALL cards"** → **Run workflow**. Locally: add `--review-all`.
- **If the Claude API has an outage mid-run**, the report says so. The cards it didn't reach
  are reviewed on the next run automatically.
- **Allowed words**: if Claude keeps failing to write examples ("uses words outside the app
  vocab" in the report), add the missing basic words to the sheet, or to
  `data/allowed_words.txt` for function words.
- **About the time**: GitHub schedules in UTC and ignores daylight saving, so from November
  to March (EST) the sync runs at 5am instead of 6am. GitHub can also start scheduled runs a
  few minutes late.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Sync fails: *not permitted to create or approve pull requests* | Step 3 |
| Sync fails: *Sheet export did not return an xlsx file* | The sheet must stay "Anyone with the link can view" |
| Sync fails: *Sheet structure is broken* | A tab's header row changed. Every tab not starting with `_` needs exactly `hanzi, pinyin, english, type, measure_word, notes, examples` |
| Report says *review skipped: ANTHROPIC_API_KEY is not set* | Step 5.5 |
| Sync fails with an authentication or permission error from Anthropic | Key deleted or out of credit. Check the Claude Console (step 5) |
| Report says *Claude API unavailable* | Temporary; the next run continues where it stopped |
| Publish fails: *GOOGLE_SERVICE_ACCOUNT_JSON is not set* | Step 6.7, then Actions → Publish changes to source of truth → **Re-run jobs** |
| Publish fails with a 403 / permission error from Google | Sheet not shared with the service account as **Editor** (6.6), or the Sheets API isn't enabled (6.2) |
| Publish fails at "Deploy" | Steps 1–2 |
| Many "conflicts" after a merge | The sheet was edited while the PR was open; those edits are re-proposed next sync if still needed |

## Running things locally (optional)

```sh
poetry install
poetry run pytest                                                          # tests, offline
poetry run python scripts/sync_app_and_source_of_truth/sync.py --sheet-id <ID> --no-review         # full sync without Claude
poetry run python scripts/global_use/build.py                                  # rebuild cards.json from data/
```

A local sync writes into `data/` and `reports/`. Don't commit those by hand; the workflows
own them. To throw away a local run: `git restore data && git clean -fd data reports`.
