import pytest
from pathlib import Path
import sys
import ast
import os
import json

from analyzer import (
    analyze_file,
    analyze_lines,
    analyze_functions,
    analyze_imports,
    analyze_control_flow,
    analyze_classes,
    analyze_operations,
    analyze_quality,
    calculate_complexity,
    calculate_health_score,
    count_function_arguments,
    get_health_rating,
    parse_python_file,
    display_quality_issues_metrics,
    main,
)


# Helper function to capture stdout using a temporary file
def capture_output(func, *args, **kwargs):
    """Capture stdout while running a function"""
    import tempfile
    old_stdout = sys.stdout
    temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
    sys.stdout = temp_file
    try:
        func(*args, **kwargs)
        temp_file.flush()
        with open(temp_file.name, 'r') as f:
            return f.read()
    finally:
        sys.stdout = old_stdout
        temp_file.close()
        Path(temp_file.name).unlink(missing_ok=True)


# ==================== Tests for get_health_rating ====================


def test_get_health_rating():
    """Test health rating categorization"""
    assert get_health_rating(100) == "Excellent"
    assert get_health_rating(90) == "Excellent"
    assert get_health_rating(89) == "Good"
    assert get_health_rating(75) == "Good"
    assert get_health_rating(74) == "Needs Improvement"
    assert get_health_rating(50) == "Needs Improvement"
    assert get_health_rating(49) == "Poor"
    assert get_health_rating(0) == "Poor"


# ==================== Tests for analyze_lines ====================


def test_analyze_lines_basic():
    """Test basic line analysis"""
    lines = [
        "def test():",
        "    # This is a comment",
        "    print('hello')",
        "",
        "    # TODO: fix this",
        "    # FIXME: urgent",
        "    return True",
    ]

    result = analyze_lines(lines)

    assert result["blank_lines"] == 1
    assert result["comment_lines"] == 3
    assert result["code_lines"] == 3
    assert result["todos"] == 1
    assert result["fixmes"] == 1


def test_analyze_lines_empty():
    """Test empty file analysis"""
    lines = []
    result = analyze_lines(lines)
    assert result["blank_lines"] == 0
    assert result["comment_lines"] == 0
    assert result["code_lines"] == 0
    assert result["todos"] == 0
    assert result["fixmes"] == 0


def test_analyze_lines_only_blanks():
    """Test file with only blank lines"""
    lines = ["", "", ""]
    result = analyze_lines(lines)
    assert result["blank_lines"] == 3
    assert result["code_lines"] == 0
    assert result["comment_lines"] == 0


def test_analyze_lines_todos_and_fixmes_in_comments():
    """Test that TODOs and FIXMEs are counted even in comments"""
    lines = [
        "# TODO: implement this",
        "# FIXME: bug here",
        "print('hello')  # TODO: remove print",
    ]
    result = analyze_lines(lines)
    assert result["todos"] == 2
    assert result["fixmes"] == 1


# ==================== Tests for calculate_complexity ====================


def test_calculate_complexity_simple_function():
    """Test complexity of a simple function"""
    code = """
def simple():
    print('hello')
    return True
    """
    tree = ast.parse(code)
    function = tree.body[0]
    assert calculate_complexity(function) == 1


def test_calculate_complexity_with_if_statements():
    """Test complexity with if statements including elif"""
    code = """
def with_if(x):
    if x > 0:
        print('positive')
    elif x < 0:
        print('negative')
    else:
        print('zero')
    return x
    """
    tree = ast.parse(code)
    function = tree.body[0]
    assert calculate_complexity(function) == 3


def test_calculate_complexity_elif():
    code = """
def example(value):
    if value == 1:
        pass
    elif value == 2:
        pass
    elif value == 3:
        pass
"""

    tree = ast.parse(code)
    function = tree.body[0]

    assert calculate_complexity(function) == 4


def test_calculate_complexity_with_loops():
    """Test complexity with loops"""
    code = """
def with_loops(items):
    for item in items:
        print(item)
    while True:
        break
    return True
    """
    tree = ast.parse(code)
    function = tree.body[0]
    assert calculate_complexity(function) == 3


