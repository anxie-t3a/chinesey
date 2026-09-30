"""Check that an example sentence uses only words the app already teaches.

Used by: the sync_app_and_source_of_truth task, through review.py in this folder, to accept
or reject the example sentences Claude writes.

The "lexicon" is every hanzi in the sheet plus the function words in data/allowed_words.txt.
Chinese has no spaces between words, so a sentence is checked by trying to split it
completely into lexicon words (a word-break search). If no complete split exists, the
sentence uses a word outside the app and is rejected.
"""
from __future__ import annotations

from common import ALT_SEP, DATA, HAN_RUN

ALLOWED_WORDS_FILE = DATA / "allowed_words.txt"


def load_allowed_words(path=ALLOWED_WORDS_FILE) -> set[str]:
    """Read allowed_words.txt: words separated by whitespace, with `#` starting a comment."""
    words = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0]  # drop the comment part of the line
        words.update(w for w in line.split() if w)
    return words


def word_pieces(hanzi: str) -> list[list[str]]:
    """Split a hanzi cell into its alternatives, each as a list of Chinese-character pieces.

    `要是……就……`       -> [["要是", "就"]]            (a grammar pattern has several pieces)
    `理发店 / 美发店`   -> [["理发店"], ["美发店"]]    (two alternatives)
    """
    return [HAN_RUN.findall(alt) for alt in hanzi.split(ALT_SEP) if HAN_RUN.findall(alt)]


def build_lexicon(hanzi_values, allowed: set[str]) -> set[str]:
    """Every word a sentence may use: all pieces of all hanzi in the sheet, plus allowed words."""
    lexicon = set(allowed)
    for hanzi in hanzi_values:
        for pieces in word_pieces(hanzi):
            lexicon.update(pieces)
    return lexicon


def unknown_parts(sentence: str, lexicon: set[str]) -> list[str]:
    """Return the parts of `sentence` that can't be made from lexicon words. Empty list = valid.

    Punctuation, spaces and Arabic numerals are ignored; only runs of Chinese characters
    are checked. The returned parts are sent back to Claude as feedback on a retry.
    """
    longest = max((len(w) for w in lexicon), default=1)
    unknown = []
    for run in HAN_RUN.findall(sentence):
        n = len(run)
        # Word break by dynamic programming: ok[i] is True when run[:i] splits fully into
        # lexicon words. Only look back `longest` characters, since no word is longer than that.
        ok = [True] + [False] * n
        for i in range(1, n + 1):
            ok[i] = any(ok[j] and run[j:i] in lexicon for j in range(max(0, i - longest), i))
        if ok[n]:
            continue  # this run is fine

        # The run failed. Find which characters no lexicon word covers, to report them.
        covered = [False] * n
        for i in range(n):
            for j in range(i + 1, min(n, i + longest) + 1):
                if run[i:j] in lexicon:
                    covered[i:j] = [True] * (j - i)
        stretch = ""
        for ch, c in zip(run, covered):
            if c and stretch:
                unknown.append(stretch)  # end of an uncovered stretch
                stretch = ""
            elif not c:
                stretch += ch
        if stretch:
            unknown.append(stretch)
        if not any(not c for c in covered):
            unknown.append(run)  # every char is covered but no full segmentation exists
    return unknown


def uses_target(sentence: str, hanzi: str) -> bool:
    """True when the sentence contains the card's own word.

    Any alternative counts. For a grammar pattern, all of its pieces must appear in order
    (e.g. 要是 … 就 …).
    """
    for pieces in word_pieces(hanzi):
        pos = 0
        for piece in pieces:
            pos = sentence.find(piece, pos)
            if pos < 0:
                break
            pos += len(piece)
        else:  # the loop didn't break, so every piece was found in order
            return True
    return False
