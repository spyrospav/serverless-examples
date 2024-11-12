import json
import argparse
import importlib.util

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Driver for running test cases for Lambda functions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Enjoy :)",
    )

    parser.add_argument("appname", help="Name of the application", type=str)
    parser.add_argument(
        "--handler",
        help="Name of the handler function",
        type=str,
        default="handler",
    )
    parser.add_argument(
        "--filename",
        "-f",
        help="Name of the main of the application",
        type=str,
        default="lambda.py",
    )
    parser.add_argument(
        "--test",
        "-t",
        help="Path to the test cases file",
        type=str,
        default="data.json",
    )

    args = parser.parse_args()

    appname = args.appname
    file_path = appname + "/" + args.filename
    module_name = "lambda"

    # Find spec from file location
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    # Load the module from the specification
    module = importlib.util.module_from_spec(spec)

    # Execute the module
    spec.loader.exec_module(module)

    handler = getattr(module, args.handler)

    # open data.json file
    with open(appname + "/data.json") as f:

        data = json.load(f)

        for entry in data["tests"]:
            event = entry["event"]
            context = entry["context"]
            print(handler(event, context))
