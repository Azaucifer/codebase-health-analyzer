import ast
import copy

from analysis.file_analysis import parse_python_file


def extract_functions(tree):
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node)

    return functions


def normalize_function(function):
    function = copy.deepcopy(function)
    function = ast.fix_missing_locations(function)

    for node in ast.walk(function):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node.name = "FUNCTION"

        elif isinstance(node, ast.arg):
            node.arg = "ARGUMENT"

        elif isinstance(node, ast.Name):
            node.id = "VARIABLE"

    return ast.dump(function)


def find_duplicates(functions):
    normalized = {}

    for file, function in functions:
        key = normalize_function(function)

        if key not in normalized:
            normalized[key] = []

        normalized[key].append(
            {
                "file": file,
                "name": function.name,
                "start_line": function.lineno,
            }
        )

    return [
        group
        for group in normalized.values()
        if len(group) > 1
    ]


def detect_duplicates(py_files):
    functions = []

    for file in py_files:
        with file.open(encoding="utf-8") as f:
            source = f.read()

        tree = parse_python_file(source, file)

        if tree is None:
            continue

        for function in extract_functions(tree):
            functions.append((file, function))

    return find_duplicates(functions)
