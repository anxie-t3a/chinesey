"""Claude review: check cards for accuracy and completeness, and write missing example sentences.

Used by: the sync_app_and_source_of_truth task (called from sync.py in this folder). It only
runs when ANTHROPIC_API_KEY is set.

For each card, Claude checks:
  - accuracy: hanzi, pinyin, english gloss, type, measure word
  - completeness: e.g. a noun without a measure word
  - example sentence: when the card has none, Claude writes one using only words in the
    app (checked by vocab.py; one retry with feedback if it fails)

Claude's answers come back as JSON matching OUTPUT_SCHEMA. scripts/global_use/edits.py turns
them into proposed sheet edits.

Which cards get reviewed: every run reviews ALL cards whose content changed since their last
review, with no per-run cap. Results are cached in data/reviews.json, keyed by card id with a
fingerprint of the card's content (see review_hash), so unchanged cards are skipped. The
first run therefore reviews every card once. Passing --review-all to sync.py (the
"review_all" option when running the workflow by hand) ignores the cache and reviews every
card in the sheet again.
"""
from __future__ import annotations

import datetime as dt
import json
import sys

import anthropic

from common import TYPES, short_hash
from vocab import unknown_parts, uses_target

MODEL = "claude-opus-5-5"
BATCH_SIZE = 20  # cards per request: big enough to be efficient, small enough to review carefully

# System prompt. The full vocabulary list sits here (not in each message), so it's cached
# once and reused by every batch in a run (prompt caching makes repeat reads cheap).
SYSTEM = """You review Mandarin Chinese vocabulary flashcards for a learner's study app. \
The app teaches Simplified Chinese and standard Mainland Mandarin (Putonghua).

For each card you receive, do three things.

1. Accuracy. Check hanzi, pinyin, english, type and measure_word. Report only real problems: \
a wrong or missing tone mark, wrong characters, a gloss that is wrong or misleading, a type \
that doesn't fit, or an unusual/incorrect measure word. Don't report stylistic preferences or \
rewrite a gloss that is already acceptable. Either citation tones or tone-sandhi spelling is fine \
in the card's pinyin. Alternatives are separated by " / " and must line up between hanzi and pinyin. \
Grammar patterns use "……" as placeholders.

2. Completeness. A noun with no measure_word should get its standard measure word, in the format \
`字 (pīnyīn)`, e.g. `张 (zhāng)`. A measure_word on a card that is not a noun is a problem to report.

3. Example sentence. Only when has_example is false: write one short, natural sentence that uses \
the card's word. The sentence may use ONLY words from the VOCABULARY and ALLOWED WORDS lists below \
(plus punctuation and Arabic numerals). This is checked by code, and a sentence with any other word \
is thrown away. Give pinyin with tone marks and spaces between words, and a natural English \
translation. If no good sentence is possible with these words, return empty strings. When \
has_example is true, return empty strings.

Allowed types: {types}. `VOV` means verb-object compound (e.g. 跑步, 洗澡).

Issue fields: `field` is the column; `current` is its current value; `suggested` is the exact \
replacement value (empty if you can only flag it); `confidence` is how sure you are that the \
current value is wrong.

ALLOWED WORDS (function words):
{allowed}

VOCABULARY (hanzi — pinyin — english):
{vocab}"""

# One problem Claude found with a card.
ISSUE_SCHEMA = {
    "type": "object",
    "properties": {
        "field": {"type": "string", "enum": ["hanzi", "pinyin", "english", "type", "measure_word", "notes"]},
        "kind": {"type": "string", "enum": ["incorrect", "missing", "questionable"]},
        "current": {"type": "string"},
        "suggested": {"type": "string"},   # "" = flag only, no concrete fix
        "reason": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
    },
    "required": ["field", "kind", "current", "suggested", "reason", "confidence"],
    "additionalProperties": False,
}
# The whole response: one entry per card, matched back to the card by `ref`.
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ref": {"type": "integer"},
                    "issues": {"type": "array", "items": ISSUE_SCHEMA},
                    "example": {  # all "" when no sentence was written
                        "type": "object",
                        "properties": {k: {"type": "string"} for k in ("hanzi", "pinyin", "english")},
                        "required": ["hanzi", "pinyin", "english"],
                        "additionalProperties": False,
                    },
                },
                "required": ["ref", "issues", "example"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["cards"],
    "additionalProperties": False,
}


class ReviewUnavailable(Exception):
    """Transient API trouble (rate limit, outage). Stop reviewing for this run and keep what we have."""


def review_hash(card: dict) -> str:
    """Fingerprint of everything Claude looks at on a card. If it changes, the card is reviewed again.

    It covers the identity fields (through the id), the measure word, notes, examples and the
    tabs the card is in. Any content change in the sheet, including an example added by an
    earlier review, leads to exactly one fresh review of that card.
    """
    notes = [n["text"] for n in card["notes"]]
    examples = [(e["hanzi"], e["pinyin"], e["english"]) for e in card["examples"]]
    return short_hash(card["id"], card["measure_word"], notes, examples, card["groups"])


def needs_review(cards: list[dict], reviews: dict, review_all: bool = False) -> list[dict]:
    """The cards to send to Claude this run.

    Normally: cards with no cached review, or whose content changed since their review.
    review_all=True: every card, ignoring the cache (the manual "review everything" option).
    """
    if review_all:
        return list(cards)
    return [c for c in cards if reviews.get(c["id"], {}).get("hash") != review_hash(c)]


