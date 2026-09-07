import argparse


def create_parser():
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
        help="Output file for the JSON report",
    )

    return parser
