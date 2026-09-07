from analysis.quality import get_health_rating


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