def test_calculate_complexity_with_bool_ops():
    """Test complexity with boolean operations"""
    code = """
def with_bool(x, y, z):
    if x and y and z:
        return True
    return False
    """
    tree = ast.parse(code)
    function = tree.body[0]
    assert calculate_complexity(function) == 4


def test_calculate_complexity_with_try_except():
    """Test complexity with try/except"""
    code = """
def with_try():
    try:
        print('try')
    except Exception:
        print('except')
    return True
    """
    tree = ast.parse(code)
    function = tree.body[0]
    assert calculate_complexity(function) == 2


def test_calculate_complexity_nested_function():
    code = """
def outer():
    def inner():
        if condition:
            pass

    return inner
"""

    tree = ast.parse(code)
    outer_function = tree.body[0]

    assert calculate_complexity(outer_function) == 1


def test_calculate_complexity_nested_async_function():
    code = """
def outer():
    async def inner():
        if condition:
            pass

    return inner
"""

    tree = ast.parse(code)
    outer_function = tree.body[0]

    assert calculate_complexity(outer_function) == 1


# ==================== Tests for analyze_functions ====================


def test_analyze_functions_basic():
    """Test function analysis"""
    code = """
def func1():
    return True

def func2(x, y):
    if x > y:
        return x
    return y

def func3(a, b, c, d, e):
    return a + b + c + d + e
    """
    tree = ast.parse(code)
    result = analyze_functions(tree)

    assert result["functions"] == 3
    assert len(result["function_details"]) == 3
    assert result["function_details"][0]["name"] == "func1"
    assert result["function_details"][0]["arguments"] == 0
    assert result["function_details"][0]["complexity"] == 1
    assert result["function_details"][0]["start_line"] == 2


def test_analyze_functions_nested():
    """Test function analysis with nested functions"""
    code = """
def outer():
    def inner():
        return True
    return inner()
    """
    tree = ast.parse(code)
    result = analyze_functions(tree)
    assert result["functions"] == 2


def test_analyze_functions_no_functions():
    """Test file with no functions"""
    code = """
print('hello')
x = 5
"""
    tree = ast.parse(code)
    result = analyze_functions(tree)
    assert result["functions"] == 0
    assert result["function_details"] == []


def test_count_function_arguments():
    code = """
def example(a, b=10, *args, c=20, **kwargs):
    pass
"""

    tree = ast.parse(code)
    function = tree.body[0]

    assert count_function_arguments(function) == 5


def test_analyze_functions_async():
    code = """
async def fetch_data(url):
    return url
"""

    tree = ast.parse(code)
    result = analyze_functions(tree)

    assert result["functions"] == 1


# ==================== Tests for analyze_imports ====================


def test_analyze_imports_basic():
    """Test basic import analysis"""
    code = """
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
"""
    tree = ast.parse(code)
    result = analyze_imports(tree)
    assert result["imports"] == 2
    assert result["import_from"] == 2


def test_analyze_imports_none():
    """Test file with no imports"""
    code = """
def test():
    return True
"""
    tree = ast.parse(code)
    result = analyze_imports(tree)
    assert result["imports"] == 0
    assert result["import_from"] == 0


# ==================== Tests for analyze_control_flow ====================


def test_analyze_control_flow_basic():
    """Test control flow analysis"""
    code = """
if x > 0:
    print('positive')

for i in range(10):
    print(i)

while x < 10:
    x += 1

try:
    risky_operation()
except:
    handle_error()
"""
    tree = ast.parse(code)
    result = analyze_control_flow(tree)

    assert result["if_statements"] == 1
    assert result["for_loops"] == 1
    assert result["while_loops"] == 1
    assert result["try_blocks"] == 1


def test_analyze_control_flow_nested():
    """Test nested control flow structures"""
    code = """
for i in range(10):
    if i % 2 == 0:
        print(i)
    while i < 5:
        i += 1
"""
    tree = ast.parse(code)
    result = analyze_control_flow(tree)
    assert result["for_loops"] == 1
    assert result["if_statements"] == 1
    assert result["while_loops"] == 1


# ==================== Tests for analyze_classes ====================


def test_analyze_classes_basic():
    """Test class analysis"""
    code = """
class MyClass:
    def method1(self):
        return True

class AnotherClass:
    pass
"""
    tree = ast.parse(code)
    result = analyze_classes(tree)
    assert result["classes"] == 2


