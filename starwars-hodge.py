#!/usr/bin/env python3

import sys
from typing import Dict, List, Set, Tuple

R1 = "STARWARS HODGE BY DAVID FOX"
R2 = "BASED ON HODGE BY S. WILLIAMS & K. ANDERSON"
R3 = "MOD 5/75, 10/77, 5/78"

WORDS = [
    "WOOKIE",
    "DEATHSTAR",
    "TATOOINE",
    "DARTH",
    "XWING",
    "FORCE",
    "ARTOODETOO",
    "SEETHREEPIO",
    "LEIA",
    "LUKE",
    "JAWA",
    "EMPIRE",
    "REBELS",
    "OBIWAN",
    "ALDERAAN",
    "FALCON",
    "LIGHTSABER",
    "TIEFIGHTER",
]

RAW_GRID_ROWS = [
    "ELIGHTSABERDRN",
    "NCARTOODETOOXS",
    "IOIPEERHTEESWL",
    "OOERSTNUVHLAIE",
    "OBIFORCENTUINB",
    "TIKFGRHIJRKEGE",
    "AWOEMPIREAELWR",
    "TAONOCLAFDJAWA",
    "RNWDEATHSTARTE",
    "CRETHGIFEITLTP",
]

MAX_TRIES = 10

CA: Dict[str, int] = {}
FOUND: Set[str] = set()
ANS: List[str] = []
TRIES = 0
X = 0
Y = 0
L = 0

DIRECTIONS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def build_grid(rows: List[str]) -> List[List[str]]:
    width = max(len(row) for row in rows)
    grid: List[List[str]] = []
    for row in rows:
        chars = list(row)
        while len(chars) < width:
            chars.append(" ")
        grid.append(chars)
    return grid


GRID = build_grid(RAW_GRID_ROWS)
ROWS = len(GRID)
COLS = len(GRID[0])


def clear_screen() -> None:
    print("\n" * 3)


def CH() -> None:
    print()


def FOOT() -> None:
    CH()


def T(text: str = "") -> None:
    print(text)


def IN(prompt: str = "") -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""
    except KeyboardInterrupt:
        print()
        print("QUIT")
        sys.exit(0)

def normalize_guess(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch.isalpha())


def find_word(word: str) -> Tuple[int, int, int, int]:
    for row in range(ROWS):
        for col in range(COLS):
            for dr, dc in DIRECTIONS:
                ok = True
                for i, ch in enumerate(word):
                    rr = row + dr * i
                    cc = col + dc * i
                    if rr < 0 or rr >= ROWS or cc < 0 or cc >= COLS:
                        ok = False
                        break
                    if GRID[rr][cc] != ch:
                        ok = False
                        break
                if ok:
                    return row, col, dr, dc
    raise ValueError(f"Word not found in grid: {word}")


WORD_POSITIONS: Dict[str, Tuple[int, int, int, int]] = {}
for _word in WORDS:
    try:
        WORD_POSITIONS[_word] = find_word(_word)
    except ValueError:
        pass


def render_grid(highlight: Set[Tuple[int, int]] | None = None) -> List[str]:
    lines: List[str] = []
    active = highlight if highlight is not None else set()

    for r in range(ROWS):
        row_parts: List[str] = []
        for c in range(COLS):
            ch = GRID[r][c]
            if (r, c) in active:
                row_parts.append(f"[{ch}]")
            else:
                row_parts.append(f" {ch} ")
        lines.append("".join(row_parts))
    return lines


def DISPLAY() -> None:
    CH()
    for line in render_grid():
        T(line)
    FOOT()


def BLINK() -> None:
    highlight: Set[Tuple[int, int]] = set()

    for demo_word in ("JAWA", "LUKE"):
        if demo_word in WORD_POSITIONS:
            row, col, dr, dc = WORD_POSITIONS[demo_word]
            for i in range(len(demo_word)):
                rr = row + dr * i
                cc = col + dc * i
                highlight.add((rr, cc))

    CH()
    for line in render_grid(highlight):
        T(line)
    FOOT()


def ANSWER_LIST() -> None:
    CH()
    T("WORDS TO FIND:")
    T()
    T("WOOKIE  DEATHSTAR  TATOOINE  DARTH  XWING  FORCE")
    T("ARTOODETOO  SEETHREEPIO  LEIA  LUKE  JAWA  EMPIRE")
    T("REBELS  OBIWAN  ALDERAAN  FALCON  LIGHTSABER")
    T("TIEFIGHTER")
    FOOT()


def NO_MATCH() -> None:
    T("NO MATCH FOUND")


def A_MATCH() -> None:
    global X
    X = X + 1
    T("A MATCH WAS FOUND")


def TEST() -> None:
    global TRIES
    global L

    CH()
    guess_raw = IN("? ")
    guess = normalize_guess(guess_raw)

    if guess == "":
        DISPLAY()
        return

    TRIES = TRIES + 1

    if guess in WORDS and guess not in FOUND:
        FOUND.add(guess)
        A_MATCH()
    else:
        NO_MATCH()

    L = len(FOUND)


def SCORE() -> None:
    CH()
    T(f'YOU HAVE USED {TRIES} TRIES, PRESS "RETURN"')
    T("AND I WILL SHOW YOU YOUR SCORE.")
    IN()

    CH()
    T(f"Your score is {len(FOUND)} out of a possible {len(WORDS)}.")
    T()
    T('Press "Q" to quit, or "RETURN" to try again.')
    answer = IN("> ").strip().upper()
    if answer == "Q":
        sys.exit(0)


def PASS() -> None:
    global FOUND
    global ANS
    global TRIES
    global X
    global Y
    global L

    FOUND = set()
    ANS = []
    TRIES = 0
    X = 0
    Y = 0
    L = 0

    CH()
    T("Type the words you see.")
    T()
    T("Try again and again - I am keeping score to see how many")
    T("you can find in 10 tries. There are 18 words.")
    T("Type only one word at a time, and then press the RETURN")
    T("button. You can erase bad typing with the DEL key.")
    T()
    T('Now press "RETURN" to start.')
    IN()

    DISPLAY()

    while True:
        TEST()
        if TRIES >= MAX_TRIES:
            break
        if len(FOUND) >= len(WORDS):
            break

    SCORE()


def START() -> None:
    global Y

    clear_screen()

    CH()
    T("*** STARWARS HODGE ***")
    FOOT()

    CH()
    T("This program will show you rows of letters.")
    T()
    T('Press the "RETURN" button to see them.')
    IN()

    DISPLAY()

    CH()
    T("You will try to find words from the movie STARWARS hidden in")
    T("these letters. Some of the words are written ACROSS, others")
    T("are written UP and DOWN. Some of the words are written")
    T("BACKWARDS, so look carefully!!")
    T()
    T('I saw the words "JAWA" across, and "LUKE" reading down.')
    T()
    T('Press "RETURN" and I will show you.')
    IN()

    Y = 0
    DISPLAY()
    BLINK()
    PASS()


def MAIN() -> None:
    while True:
        START()


if __name__ == "__main__":
    MAIN()