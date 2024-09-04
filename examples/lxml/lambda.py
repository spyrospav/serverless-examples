import requests
from lxml import html

def handler(event, context):
    url = "https://github.com/spyrospav"
    response = requests.request("GET", url)
    tree = html.fromstring(response.content)
    # Extract the username using XPath
    username = tree.find_class("vcard-username")[0].text_content()

    # remove spaces and newlines
    username = username.strip()

    return username

if __name__ == "__main__":
    print(handler(42, 42))