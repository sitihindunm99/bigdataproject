import requests
import os
from dotenv import load_dotenv
from json import loads, dump

def edit_columns(tweets, topic, headers):
    for tweet in tweets:
        # Insert topic key-value for each tweet and remove unrequired fields
        tweet['topic'] = topic
        del tweet['edit_history_tweet_ids']

        # Handle location of tweet if provided
        if 'geo' in tweet:
            search_url = f"https://api.twitter.com/1.1/geo/id/{tweet['geo']['place_id']}.json"
            r = requests.get(url=search_url, headers=headers)
            place_info = loads(r.text)

            try:
                tweet['country'] = place_info['country']
                tweet['place_type'] = place_info['place_type']
            except KeyError:
                continue
    return tweets

def run_etl():

    # Get the topics from topic.txt
    topics = []
    with open('./topic_live.txt') as f:
        topics = [line.rstrip() for line in f]

    # Credentials for Twitter API
    load_dotenv()
    authorization = {'Authorization': "Bearer {0}".format(os.getenv("bearer"))}
    search_url = 'https://api.twitter.com/2/tweets/search/recent'
    collated_tweets = []
    for topic in topics:
        # Customize required fields here
        query_params = {'query': topic,'tweet.fields': 'text,id','max_results': 100, 'user.fields':'location', 'expansions':'geo.place_id', 'place.fields':'contained_within,country,country_code,full_name,geo,id,name,place_type'}
        r = requests.get(url=search_url, headers=authorization, params=query_params)
        tweets = r.json()
        tweets['data'] = edit_columns(tweets=tweets['data'], topic=topic, headers=authorization)
        oldest_id = tweets['meta']['oldest_id']

        # Iterate to retrieve next 100 tweets (loop maximum of 100 times to achieve 10,000 tweets goal)
        for _ in range(100):
            query_params['until_id'] = oldest_id
            try:
                r = requests.get(url=search_url, headers=authorization, params=query_params)
                next_tweets = edit_columns(tweets=r.json()['data'], topic=topic, headers=authorization)
                tweets['data'] += next_tweets
                oldest_id = r.json()['meta']['oldest_id']
                tweets['meta']['oldest_id'] = oldest_id
            except KeyError:
                # No more tweets found for this topic
                break

        # Insert tweets into collated tweets list
        collated_tweets += tweets['data']
        print("Number of Tweets for topic {0}: ".format(topic) + str(len(tweets['data'])))

    # Write tweets to JSON file
    with open('./twitter_output.json', 'w') as f:
        dump(eval(str(collated_tweets)), f)
    print(f"Total Number of Tweets: " + str(len(collated_tweets)))

run_etl()