def test_analyze_classes_nested():
    """Test nested classes"""
    code = """
class Outer:
    class Inner:
        pass
"""
    tree = ast.parse(code)
    result = analyze_classes(tree)
    assert result["classes"] == 2


# ==================== Tests for analyze_operations ====================


def test_analyze_operations_basic():
    """Test operation analysis"""
    code = """
def test():
    result = sum([1, 2, 3])
    return result

def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def debug():
    assert x > 0, "x must be positive"
"""
    tree = ast.parse(code)
    result = analyze_operations(tree)

    assert result["function_calls"] == 2  # sum() and ValueError()
    assert result["return_statements"] == 2
    assert result["exceptions_raised"] == 1
    assert result["assertions"] == 1


# ==================== Tests for analyze_quality ====================


def test_analyze_quality_no_issues():
    """Test quality analysis with no issues"""
    function_details = [
        {
            "name": "good_func",
            "lines": 5, 
            "arguments": 2, 
            "complexity": 3
            }
    ]
    issues = analyze_quality(function_details)
    assert len(issues) == 0


def test_analyze_quality_long_function():
    """Test long function detection"""
    function_details = [
        {
            "name": "long_func", 
            "start_line": 10, 
            "lines": 35, 
            "arguments": 2, 
            "complexity": 3
            }
    ]
    issues = analyze_quality(function_details)
    assert len(issues) == 1
    assert "long function" in issues[0]
    assert "starts at Line 10" in issues[0]


def test_analyze_quality_too_many_arguments():
    """Test too many arguments detection"""
    function_details = [
        {
            "name": "args_func",
            "start_line": 10,
            "lines": 5,
            "arguments": 6,
            "complexity": 3,
        }
    ]
    issues = analyze_quality(function_details)
    assert len(issues) == 1
    assert "too many arguments" in issues[0]


def test_analyze_quality_high_complexity():
    """Test high complexity detection"""
    function_details = [
        {
            "name": "complex_func",
            "start_line": 15,
            "lines": 5,
            "arguments": 2,
            "complexity": 12,
        }
    ]
    issues = analyze_quality(function_details)
    assert len(issues) == 1
    assert "high complexity" in issues[0]


def test_analyze_quality_multiple_issues():
    """Test detection of multiple issues in one function"""
    function_details = [
        {
            "name": "bad_func",
            "start_line": 20,
            "lines": 35,
            "arguments": 7,
            "complexity": 15,
        }
    ]
    issues = analyze_quality(function_details)
    assert len(issues) == 3


def test_display_quality_issues_with_todos_and_fixmes():
    """Test quality report displays TODO and FIXME warnings"""
    metrics = {
        "todos": 2,
        "fixmes": 1,
        "issues": [],
    }

    output = capture_output(display_quality_issues_metrics, metrics)

    assert "TODOs:  2" in output
    assert "FIXMEs: 1" in output
    assert "WARNING: 2 TODO(s) found" in output
    assert "WARNING: 1 FIXME(s) found" in output


def test_display_quality_issues_no_issues():
    """Test quality report when no issues exist"""
    metrics = {
        "todos": 0,
        "fixmes": 0,
        "issues": [],
    }

    output = capture_output(display_quality_issues_metrics, metrics)

    assert "TODOs:  0" in output
    assert "FIXMEs: 0" in output
    assert "No issues detected" in output


# ==================== Tests for calculate_health_score ====================


def test_calculate_health_score_perfect():
    """Test health score for perfect code"""
    function_details = [{"name": "good", "lines": 5, "arguments": 2, "complexity": 3}]
    score = calculate_health_score(function_details, 0, 0)
    assert score == 100


def test_calculate_health_score_with_issues():
    """Test health score deduction for various issues"""
    function_details = [{"name": "bad", "lines": 35, "arguments": 6, "complexity": 12}]
    score = calculate_health_score(function_details, 2, 1)
    assert score == 84


def test_calculate_health_score_multiple_functions():
    """Test health score with multiple functions"""
    function_details = [
        {"name": "good", "lines": 5, "arguments": 2, "complexity": 3},
        {"name": "bad", "lines": 35, "arguments": 6, "complexity": 12},
    ]
    score = calculate_health_score(function_details, 1, 0)
    assert score == 86


