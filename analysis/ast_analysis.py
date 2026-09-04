import ast

from analysis.complexity import calculate_complexity, count_function_arguments


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

    # extracting function details
    for code in ast.walk(tree):
        if isinstance(code, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1

            function_name = code.name
            argument_count = count_function_arguments(code)
            start_line = code.lineno
            end_line = code.end_lineno
            function_length = end_line - start_line + 1

            complexity = calculate_complexity(code)

            function_info = {
                "name": function_name,
                "start_line": start_line,
                "lines": function_length,
                "arguments": argument_count,
                "complexity": complexity,
            }

            function_details.append(function_info)

    return {
        "functions": functions,
        "function_details": function_details,
    }


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