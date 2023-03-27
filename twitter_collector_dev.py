import requests
import os
from dotenv import load_dotenv
from json import loads

def edit_columns(tweets, topic, headers):
    for tweet in tweets:
        tweet['topic'] = topic
        del tweet['edit_history_tweet_ids']

        if 'geo' in tweet:
            search_url = f"https://api.twitter.com/1.1/geo/id/{tweet['geo']['place_id']}.json"
            r = requests.get(url=search_url, headers=headers)
            place_info = loads(r.text)

            try:
                tweet['country'] = place_info['country']
                tweet['place_type'] = place_info['place_type']
            except KeyError:
                print("key")

    return tweets

def run_etl():

    # Get the topics from topic.txt
    topics = []
    with open('./topic.txt') as f:
        topics = [line.rstrip() for line in f]

    # Interact with Twitter API
    load_dotenv()
    authorization = {'Authorization': f'Bearer {os.getenv("bearer")}'}
    search_url = f'https://api.twitter.com/2/tweets/search/recent'
    collated_tweets = []
    for topic in topics:
        # TODO: customize what fields are required
        query_params = {'query': f'{topic}','tweet.fields': 'text,id','max_results': 100, 'user.fields':'location', 'expansions':'geo.place_id', 'place.fields':'contained_within,country,country_code,full_name,geo,id,name,place_type'}
        r = requests.get(url=search_url, headers=authorization, params=query_params)
        tweets = r.json()
        tweets['data'] = edit_columns(tweets=tweets['data'], topic=topic, headers=authorization)

        oldest_id = tweets['meta']['oldest_id']

        for _ in range(100):
            query_params['until_id'] = oldest_id
            try:
                r = requests.get(url=search_url, headers=authorization, params=query_params)
                next_tweets = edit_columns(tweets=r.json()['data'], topic=topic, headers=authorization)
                tweets['data'] += next_tweets
                oldest_id = r.json()['meta']['oldest_id']
                tweets['meta']['oldest_id'] = oldest_id
            except KeyError:
                break

        print(f"Number of Tweets for topic {topic}: " + str(len(tweets['data'])))
        # Save tweets to a JSON file
        # with open(f'./{topic.replace(" ", "_")}.json', 'w') as f:
        #     f.write(str(tweets))
        collated_tweets += tweets['data']

    print(f"Total Number of Tweets: " + str(len(collated_tweets)))
    with open('twitter_output.json', 'w') as f:
        f.write(str(collated_tweets))
run_etl()