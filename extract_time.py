"""extract import time from the output"""

import re
import sys

REGEX = re.compile(r"<import\s([\d.]+)\sseconds>")


def extract(output: str) -> float:
    """extract floating point number"""
    match = REGEX.search(output)
    return float(match.group(1)) if match else 0


if __name__ == "__main__":
    print(extract(sys.argv[1]))
