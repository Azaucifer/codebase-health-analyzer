from pathlib import Path

from cli.arguments import create_parser

from analysis.file_analysis import analyze_file

from reporting.terminal import (
    generate_codebase_summary,
    generate_report,
)

from reporting.json_report import generate_json_report


def main():
    parser = create_parser()
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


if __name__ == "__main__":
    main()
