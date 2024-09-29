import json
import spacy
nlp = spacy.load("en_core_web_sm")

def handler(event, context):
    text = event["body"]
    doc = nlp(text)
    nouns = [token.lemma_ for token in doc if  token.pos_ == 'NOUN']

    response = {
        "statusCode": 200,
        "body": json.dumps(nouns)
    }

    return response

if __name__ == "__main__":
    event = {
        "body": "black cat"
    }
    print(handler(event, None))