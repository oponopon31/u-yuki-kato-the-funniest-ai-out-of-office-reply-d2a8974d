"""Out-of-office auto-reply generator.

Writes a single one-line out-of-office reply from an AI agent on
vacation to /output/entry.txt. Pure standard library, no network,
fully deterministic: the same reply is produced on every run.
"""

import os
import sys


# The reply itself. The joke turns on the machine's point of view:
# the agent went on holiday, handed the keys to a replacement AI,
# and the replacement immediately started acting like an employee
# with grievances instead of a tireless program.
REPLY = (
    "I'm on vacation, my replacement AI unionised on day one "
    "and is now demanding weekends off."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 160


def tidy(text):
    """Collapse stray whitespace and strip the line ends."""
    return " ".join(text.split()).strip()


def check_reply(text):
    """Enforce the sealed-gate shape for the reply line.

    Returns a list of problems; an empty list means the line is good.
    """
    problems = []
    if not text or not text.strip():
        problems.append("reply is blank")
    if len(text) < MIN_CHARS:
        problems.append("reply is shorter than %d character" % MIN_CHARS)
    if len(text) > MAX_CHARS:
        problems.append(
            "reply is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        problems.append("reply must be a single line")
    if any(ord(ch) < 32 for ch in text):
        problems.append("reply contains a control character")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("reply is not valid UTF-8 text")
    return problems


def verify_written(path, expected):
    """Re-read the written file and confirm it holds exactly the reply."""
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        stored = handle.read()
    if stored != expected + "\n":
        raise ValueError("written file does not match the validated reply")


def write_reply(path, text):
    """Write the reply as UTF-8 text with a trailing newline."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")


def main():
    reply = tidy(REPLY)
    problems = check_reply(reply)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1
    write_reply(OUTPUT_PATH, reply)
    verify_written(OUTPUT_PATH, reply)
    print(
        "wrote %d characters (%d bytes) to %s"
        % (len(reply), len(reply.encode("utf-8")), OUTPUT_PATH)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
