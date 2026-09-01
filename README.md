# Codebase Health Analyzer

A Python-based tool for analyzing the **health, structure, maintainability, and complexity** of Python codebases.

The analyzer uses Python's **Abstract Syntax Tree (AST)** to inspect Python source files and generate detailed codebase health reports.

## Features

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
* 🔍 Performs function-level analysis

  * Function starting line
  * Function length
  * Number of arguments
  * Cyclomatic-style complexity
* ⚠️ Detects potential code quality issues

  * Long functions
  * Functions with too many arguments
  * High-complexity functions
  * `TODO` comments
  * `FIXME` comments
* ❤️ Calculates a codebase health score
* 🏷️ Assigns a health rating

  * Excellent
  * Good
  * Needs Improvement
  * Poor
* 📄 Generates JSON reports for programmatic use
* 🧪 Includes automated tests using `pytest`
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

Display the command-line help:

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

The generated report is excluded from version control through `.gitignore`.

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

Run the test suite with:

```bash
python -m pytest test_analyzer.py
```

The project currently contains automated tests covering:

* Line analysis
* Complexity calculation
* Function analysis
* Import analysis
* Control-flow analysis
* Class detection
* Operation analysis
* Quality issue detection
* Health score calculation
* Syntax error handling
* CLI behavior
* JSON report generation

## Project Structure

```text
codebase-health-analyzer/
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
       ▼
Parse Source with AST
       │
       ├── Line Analysis
       ├── Structure Analysis
       ├── Control Flow Analysis
       ├── Operation Analysis
       └── Function Analysis
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

## Current Status

The project is actively being developed.

Current focus areas include improving codebase analysis, expanding quality checks, improving reporting, and adding more useful developer-oriented features.

## License

This project is currently intended as an open-source learning and development project.
