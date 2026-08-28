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
        print(metrics)


def analyze_file(file):
    #  encoding with utf-8 as it causes "unicode error" on windows
    with file.open(encoding="utf-8") as f:
        source = f.read()
        lines = source.splitlines()
        tree = ast.parse(source)

        blank_lines = 0
        comment_lines = 0

        for line in lines:
            checked_line = line.strip()
            if checked_line == "":
                blank_lines += 1
            if checked_line.startswith("#"):
                comment_lines += 1

        code_lines = len(lines) - blank_lines - comment_lines

        functions = 0
        classes = 0
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

        print()
        return {
            "file": file,
            "total_lines": len(lines),
            "blank_lines": blank_lines,
            "comment_lines": comment_lines,
            "code_lines": code_lines,
            "functions": functions,
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
        }


if __name__ == "__main__":
    main()
