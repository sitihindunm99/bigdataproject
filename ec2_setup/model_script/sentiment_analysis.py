import pandas as pd
from textblob import TextBlob 
import boto3
import io

# df = pd.read_csv('cleaned_data.csv')
s3 = boto3.client('s3')
bucket = "is459_group5_project"

file_name = "cleaned/cleaned_data_combined.csv"
obj = s3.get_object(Bucket= bucket, Key= file_name)

df = pd.read_csv(io.BytesIO(obj['Body'].read()))
# df = pd.read_csv('cleaned_data_new.csv') #change file location
# df = pd.read_excel('cleaned_data_combined.xlsx')
print('read file')
cleaned_texts = list(df["cleaned_text"].values)

sentiment_objects = [TextBlob(post) for post in cleaned_texts]
print('textblob')

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

print('sentiment list')
# sentiment_df['post'] = df['text']
sentiment_df['country'] = df["country"]
sentiment_df['topic'] = df["topic"]
sentiment_df['source'] = df['source']
sentiment_df['subreddit'] = df['subreddit']
sentiment_df['sentiment'] = sentiment_list

sentiment_df.to_csv('sentiment_analysis_output.csv', index = False)
# sentiment_df.to_excel('sentiment_analysis_output.xlsx', index = False)
print('sentiment output csv created')

s3.upload_file('sentiment_analysis_output.csv',"is459_group5_project","insights/sentiment_analysis/sentiment_analysis_output.csv")
# print('pushed to bucket')

