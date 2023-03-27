import requests
import os
from dotenv import load_dotenv

def run_etl():

    # Get the topics from topic.txt
    topics = []
    with open('./topic.txt') as f:
        topics = [line.rstrip() for line in f]

    # Interact with Twitter API
    load_dotenv()
    authorization = {'Authorization': "Bearer {0}".format(os.getenv("bearer"))}
    search_url = 'https://api.twitter.com/2/tweets/search/recent'
    for topic in topics:
        # TODO: customize what fields are required
        query_params = {'query': topic,'tweet.fields': 'text,id','max_results': 100, 'user.fields':'location', 'expansions':'geo.place_id', 'place.fields':'contained_within,country,country_code,full_name,geo,id,name,place_type'}
        r = requests.get(url=search_url, headers=authorization, params=query_params)
        tweets = r.json()
        oldest_id = tweets['meta']['oldest_id']

        for _ in range(100):
            query_params['until_id'] = oldest_id
            try:
                r = requests.get(url=search_url, headers=authorization, params=query_params)
                tweets['data'] += (r.json()['data'])
                oldest_id = r.json()['meta']['oldest_id']
                tweets['meta']['oldest_id'] = oldest_id
            except KeyError:
                break

        print("Number of Tweets for topic {0}: ".format(topic) + str(len(tweets['data'])))
        # Save tweets to a JSON file
        with open("./{0}.json".format(topic.replace(" ", "_")), 'w') as f:
            f.write(str(tweets))

run_etl()