def test_calculate_health_score_minimum():
    """Test health score doesn't go below 0"""
    function_details = [
        {"name": "very_bad", "lines": 100, "arguments": 20, "complexity": 50}
    ]
    score = calculate_health_score(function_details, 100, 100)
    assert score == 0


# ==================== Tests for parse_python_file ====================


def test_parse_python_file_valid():
    """Test parsing valid Python code"""
    source = """
def test():
    return True
"""
    result = parse_python_file(source, Path("test.py"))
    assert result is not None
    assert isinstance(result, ast.Module)


def test_parse_python_file_invalid():
    """Test parsing invalid Python code"""
    source = """
def test()
    return True
"""
    old_stdout = sys.stdout
    temp_file = Path("temp_output.txt")
    sys.stdout = open(temp_file, 'w')
    try:
        result = parse_python_file(source, Path("test.py"))
        sys.stdout.flush()
        with open(temp_file, 'r') as f:
            output = f.read()
    finally:
        sys.stdout = old_stdout
        temp_file.unlink(missing_ok=True)
    
    assert result is None
    assert "Syntax error" in output


# ==================== Tests for analyze_file ====================


def test_analyze_file_valid(tmp_path):
    """Test file analysis with valid Python file"""
    test_file = tmp_path / "test.py"
    test_file.write_text("""import os

def hello(name):
    # Greet the user
    print(f"Hello, {name}!")
    return True

class Greeter:
    def greet(self):
        return hello("World")

# TODO: Add more features
""")

    result = analyze_file(test_file)

    assert result is not None
    assert result["file"].name == "test.py"
    assert result["functions"] == 2
    assert result["classes"] == 1
    assert result["imports"] == 1
    assert result["todos"] == 1


def test_analyze_file_syntax_error(tmp_path):
    """Test file analysis with syntax error"""
    test_file = tmp_path / "syntax_error.py"
    test_file.write_text("""def test()
    return True
""")

    old_stdout = sys.stdout
    temp_file = Path("temp_output.txt")
    sys.stdout = open(temp_file, 'w')
    try:
        result = analyze_file(test_file)
        sys.stdout.flush()
        with open(temp_file, 'r') as f:
            output = f.read()
    finally:
        sys.stdout = old_stdout
        temp_file.unlink(missing_ok=True)
    
    assert result is None
    assert "Syntax error" in output


# ==================== Tests for main function ====================


def test_main_no_arguments():
    """Test main with no arguments"""
    original_argv = sys.argv.copy()
    sys.argv = ["analyzer.py"]
    
    try:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2
    finally:
        sys.argv = original_argv


def test_main_invalid_directory():
    """Test main with invalid directory"""
    original_argv = sys.argv.copy()
    sys.argv = ["analyzer.py", "/invalid/path"]
    
    original_is_dir = Path.is_dir
    
    try:
        Path.is_dir = lambda self: False
        
        old_stdout = sys.stdout
        temp_file = Path("temp_output.txt")
        sys.stdout = open(temp_file, 'w')
        try:
            main()
            sys.stdout.flush()
            with open(temp_file, 'r') as f:
                output = f.read()
        finally:
            sys.stdout = old_stdout
            temp_file.unlink(missing_ok=True)
        
        assert "This is not a valid directory" in output
    finally:
        Path.is_dir = original_is_dir
        sys.argv = original_argv


def test_main_valid_directory(tmp_path):
    """Test main with valid directory"""
    test_file = tmp_path / "test.py"
    test_file.write_text("""def test():
    return True
""")

    original_argv = sys.argv.copy()
    sys.argv = ["analyzer.py", str(tmp_path)]
    
    try:
        old_stdout = sys.stdout
        temp_file = Path("temp_output.txt")
        sys.stdout = open(temp_file, 'w')
        try:
            main()
            sys.stdout.flush()
            with open(temp_file, 'r') as f:
                output = f.read()
        finally:
            sys.stdout = old_stdout
            temp_file.unlink(missing_ok=True)
        
        assert "Python files: 1" in output
        assert "CODEBASE HEALTH REPORT" in output
    finally:
        sys.argv = original_argv


