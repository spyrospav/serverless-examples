import time
IMPORT_START_TIME = time.time()
import requests
from lxml import html
IMPORT_END_TIME = time.time()
print(f"<import {IMPORT_END_TIME - IMPORT_START_TIME} seconds>")
def handler(event, context):
    # TODO - change this URL to a frozen X account
    url = "https://twitter.com/realDonaldTrump"
    response = requests.request("GET", url)
    tree = html.fromstring(response.content)
    vecTweets = tree.xpath('//div[@class="js-tweet-text-container"]//p')	
    return vecTweets[0].text_content()