from pathlib import Path
import sys
import ast


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py C:/Users/name/folder")
        return

    p = Path(sys.argv[1])

    if p.is_dir():
        #  getting only the files that end with .py
        py_files = list(p.rglob("*.py"))
        print(f"\nPython files: {len(py_files)}\n")
        analyze_python_files(py_files)

    else:
        print("This is not a valid directory")


def analyze_python_files(py_files):
    for file in py_files:
        metrics = analyze_file(file)
        print()
        # print(metrics)
        generate_report(metrics)
        print()


def analyze_file(file):
    #  encoding with utf-8 as it causes "unicode error" on windows
    with file.open(encoding="utf-8") as f:
        source = f.read()
        lines = source.splitlines()
        tree = ast.parse(source)

        line_data = analyze_lines(lines)
        ast_data = analyze_ast(tree)
        quality_data = analyze_quality(ast_data)
        health_score = calculate_health_score({
            **line_data,
            **ast_data,
        })

        #  unpacking dictionaries in line_data, ast_data, quality_data by using **
        return {
            "file": file,
            "total_lines": len(lines),
            **line_data,
            **ast_data,
            "issues": quality_data,
            "health_score": health_score,
        }


def analyze_lines(lines):
    blank_lines = 0
    comment_lines = 0
    todos = 0
    fixmes = 0

    for line in lines:
        checked_line = line.strip()
        if checked_line == "":
            blank_lines += 1
        if checked_line.startswith("#"):
            comment_lines += 1
        if "TODO" in checked_line:
            todos += 1
        if "FIXME" in checked_line:
            fixmes += 1

    code_lines = len(lines) - blank_lines - comment_lines

    return {
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "code_lines": code_lines,
        "todos": todos,
        "fixmes": fixmes,
    }


def analyze_ast(tree):
    function_data = analyze_functions(tree)
    import_data = analyze_imports(tree)
    control_flow_data = analyze_control_flow(tree)
    classes_data = analyze_classes(tree)
    operations_data = analyze_operations(tree)

    return {
        **function_data,
        **import_data,
        **control_flow_data,
        **classes_data,
        **operations_data,
    }


def analyze_functions(tree):
    functions = 0
    function_details = []

    #  extracting function details
    for code in ast.walk(tree):
        if isinstance(code, ast.FunctionDef):
            functions += 1

            function_name = code.name
            argument_count = len(code.args.args)
            start_line = code.lineno
            end_line = code.end_lineno
            function_length = end_line - start_line + 1

            complexity = calculate_complexity(code)

            function_info = {
                "name": function_name,
                "lines": function_length,
                "arguments": argument_count,
                "complexity": complexity,
            }

            function_details.append(function_info)

    return {
        "functions": functions,
        "function_details": function_details,
    }


def calculate_complexity(function):
    complexity = 1

    for code in ast.walk(function):
        if isinstance(code, ast.If):
            complexity += 1
        if isinstance(code, ast.For):
            complexity += 1
        if isinstance(code, ast.While):
            complexity += 1
        if isinstance(code, ast.ExceptHandler):
            complexity += 1
        if isinstance(code, ast.BoolOp):
            complexity += len(code.values) - 1

    return complexity


def analyze_imports(tree):
    imports = 0
    import_from = 0

    for code in ast.walk(tree):
        if isinstance(code, ast.Import):
            imports += 1

        if isinstance(code, ast.ImportFrom):
            import_from += 1

    return {
        "imports": imports,
        "import_from": import_from,
    }


def analyze_control_flow(tree):
    if_statements = 0
    for_loops = 0
    while_loops = 0
    try_blocks = 0

    for code in ast.walk(tree):
        if isinstance(code, ast.If):
            if_statements += 1
        if isinstance(code, ast.For):
            for_loops += 1
        if isinstance(code, ast.While):
            while_loops += 1
        if isinstance(code, ast.Try):
            try_blocks += 1

    return {
        "if_statements": if_statements,
        "for_loops": for_loops,
        "while_loops": while_loops,
        "try_blocks": try_blocks,
    }


def analyze_classes(tree):
    classes = 0

    for code in ast.walk(tree):
        if isinstance(code, ast.ClassDef):
            classes += 1

    return {
        "classes": classes,
    }


def analyze_operations(tree):
    function_calls = 0
    return_statements = 0
    exceptions_raised = 0
    assertions = 0

    for code in ast.walk(tree):
        if isinstance(code, ast.Call):
            function_calls += 1
        if isinstance(code, ast.Return):
            return_statements += 1
        if isinstance(code, ast.Raise):
            exceptions_raised += 1
        if isinstance(code, ast.Assert):
            assertions += 1

    return {
        "function_calls": function_calls,
        "return_statements": return_statements,
        "exceptions_raised": exceptions_raised,
        "assertions": assertions,
    }


def analyze_quality(ast_data):
    issues = []

    for function in ast_data["function_details"]:
        if function["lines"] > 30:
            issues.append(f"{function['name']} is a long function")

        if function["arguments"] > 5:
            issues.append(f"{function['name']} has too many arguments")

        if function["complexity"] > 10:
            issues.append(
                f"{function['name']} has high complexity " f"({function['complexity']})"
            )

    return issues


def calculate_health_score(metrics):
    score = 100

    for function in metrics["function_details"]:
        if function['lines'] > 30:
            score -= 5
        if function['arguments'] > 5:
            score -= 3
        if function['complexity'] > 10:
            score -= 5

    score -= metrics["todos"]
    score -= metrics["fixmes"]

    return score


def generate_report(metrics):
    print("=" * 50)
    print("CODEBASE HEALTH REPORT")
    print("=" * 50)

    print(f"\nFile: {metrics['file']}")

    print("\nLines")
    print("-" * 20)
    print(f"Total lines:   {metrics['total_lines']}")
    print(f"Code lines:    {metrics['code_lines']}")
    print(f"Blank lines:   {metrics['blank_lines']}")
    print(f"Comment lines: {metrics['comment_lines']}")

    print("\nStructure")
    print("-" * 20)
    print(f"Functions:     {metrics['functions']}")
    print(f"Classes:       {metrics['classes']}")
    print(f"Imports:       {metrics['imports']}")
    print(f"From imports:  {metrics['import_from']}")

    print("\nControl Flow")
    print("-" * 20)
    print(f"If statements: {metrics['if_statements']}")
    print(f"For loops:     {metrics['for_loops']}")
    print(f"While loops:   {metrics['while_loops']}")
    print(f"Try blocks:    {metrics['try_blocks']}")

    print("\nOperations")
    print("-" * 20)
    print(f"Function calls:     {metrics['function_calls']}")
    print(f"Return statements:  {metrics['return_statements']}")
    print(f"Exceptions raised:  {metrics['exceptions_raised']}")
    print(f"Assertions:         {metrics['assertions']}")

    print("\nFunction Analysis")
    print("-" * 20)

    for function in metrics["function_details"]:
        print(f"{function['name']}")
        print(f"  Lines:       {function['lines']}")
        print(f"  Arguments:   {function['arguments']}")
        print(f"  Complexity:  {function['complexity']}")
        print()

    print("\nQuality Issues")
    print("-" * 20)

    if metrics["issues"]:
        for issue in metrics["issues"]:
            print(f"WARNING: {issue}")
    else:
        print("No issues detected")

    print("\nHealth Score")
    print("-" * 20)

    print(f"Score: {metrics['health_score']}")


if __name__ == "__main__":
    main()
