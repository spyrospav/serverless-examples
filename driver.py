import json
import argparse
import importlib

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Driver for running test cases for Lambda functions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Enjoy :)",
    )

    parser.add_argument("appname", help="Name of the application", type=str)

    args = parser.parse_args()

    appname = args.appname

    modname = appname + ".lambda"

    module = importlib.import_module(appname)

    handler = getattr(module, "handler")

    # open data.json file
    with open(appname + "/data.json") as f:

        data = json.load(f)

        for entry in data:
            event = entry["event"]
            context = entry["context"]
            print(handler(event, context))
