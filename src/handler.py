import json
import requests
from utilities.sitescraper import retrieve_articles
from utilities.constants import API_ENDPOINT_LOAD, TIMEOUT_SECONDS


def load_data(event, context):
    body = {
        'message': 'Go Serverless v1.0! Your function executed successfully!',
        'input': event
    }

    articles = retrieve_articles()

    insert(articles)

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def insert(articles):
    for article in articles:
        payload = {
            'image_url': article['image_url'],
            'title': article['title'],
            'title_link': article['title_link'],
            'category': article['category'],
            'meta_content': article['meta_content']
        }

        response = requests.post(
            API_ENDPOINT_LOAD, data=payload, timeout=TIMEOUT_SECONDS)

        if '20' in str(response.status_code):
            print('SUCCESSFULLY LOADED {}'.format(payload))
        else:
            print('FAILED TO LOAD {}'.format(payload))


if __name__ == '__main__':
    load_data(None, None)
