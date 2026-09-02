import tokenize
from io import StringIO


def count_todos_and_fixmes(lines):
    """Count TODO and FIXME markers in Python comments."""
    source = "\n".join(lines)

    todos = 0
    fixmes = 0

    tokens = tokenize.generate_tokens(StringIO(source).readline)

    for token in tokens:
        if token.type == tokenize.COMMENT:
            if "TODO" in token.string:
                todos += 1

            if "FIXME" in token.string:
                fixmes += 1

    return todos, fixmes


def analyze_lines(lines):
    blank_lines = 0
    comment_lines = 0

    for line in lines:
        checked_line = line.strip()
        if checked_line == "":
            blank_lines += 1
        if checked_line.startswith("#"):
            comment_lines += 1

    todos, fixmes = count_todos_and_fixmes(lines)

    code_lines = len(lines) - blank_lines - comment_lines

    return {
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "code_lines": code_lines,
        "todos": todos,
        "fixmes": fixmes,
    }