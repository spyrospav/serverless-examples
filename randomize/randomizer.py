"""generating randomized test for debloater"""

import argparse
import importlib
import random

parser = argparse.ArgumentParser()

parser.add_argument("packages", type=str, nargs="*", help="imported packages")

# output option
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="test.py",
    help="output filename for the test file",
)

parser.add_argument(
    "-n", type=int, help="number of attributes accessed for each module", required=True
)

if __name__ == "__main__":
    args = parser.parse_args()

    num_attributes: int = args.n
    packages: list[str] = args.packages
    output: str = args.output

    with open(output, "w", encoding="utf-8") as output_file:
        print("# import section", file=output_file)
        for p in packages:
            print(f"import {p}", file=output_file)

        for p in packages:
            print(f'generating access for module "{p}"')
            module = importlib.import_module(p)
            attributes = random.choices(dir(module), k=num_attributes)

            print(f"\n# access {p}", file=output_file)
            for attr in attributes:
                print(f'getattr({p}, "{attr}")', file=output_file)

        print("\n# success", file=output_file)
        print('print("SUCCESS")', file=output_file)
