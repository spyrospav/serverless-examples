"""process Python files to create timed import version of it"""

import os


def find_python_files(directory: str) -> list[str]:
    """file all Python files, recursively"""
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def process_python_file(path: str):
    """process single python file, create a timed version of it"""
    new_path = os.path.splitext(path)[0] + "_timed.py"

    start_timing_stubs = ["import time\n", "IMPORT_START_TIME = time.time()\n"]
    end_timing_stubs = [
        "IMPORT_END_TIME = time.time()\n",
        'print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")',
    ]

    original_lines = []
    import_linenos = []

    with open(path, "r", encoding="utf-8") as original_file:
        for lineno, line in enumerate(original_file.readlines()):
            if line.startswith("import") or (
                line.startswith("from") and not line.startswith("from __future__")
            ):  # this line is an import
                import_linenos.append(lineno)

            original_lines.append(line)

    if len(import_linenos) != 0:
        begin_import_lineno = min(import_linenos)
        end_import_lineno = max(import_linenos)
    else:
        begin_import_lineno = (end_import_lineno := 0)

    with open(new_path, "w", encoding="utf-8") as processed_file:
        for lineno, line in enumerate(original_lines):
            if lineno == begin_import_lineno:
                processed_file.writelines(start_timing_stubs)
            processed_file.write(line)
            if lineno == end_import_lineno:
                processed_file.writelines(end_timing_stubs)


if __name__ == "__main__":
    for filename in find_python_files("./examples"):
        if not filename.endswith("_timed.py"):
            print(f"processing {filename}")
            process_python_file(filename)
