import io
import nltk 
import pandas as pd
import re
import gensim
import boto3
import datetime
import json

from io import BytesIO
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

bucket = "is459-group5-project"

nltk.data.path.append("s3://"+bucket+"/library")
nltk.download('stopwords', download_dir="s3://"+bucket+"/library")
nltk.download('punkt', download_dir="s3://"+bucket+"/library")
nltk.download('wordnet', download_dir="s3://"+bucket+"/library")
nltk.download('averaged_perceptron_tagger', download_dir="s3://"+bucket+"/library")

s3 = boto3.client('s3')
now = datetime.datetime.now()
timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")

def pre_processing(column):
    stop_list = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    docs1 = []
    for row in column: 
        doc = nltk.word_tokenize(str(row))
        docs1.append(doc)
    
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
    docs5 = [[lemmatizer.lemmatize(w) for w in doc] for doc in docs4]

    flatten_pro_docs = [word for post in docs5 for word in post]
    word_counts = Counter(flatten_pro_docs)
    threshold = 10000
   
    common_words = [word for word, count in word_counts.most_common() if count>= threshold]
    pro_docs = [[w for w in doc if w not in common_words] for doc in docs5]
    
    return pro_docs, docs3
    
def twitter():
    prefix = 'raw/historical/twitter/'
    ##################################################
    ## DESCRIPTION  :   Extract JSON Files in S3 
    ##################################################
    df_old = pd.DataFrame()
    
    for file in s3.list_objects_v2(Bucket=bucket, Prefix=prefix)['Contents']:
        if file['Key'].endswith('.json'):
            obj = s3.get_object(Bucket=bucket, Key=file['Key'])
            data = obj['Body'].read().decode('utf-8')
            json_data = json.loads(data)
            temp_df = pd.DataFrame(json_data)
            df_old = df_old.append(temp_df, ignore_index=True)

    ##################################################
    ## DESCRIPTION  :   Combine Historical Data and New Data
    ##################################################
    file_name = "raw/twitter/twitter_output.json"
    obj = s3.get_object(Bucket= bucket, Key= file_name)
    df_new = pd.read_json(io.BytesIO(obj['Body'].read()))
    df_twitter = pd.concat([df_old, df_new], axis=0)
    column = df_twitter['text']

    pro_docs, cleaned_text= pre_processing(column)
    
    df_twitter['pro_docs'] = pro_docs
    df_twitter['cleaned_text'] = cleaned_text
    df_twitter[['topic_chatgpt', 'topic']] = df_twitter['topic'].str.split(' ', expand=True)
    df_twitter['source'] = 'twitter'
    df_twitter['subreddit'] = 'Twitter'

    s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': file_name}, Key="raw/historical/twitter/twitter_output_" + timestamp_str + ".json")
    s3.delete_object(Bucket=bucket, Key=file_name)
    
    return df_twitter
    
def reddit():
    prefix = 'raw/historical/reddit/'
    ##################################################
    ## DESCRIPTION  :   Extract XLSX Files in S3 
    ##################################################
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    dfs = []
    
    for obj in objects['Contents']:
        if obj['Key'].endswith('.xlsx'):
            file_obj = s3.get_object(Bucket=bucket, Key=obj['Key'])['Body'].read()
            df = pd.read_excel(BytesIO(file_obj))
            dfs.append(df)
    
    df_old = pd.concat(dfs, ignore_index=True)
    
    ##################################################
    ## DESCRIPTION  :   Combine Historical Data and New Data
    ##################################################
    file_name = "raw/reddit/reddit_output.xlsx"
    obj = s3.get_object(Bucket= bucket, Key= file_name)
    
    df_new = pd.read_excel(BytesIO(file_obj))
    df_reddit = pd.concat([df_old, df_new], axis=0)
    column = df_reddit['comment']

    pro_docs, cleaned_text = pre_processing(column)
    
    df_reddit['pro_docs'] = pro_docs
    df_reddit['cleaned_text'] = cleaned_text
    df_reddit['source'] = 'reddit'

    s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': file_name}, Key="raw/historical/reddit/reddit_output_" + timestamp_str + ".json")
    s3.delete_object(Bucket=bucket, Key=file_name)
    
    return df_reddit

df_twitter = twitter()
df_reddit = reddit()

# final columns should be ['text', 'topic', 'country', 'pro_docs', 'cleaned_text', 'source', 'subreddit']
df_combined = pd.concat([df_twitter, df_reddit], axis=0)
df_combined.drop(columns=['id', 'geo', 'place_type', 'topic_chatgpt', 'title', 'score', 'num_comments', 'comment'], inplace=True)
df_combined.to_excel("s3://"+bucket+"/cleaned/cleaned_data_combined.xlsx", index=False)