from pathlib import Path
import ast
import argparse

from analysis.lines import analyze_lines
from analysis.ast_analysis import analyze_ast
from analysis.quality import (
    analyze_quality,
    calculate_health_score,
)

from reporting.terminal import (
    generate_codebase_summary,
    generate_report,
)

from reporting.json_report import generate_json_report


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a Python codebase and generate a health report."
    )

    parser.add_argument(
        "path",
        help="Path to the Python codebase",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate a JSON report",
    )

    parser.add_argument(
        "--output",
        default="codebase_report.json",
        help="Output file for the JSON report"
    )

    args = parser.parse_args()

    p = Path(args.path)

    if p.is_dir():
        py_files = list(p.rglob("*.py"))
        print(f"\nPython files: {len(py_files)}\n")

        analyze_codebase(
            py_files,
            generate_json=args.json,
            output_file=args.output,
        )

    else:
        print("This is not a valid directory")


def analyze_codebase(
        py_files,
        generate_json=False,
        output_file="codebase_report.json",
        ):
    results = []
    for file in py_files:
        metrics = analyze_file(file)

        # skipping files with syntax errors
        if metrics is None:
            continue

        results.append(metrics)

        print()
        generate_report(metrics)
        print()

    generate_codebase_summary(results)
    print()

    if generate_json:
        generate_json_report(results, output_file)


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


if __name__ == "__main__":
    main()