def test_main_json_output(tmp_path):
    """Test main with JSON output enabled"""
    test_file = tmp_path / "test.py"
    test_file.write_text(
        """def test():
    return True
"""
    )

    output_file = tmp_path / "codebase_report.json"

    original_argv = sys.argv.copy()
    original_cwd = Path.cwd()
    sys.argv = ["analyzer.py", str(tmp_path), "--json"]
    
    try:
        # Change to temp directory
        os.chdir(tmp_path)
        
        main()
        
        assert output_file.exists()
        
        with open(output_file, encoding="utf-8") as f:
            report = json.load(f)
        
        assert "summary" in report
        assert "files" in report
        assert report["summary"]["python_files"] == 1
        assert report["files"][0]["file"] == "test.py"
    finally:
        sys.argv = original_argv
        os.chdir(original_cwd)


def test_main_json_custom_output(tmp_path):
    """Test main with a custom JSON output filename"""
    test_file = tmp_path / "test.py"
    test_file.write_text(
        """def test():
    return True
"""
    )

    output_file = tmp_path / "custom_report.json"

    original_argv = sys.argv.copy()
    original_cwd = Path.cwd()
    sys.argv = [
        "analyzer.py",
        str(tmp_path),
        "--json",
        "--output",
        str(output_file),
    ]

    try:
        main()

        assert output_file.exists()

        with open(output_file, encoding="utf-8") as f:
            report = json.load(f)

        assert "summary" in report
        assert "files" in report
        assert report["summary"]["python_files"] == 1
        assert report["files"][0]["file"] == "test.py"

    finally:
        sys.argv = original_argv
        os.chdir(original_cwd)


# ==================== Integration Tests ====================


def test_full_analysis_flow(tmp_path):
    """Integration test with real file"""
    test_file = tmp_path / "test.py"
    test_file.write_text("""import sys

def calculate_average(numbers):
    # Calculate average of numbers
    if not numbers:
        return 0
    
    total = sum(numbers)
    return total / len(numbers)

def complex_function(a, b, c, d, e, f):
    # This function has too many arguments
    if a > 0:
        if b > 0:
            if c > 0:
                return a + b + c + d + e + f
    return 0

# TODO: Add error handling
# FIXME: Performance issue
""")

    with open(test_file, "r") as f:
        lines = f.readlines()
        actual_line_count = len(lines)

    result = analyze_file(test_file)

    assert result is not None
    assert result["functions"] == 2
    assert result["classes"] == 0
    assert result["imports"] == 1
    assert result["todos"] == 1
    assert result["fixmes"] == 1
    assert result["total_lines"] == actual_line_count
    assert len(result["issues"]) > 0
    assert result["health_score"] < 100


# ==================== Edge Cases ====================


def test_empty_file():
    """Test analysis of empty file"""
    result = analyze_lines([])
    assert result["code_lines"] == 0
    assert result["blank_lines"] == 0
    assert result["comment_lines"] == 0


def test_file_with_only_comments():
    """Test file with only comments"""
    source = """
# This is a comment
# Another comment
# TODO: Fix this
"""
    lines = source.strip().split("\n")
    result = analyze_lines(lines)
    assert result["comment_lines"] == 3
    assert result["code_lines"] == 0
    assert result["todos"] == 1


def test_file_with_unicode_characters():
    """Test file with Unicode characters"""
    source = """
def greet():
    print("Hello Azaucifer!")
    return True
"""
    tree = ast.parse(source)
    assert tree is not None


def test_large_complexity_handling():
    """Test handling of extremely high complexity"""
    code = "def complex():\n"
    indent = "    "
    code += indent + "if x0 > 0:\n"

    for i in range(1, 20):
        indent += "    "
        code += indent + f"if x{i} > 0:\n"

    indent += "    "
    code += indent + "return True\n"

    tree = ast.parse(code)
    function = tree.body[0]
    complexity = calculate_complexity(function)
    assert complexity == 21
    assert complexity > 10


def test_duplicate_function_names():
    """Test handling of duplicate function names"""
    code = """
def test():
    return 1

def test():
    return 2
"""
    tree = ast.parse(code)
    result = analyze_functions(tree)
    assert result["functions"] == 2
    assert result["function_details"][0]["name"] == "test"
    assert result["function_details"][1]["name"] == "test"