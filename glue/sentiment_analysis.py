import pandas as pd
from textblob import TextBlob 

df = pd.read_csv('cleaned_data.csv') #change file location
cleaned_texts = list(df['cleaned_text'].values)

sentiment_objects = [TextBlob(post) for post in cleaned_texts]

sentiment_values = [[post.sentiment.polarity, str(post)] for post in sentiment_objects]

sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "cleaned_text"])

polarity =sentiment_df["polarity"]
sentiment_list = []
for p in polarity:
    if p > 0:
        sentiment_list.append('Positive')
    elif p < 0:
        sentiment_list.append('Negative')
    else:
        sentiment_list.append('Neutral')

sentiment_df['post'] = df['text']
sentiment_df['country'] = df["country"]
sentiment_df['topic'] = df["topic"]
sentiment_df['source'] = df['source']
sentiment_df['subreddit'] = df['subreddit']
sentiment_df['sentiment'] = sentiment_list


sentiment_df.to_csv('sentiment_analysis_output.csv', index = False) #change file location
