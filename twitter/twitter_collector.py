import requests
import os
from dotenv import load_dotenv

def run_etl():

    # Get the topics from topic.txt
    topics = []
    with open('topic.txt') as f:
        topics = [line.rstrip() for line in f]

    # Interact with Twitter API
    load_dotenv()
    authorization = {'Authorization': f'Bearer {os.getenv("bearer")}'}
    search_url = f'https://api.twitter.com/2/tweets/search/recent'
    for topic in topics:
        # TODO: customize what fields are required
        query_params = {'query': f'{topic}','tweet.fields': 'text,id','max_results': 100}
        r = requests.get(url=search_url, headers=authorization, params=query_params)

        # Save tweets to a JSON file
        with open(f'{topic.replace(" ", "_")}.json', 'w') as f:
            f.write(str(r.json()))

run_etl()