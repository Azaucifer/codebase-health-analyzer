from pathlib import Path
import sys


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
        lines = f.readlines()
        blank_lines = 0
        comment_lines = 0

        for line in lines:
            checked_line = line.strip()
            if checked_line == "":
                blank_lines += 1
            if checked_line.startswith("#"):
                comment_lines += 1

        code_lines = len(lines) - blank_lines - comment_lines

        return {
            "file": file,
            "total_lines": len(lines),
            "blank_lines": blank_lines,
            "comment_lines": comment_lines,
            "code_lines": code_lines,
        }


if __name__ == "__main__":
    main()
