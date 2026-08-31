from pathlib import Path
import sys
import ast


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py C:/Users/name/folder")

    elif len(sys.argv) == 2:
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
        print(metrics)
        print()


def analyze_file(file):
    #  encoding with utf-8 as it causes "unicode error" on windows
    with file.open(encoding="utf-8") as f:
        source = f.read()
        lines = source.splitlines()
        tree = ast.parse(source)

        line_data = analyze_lines(lines)
        ast_data = analyze_ast(tree)

        #  unpacking dictionaries in line_data and ast_data by using **
        return {
            "file": file,
            "total_lines": len(lines),
            **line_data,
            **ast_data,
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
    functions = 0
    classes = 0
    function_details = []
    issues = []
    imports = 0
    import_from = 0
    if_statements = 0
    for_loops = 0
    while_loops = 0
    try_blocks = 0
    function_calls = 0
    return_statements = 0
    exceptions_raised = 0
    assertions = 0

    #  checking the code because functions and classes can be inside other functions or classes.
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
                "complexity": complexity
            }

            function_details.append(function_info)

            if function_length > 30:
                issues.append(f"WARNING: {function_name} is a long function")

            if argument_count > 5:
                issues.append(f"WARNING: {function_name} has too many arguments")

        if isinstance(code, ast.ClassDef):
            classes += 1
        if isinstance(code, ast.Import):
            imports += 1
        if isinstance(code, ast.ImportFrom):
            import_from += 1
        if isinstance(code, ast.If):
            if_statements += 1
        if isinstance(code, ast.For):
            for_loops += 1
        if isinstance(code, ast.While):
            while_loops += 1
        if isinstance(code, ast.Try):
            try_blocks += 1
        if isinstance(code, ast.Call):
            function_calls += 1
        if isinstance(code, ast.Return):
            return_statements += 1
        if isinstance(code, ast.Raise):
            exceptions_raised += 1
        if isinstance(code, ast.Assert):
            assertions += 1

    return {
        "functions": functions,
        "function_details": function_details,
        "classes": classes,
        "imports": imports,
        "import_from": import_from,
        "if_statements": if_statements,
        "for_loops": for_loops,
        "while_loops": while_loops,
        "try_blocks": try_blocks,
        "function_calls": function_calls,
        "return_statements": return_statements,
        "exceptions_raised": exceptions_raised,
        "assertions": assertions,
        "issues": issues,
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


if __name__ == "__main__":
    main()
