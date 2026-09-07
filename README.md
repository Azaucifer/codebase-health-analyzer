# Codebase Health Analyzer

A Python-based static analysis tool for evaluating the **health, structure, maintainability, and complexity** of Python codebases.

The analyzer uses Python's **Abstract Syntax Tree (AST)** to inspect source files, identify potential code-quality issues, detect duplicated functions, and generate codebase health reports.

## Features

### Code Analysis

* 📁 Recursively scans Python files in a directory
* 📊 Calculates line-level metrics

  * Total lines
  * Code lines
  * Blank lines
  * Comment lines
* 🧩 Analyzes code structure

  * Functions
  * Classes
  * Imports
  * From imports
* 🔀 Analyzes control flow

  * `if` statements
  * `for` loops
  * `while` loops
  * `try` blocks
* ⚙️ Analyzes operations

  * Function calls
  * Return statements
  * Raised exceptions
  * Assertions

### Function Analysis

* 🔍 Function starting line
* 📏 Function length
* 🔢 Number of arguments
* 🧠 Cyclomatic-style complexity
* 🔁 Structural duplicate-function detection using AST normalization

### Code Quality

* ⚠️ Detects long functions
* ⚠️ Detects functions with too many arguments
* ⚠️ Detects high-complexity functions
* 📝 Detects `TODO` comments
* 📝 Detects `FIXME` comments
* ❤️ Calculates a codebase health score
* 🏷️ Assigns a health rating:

  * Excellent
  * Good
  * Needs Improvement
  * Poor

### Reporting

* 🖥️ Detailed terminal reports
* 📄 Machine-readable JSON reports
* 🔁 Duplicate-code reporting in terminal and JSON output

### Reliability

* 🧪 Automated test suite using `pytest`
* ⚙️ Continuous integration using GitHub Actions
* 🛡️ Handles Python files containing syntax errors without stopping the entire analysis

## Requirements

* Python 3.10+
* `pytest` for running tests

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Analyze a Python codebase:

```bash
python analyzer.py C:/path/to/project
```

Display command-line help:

```bash
python analyzer.py --help
```

Generate a JSON report:

```bash
python analyzer.py C:/path/to/project --json
```

The JSON report is saved as:

```text
codebase_report.json
```

Generated reports are excluded from version control through `.gitignore`.

## Example Output

```text
==================================================
CODEBASE HEALTH REPORT
==================================================

File: example.py

Lines
--------------------
Total lines:   120
Code lines:    85
Blank lines:   25
Comment lines: 10

Structure
--------------------
Functions:     8
Classes:       2
Imports:       5
From imports:  2

Control Flow
--------------------
If statements: 12
For loops:     4
While loops:   1
Try blocks:    2

Function Analysis
--------------------
process_data
  Start Line:        24
  Lines:             38
  Arguments:         6
  Complexity:        12

Quality Issues
--------------------
TODOs:  2
FIXMEs: 1

WARNING: process_data (Line 24): long function
WARNING: process_data (Line 24): too many arguments
WARNING: process_data (Line 24): high complexity (12)

Health Score
--------------------
Score: 72/100
Rating: Needs Improvement
```

### Duplicate Code

The analyzer also identifies structurally identical functions.

For example:

```text
Duplicate Code
--------------------

Duplicate groups: 1

Group 1
  add() - one.py:1
  calculate() - two.py:1
```

Functions can be detected as duplicates even when their function names and argument names differ, provided their underlying AST structure is equivalent.

## JSON Output

Using the `--json` option produces a machine-readable report that can be used by other tools or future automation.

Example structure:

```json
{
  "summary": {
    "python_files": 4,
    "total_lines": 1590,
    "total_functions": 94,
    "total_classes": 0,
    "total_todos": 10,
    "total_fixmes": 7,
    "average_health_score": 87.5,
    "rating": "Good"
  },
  "duplicates": [
    {
      "functions": [
        {
          "file": "one.py",
          "name": "add",
          "start_line": 1
        },
        {
          "file": "two.py",
          "name": "calculate",
          "start_line": 1
        }
      ]
    }
  ],
  "files": [
    {
      "file": "analyzer.py",
      "total_lines": 446,
      "functions": 24,
      "classes": 0,
      "health_score": 84
    }
  ]
}
```

## Testing

Run the complete test suite with:

```bash
python -m pytest test_analyzer.py
```

The test suite currently contains **61 tests** covering:

* Line analysis
* Complexity calculation
* Function analysis
* Import analysis
* Control-flow analysis
* Class detection
* Operation analysis
* Quality issue detection
* Health score calculation
* Duplicate-function detection
* Duplicate detection with syntax errors
* CLI behavior
* JSON report generation
* JSON duplicate-report integration
* Syntax error handling

GitHub Actions also runs the test suite across supported Python versions.

## Project Structure

```text
codebase-health-analyzer/
│
├── analysis/
│   ├── __init__.py
│   ├── ast_analysis.py
│   ├── complexity.py
│   ├── duplicate_detection.py
│   ├── file_analysis.py
│   ├── lines.py
│   └── quality.py
│
├── cli/
│   ├── __init__.py
│   └── arguments.py
│
├── reporting/
│   ├── json_report.py
│   └── terminal.py
│
├── analyzer.py
├── test_analyzer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

The analyzer follows several stages:

```text
Python Codebase
       │
       ▼
Find Python Files
       │
       ├─────────────────────┐
       ▼                     ▼
Parse Source with AST    Analyze Lines
       │
       ├── Structure Analysis
       ├── Control Flow Analysis
       ├── Operation Analysis
       ├── Function Analysis
       └── Duplicate Detection
       │
       ▼
Quality Analysis
       │
       ▼
Health Score
       │
       ├── Terminal Report
       └── JSON Report
```

## Architecture

The project separates analysis, command-line handling, and reporting into dedicated modules:

```text
analyzer.py
    │
    ├── cli/
    │   └── arguments.py
    │
    ├── analysis/
    │   ├── file_analysis.py
    │   ├── lines.py
    │   ├── ast_analysis.py
    │   ├── complexity.py
    │   ├── quality.py
    │   └── duplicate_detection.py
    │
    └── reporting/
        ├── terminal.py
        └── json_report.py
```

This separation keeps individual responsibilities isolated and makes the analyzer easier to test, maintain, and extend.

## Open Source

Contributions are welcome.

If you would like to contribute, please open an issue to discuss significant changes before starting work. Small bug fixes, tests, documentation improvements, and focused feature contributions are welcome.

## Current Status

The project is actively being developed.

Current capabilities include:

* Python source-code analysis using AST
* Code and structural metrics
* Function complexity analysis
* Code-quality checks
* Health scoring
* Duplicate-function detection
* Terminal reporting
* JSON reporting
* Automated testing
* Continuous integration with GitHub Actions

Development will focus on improvements that provide meaningful value to developers while keeping the analyzer focused and maintainable.

## License

This project is currently intended as an open-source learning and development project.
