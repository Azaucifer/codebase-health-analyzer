from pathlib import Path
import ast
import json
import argparse

from analysis.lines import analyze_lines
from analysis.ast_analysis import analyze_ast
from analysis.quality import (
    analyze_quality,
    calculate_health_score,
    get_health_rating,
)


def generate_json_report(results, output_file="codebase_report.json"):
    if not results:
        print("No valid Python files found.")
        return

    total_files = len(results)
    total_lines = sum(result["total_lines"] for result in results)
    total_functions = sum(result["functions"] for result in results)
    total_classes = sum(result["classes"] for result in results)
    total_todos = sum(result["todos"] for result in results)
    total_fixmes = sum(result["fixmes"] for result in results)

    average_health_score = (
        sum(result["health_score"] for result in results) / total_files
    )

    report = {
        "summary": {
            "python_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_todos": total_todos,
            "total_fixmes": total_fixmes,
            "average_health_score": round(average_health_score, 1),
            "rating": get_health_rating(average_health_score),
        },
        "files": [],
    }

    for result in results:
        report["files"].append(
            {
                "file": result["file"].name,
                "total_lines": result["total_lines"],
                "code_lines": result["code_lines"],
                "blank_lines": result["blank_lines"],
                "comment_lines": result["comment_lines"],
                "functions": result["functions"],
                "classes": result["classes"],
                "imports": result["imports"],
                "import_from": result["import_from"],
                "if_statements": result["if_statements"],
                "for_loops": result["for_loops"],
                "while_loops": result["while_loops"],
                "try_blocks": result["try_blocks"],
                "function_calls": result["function_calls"],
                "return_statements": result["return_statements"],
                "exceptions_raised": result["exceptions_raised"],
                "assertions": result["assertions"],
                "todos": result["todos"],
                "fixmes": result["fixmes"],
                "health_score": result["health_score"],
                "rating": get_health_rating(result["health_score"]),
                "issues": result["issues"],
                "functions_details": result["function_details"],
            }
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"JSON report saved to: {output_file}")


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

        #  skipping files with syntax errors
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
    #  encoding with utf-8 as it causes "unicode error" on windows
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

        #  ** is used to unpack dictionaries
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

    #  handling the syntax errors
    except SyntaxError as err:
        print(f"Syntax error in {file}: {err}")
        return None


def generate_codebase_summary(results):
    if not results:
        print("No valid Python files found.")
        return

    total_files = len(results)
    total_lines = sum(result["total_lines"] for result in results)
    total_functions = sum(result["functions"] for result in results)
    total_classes = sum(result["classes"] for result in results)
    total_todos = sum(result["todos"] for result in results)
    total_fixmes = sum(result["fixmes"] for result in results)

    average_health_score = (
        sum(result["health_score"] for result in results) / total_files
    )

    print("=" * 50)
    print("CODEBASE SUMMARY")
    print("=" * 50)

    print(f"\nPython files:     {total_files}")
    print(f"Total lines:      {total_lines}")
    print(f"Total functions:  {total_functions}")
    print(f"Total classes:    {total_classes}")
    print(f"Total TODOs:      {total_todos}")
    print(f"Total FIXMEs:     {total_fixmes}")

    print("\nHealth")
    print("-" * 20)
    print(f"Average score:    {average_health_score:.1f}/100")
    print(f"Rating:           {get_health_rating(average_health_score)}")

    print("\nFiles Needing Attention")
    print("-" * 20)

    problem_files = []

    for result in results:
        if result["issues"]:
            problem_files.append(result)

    sorted_results = sorted(problem_files, key=lambda result: result["health_score"])

    for result in sorted_results[:3]:
        print(f"{result['file'].name}: " f"{result['health_score']}/100")

        for issue in result["issues"]:
            print(f"  - {issue}")
        print()


def display_line_metrics(metrics):
    print("\nLines")
    print("-" * 20)
    print(f"Total lines:   {metrics['total_lines']}")
    print(f"Code lines:    {metrics['code_lines']}")
    print(f"Blank lines:   {metrics['blank_lines']}")
    print(f"Comment lines: {metrics['comment_lines']}")


def display_structure_metrics(metrics):
    print("\nStructure")
    print("-" * 20)
    print(f"Functions:     {metrics['functions']}")
    print(f"Classes:       {metrics['classes']}")
    print(f"Imports:       {metrics['imports']}")
    print(f"From imports:  {metrics['import_from']}")


def display_control_flow_metrics(metrics):
    print("\nControl Flow")
    print("-" * 20)
    print(f"If statements: {metrics['if_statements']}")
    print(f"For loops:     {metrics['for_loops']}")
    print(f"While loops:   {metrics['while_loops']}")
    print(f"Try blocks:    {metrics['try_blocks']}")


def display_operation_metrics(metrics):
    print("\nOperations")
    print("-" * 20)
    print(f"Function calls:     {metrics['function_calls']}")
    print(f"Return statements:  {metrics['return_statements']}")
    print(f"Exceptions raised:  {metrics['exceptions_raised']}")
    print(f"Assertions:         {metrics['assertions']}")


def display_function_analysis_metrics(metrics):
    print("\nFunction Analysis")
    print("-" * 20)

    for function in metrics["function_details"]:
        print(f"{function['name']}")
        print(f"  Start Line:        {function['start_line']}")
        print(f"  Lines:             {function['lines']}")
        print(f"  Arguments:         {function['arguments']}")
        print(f"  Complexity:        {function['complexity']}")
        print()


def display_quality_issues_metrics(metrics):
    print("\nQuality Issues")
    print("-" * 20)

    print(f"TODOs:  {metrics['todos']}")
    print(f"FIXMEs: {metrics['fixmes']}")
    print()

    if metrics["issues"]:
        for issue in metrics["issues"]:
            print(f"WARNING: {issue}")

    if metrics["todos"] > 0:
        print(f"WARNING: {metrics['todos']} TODO(s) found")

    if metrics["fixmes"] > 0:
        print(f"WARNING: {metrics['fixmes']} FIXME(s) found")

    if not metrics["issues"] and metrics["todos"] == 0 and metrics["fixmes"] == 0:
        print("No issues detected")


def display_health_score_metrics(metrics):
    print("\nHealth Score")
    print("-" * 20)

    print(f"Score: {metrics['health_score']}/100")
    print(f"Rating: {get_health_rating(metrics['health_score'])}")


def generate_report(metrics):
    print("=" * 50)
    print("CODEBASE HEALTH REPORT")
    print("=" * 50)

    print(f"\nFile: {metrics['file'].name}")

    display_line_metrics(metrics)
    display_structure_metrics(metrics)
    display_control_flow_metrics(metrics)
    display_operation_metrics(metrics)
    display_function_analysis_metrics(metrics)
    display_quality_issues_metrics(metrics)
    display_health_score_metrics(metrics)


if __name__ == "__main__":
    main()
