import ast

from analysis.lines import analyze_lines
from analysis.ast_analysis import analyze_ast
from analysis.quality import (
    analyze_quality,
    calculate_health_score,
)


def analyze_file(file):
    # encoding with utf-8 as it causes "unicode error" on windows
    with file.open(encoding="utf-8") as f:
        source = f.read()
        lines = source.splitlines()

        tree = parse_python_file(source, file)

        if tree is None:
            return

        line_data = analyze_lines(lines)
        ast_data = analyze_ast(tree)
        quality_data = analyze_quality(ast_data["function_details"])
        health_score = calculate_health_score(
            ast_data["function_details"],
            line_data["todos"],
            line_data["fixmes"],
        )

        # ** is used to unpack dictionaries
        return {
            "file": file,
            "total_lines": len(lines),
            **line_data,
            **ast_data,
            "issues": quality_data,
            "health_score": health_score,
        }


def parse_python_file(source, file):
    try:
        return ast.parse(source)

    # handling the syntax errors
    except SyntaxError as err:
        print(f"Syntax error in {file}: {err}")
        return None
