from pathlib import Path
import sys


def main():
    if len(sys.argv) == 1:
        print("Usage: python analyzer.py C:/Users/name/folder")

    elif len(sys.argv) == 2:
        print(sys.argv[1])
        p = Path(sys.argv[1])
        if p.is_dir():
            print("This is a valid directory")
            py_files = list(p.rglob("*.py"))
            print(f"Python files: {len(py_files)}")
        else:
            print("This is not a valid directory")


if __name__ == "__main__":
    main()
