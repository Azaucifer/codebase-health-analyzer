import json

from analysis.quality import get_health_rating


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