import os
import pandas as pd
import requests
import json
import tweepy

#path to the folder containing the files
folder_path = "chatgpt_twitter"
df_all_tweets = pd.DataFrame()

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), "r") as file:
            json_file = file.read()

        python_dict = eval(json_file)
        df_tweets = pd.DataFrame.from_dict(python_dict["data"])
        df_all_tweets = df_all_tweets.append(df_tweets)

bearer_token = "AAAAAAAAAAAAAAAAAAAAALt9lwEAAAAAPcZJrcfVS4QcaCdBv3exnL2iUxA%3D931InlrzGIdynkgxaDMUuFl7PyAMsLKdYbTEv7t3XjJGzfBdrx"
headers = {"Authorization": f"Bearer {bearer_token}"}

for i, row in df_tweets.iterrows():
    if pd.notna(row['geo']):
        place_id = row['geo']['place_id']
        endpoint = f"https://api.twitter.com/1.1/geo/id/{place_id}.json"
        response = requests.get(endpoint, headers=headers)
        place_info = json.loads(response.text)

        df_tweets.at[i, 'country'] = place_info['country']
        df_tweets.at[i, 'place_type'] = place_info['place_type']

# consumer_key = "Uj4K3tFqRHMJvYOoM3v2x2mnN"
# consumer_secret = "7y2IunfzveZzX7ByHIzL1LEx6HQqhvw8W8BPmgmgQY5gwLRIAl"
# access_token = "584368235-FhqbD6nl6QDSR9NYhzeaHMglYA3YLF0PHgTlCn83"
# access_token_secret = "QVrKNZeLcXBTxkVqEGlvoqPpZg7tWD4agmZSCE7Or5mC2"

# auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
# api = tweepy.API(auth)

# for i, row in df_all_tweets.iterrows():
#     if pd.notna(row['geo']):
#         place_id = row['geo']['place_id']
#         endpoint = f"/geo/id/{place_id}.json"
#         try:
#             response = api.request('GET', endpoint)
#             place_info = json.loads(response.text)
#             print(place_info)
#             df_tweets.at[i, 'country'] = place_info['country']
#             df_tweets.at[i, 'place_type'] = place_info['place_type']
#         except tweepy.errors.NotFound:
#             print(f"Error: Place ID {place_id} not found")
#             continue

df_all_tweets.to_csv("all_tweets.csv", index=False)