def _card_payload(ref: int, card: dict, note: str = "") -> dict:
    """What Claude sees for one card. `ref` is its position in the batch, used to match answers.

    `note` explains why the previous example was rejected (only set on a retry).
    """
    payload = {
        "ref": ref, "hanzi": card["hanzi"], "pinyin": card["pinyin"], "english": card["english"],
        "type": card["type"], "measure_word": card["measure_word"], "groups": card["groups"],
        "notes": " / ".join(n["text"] for n in card["notes"]), "has_example": bool(card["examples"]),
    }
    if note:
        payload["previous_attempt_rejected"] = note
    return payload


class Reviewer:
    """Runs the Claude review for one sync run.

    all_cards: every card in the app (used to give Claude the full vocabulary list)
    allowed:   the function words from allowed_words.txt
    lexicon:   vocab.build_lexicon(...), used to check example sentences
    client:    an anthropic.Anthropic client; tests pass a fake here
    """

    def __init__(self, all_cards: list[dict], allowed: set[str], lexicon: set[str], client=None):
        # max_retries: the SDK retries rate limits / 5xx / network errors with backoff.
        self.client = client or anthropic.Anthropic(max_retries=4)
        self.lexicon = lexicon
        vocab = "\n".join(f"{c['hanzi']} — {c['pinyin']} — {c['english']}" for c in all_cards)
        self.system = [{
            "type": "text",
            "text": SYSTEM.format(types=", ".join(sorted(TYPES)), allowed=" ".join(sorted(allowed)), vocab=vocab),
            "cache_control": {"type": "ephemeral"},  # cache the big system prompt across batches
        }]

    def _call(self, payloads: list[dict]) -> dict[int, dict]:
        """Send one batch of cards to Claude. Returns {ref: result}, or {} if Claude declined.

        Raises ReviewUnavailable for temporary failures. Configuration errors (bad API key,
        invalid request) are raised as-is, so the job fails loudly and gets fixed.
        """
        try:
            # Streaming avoids HTTP timeouts on long responses; get_final_message() waits for all of it.
            with self.client.messages.stream(
                model=MODEL,
                max_tokens=64000,
                system=self.system,
                messages=[{"role": "user", "content": "Review these cards:\n" +
                           json.dumps(payloads, ensure_ascii=False, indent=1)}],
                thinking={"type": "adaptive"},  # Claude decides how much to think per batch
                # effort=high for careful checking; the json_schema format guarantees parseable output.
                output_config={"effort": "high", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
                # If a safety classifier declines the request, the API retries it on a fallback model.
                extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"},
                extra_body={"fallbacks": "default"},
            ) as stream:
                message = stream.get_final_message()
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.BadRequestError):
            raise  # configuration problem: fail loudly
        except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError) as e:
            raise ReviewUnavailable(str(e)) from e
        except anthropic.APIStatusError as e:
            raise ReviewUnavailable(f"{e.status_code}: {e}") from e

        # A refusal or truncated output has no usable JSON; those cards are retried next run.
        if message.stop_reason in ("refusal", "max_tokens"):
            print(f"review batch stopped: {message.stop_reason}", file=sys.stderr)
            return {}
        # The JSON answer is the last text block (thinking and fallback blocks come before it).
        text = [b.text for b in message.content if b.type == "text"]
        return {c["ref"]: c for c in json.loads(text[-1])["cards"]} if text else {}

    def _check_example(self, card: dict, ex: dict) -> str:
        """Return "" if Claude's example is usable, otherwise the reason it was rejected."""
        if not (ex["hanzi"] and ex["pinyin"] and ex["english"]):
            return "no sentence returned"
        if not uses_target(ex["hanzi"], card["hanzi"]):
            return f"'{ex['hanzi']}' does not contain {card['hanzi']}"
        unknown = unknown_parts(ex["hanzi"], self.lexicon)
        if unknown:
            return f"'{ex['hanzi']}' uses words outside the app vocab: {', '.join(unknown)}"
        return ""

    def review(self, cards: list[dict]) -> tuple[dict[str, dict], str]:
        """Review cards in batches. Returns ({card id: review record}, why it stopped early or "").

        If the API becomes unavailable partway through, the cards reviewed so far are kept
        and the rest wait for the next run.
        """
        records: dict[str, dict] = {}
        for start in range(0, len(cards), BATCH_SIZE):
            try:
                self._review_batch(cards[start:start + BATCH_SIZE], records)
            except ReviewUnavailable as e:
                return records, f"Claude API unavailable after {len(records)} cards: {e}"
            print(f"reviewed {min(start + BATCH_SIZE, len(cards))}/{len(cards)} cards", file=sys.stderr)
        return records, ""

    def _review_batch(self, batch: list[dict], records: dict[str, dict]) -> None:
        """Review one batch and add the results to `records`.

        Each rejected example sentence gets one retry, with the reason it failed.
        """
        now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        results = self._call([_card_payload(i, c) for i, c in enumerate(batch)])
        retry = []
        for i, card in enumerate(batch):
            if i not in results:
                continue  # missing from the response; it stays unreviewed and is retried next run
            result = results[i]
            record = {"hash": review_hash(card), "reviewed_at": now, "model": MODEL,
                      "hanzi": card["hanzi"], "issues": result["issues"], "example": None,
                      "example_error": ""}
            if not card["examples"]:
                error = self._check_example(card, result["example"])
                if error:
                    record["example_error"] = error
                    retry.append((i, card, error))
                else:
                    record["example"] = result["example"]
            records[card["id"]] = record

        # One retry for the rejected examples, telling Claude what was wrong last time.
        if retry:
            again = self._call([_card_payload(i, c, err) for i, c, err in retry])
            for i, card, _ in retry:
                if i in again:
                    error = self._check_example(card, again[i]["example"])
                    record = records[card["id"]]
                    record["example"], record["example_error"] = (
                        (None, error) if error else (again[i]["example"], ""))
