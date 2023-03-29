import io
import nltk 
import pandas as pd
import re
import gensim
import boto3

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.data.path.append("s3://hindun-is459-project/library")
nltk.download('stopwords', download_dir="s3://hindun-is459-project/library")
nltk.download('punkt', download_dir="s3://hindun-is459-project/library")
nltk.download('wordnet', download_dir="s3://hindun-is459-project/library")

s3 = boto3.client('s3')
bucket = "hindun-is459-project"

def pre_processing(column):
    stop_list = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    docs1 = []
    #tokenisation:
    for row in column: 
        doc = nltk.word_tokenize(str(row))
        docs1.append(doc)

    #noun 
    nouns = []
    pos_tag = [nltk.pos_tag(doc) for doc in docs1]
    for doc in pos_tag: 
        document = []
        for w in doc: 
            if w[1] == 'NN' or w[1] == "NNS": 
                document.append(w[0])
        nouns.append(document)
    
    #make all words in lowercase
    docs2 = [[w.lower() for w in doc] for doc in docs1]

    #remove punctuation+numbers
    docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]

    #remove stopwords 
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]

    #lemmatize
    docs5 = [[lemmatizer.lemmatize(w) for w in doc] for doc in docs4]

    docs5 = [[lemmatizer.lemmatize(w) for w in doc] for doc in docs4]

    flatten_pro_docs = [word for post in docs5 for word in post]
    word_counts = Counter(flatten_pro_docs)
    threshold = 10000
   
    common_words = [word for word, count in word_counts.most_common() if count>= threshold]

    pro_docs = [[w for w in doc if w not in common_words] for doc in docs5]
    #convert words to vectors 
    # dictionary = gensim.corpora.Dictionary(pro_docs)
    # vecs1 = [dictionary.doc2bow(doc) for doc in pro_docs]
    # tfidf = gensim.models.TfidfModel(vecs1)
    # pro_vecs = [tfidf[vec] for vec in vecs1]
    
    # return pro_vecs
    return pro_docs, docs3

def twitter():
    file_name = "raw/twitter/twitter_output_formatted.json"
    obj = s3.get_object(Bucket= bucket, Key= file_name)
    
    df_twitter = pd.read_json(io.BytesIO(obj['Body'].read()))
    column = df_twitter['text']
    
    pro_docs, cleaned_text= pre_processing(column)
    df_twitter['pro_vecs'] = pro_docs
    df_twitter['cleaned_text'] = cleaned_text

    df_twitter.drop(columns=['id', 'text', 'geo', 'place_type'], inplace=True)
    df_twitter['source'] = 'twitter'
    df_twitter['subreddit'] = 'Twitter'
    
    return df_twitter
    
def reddit():
    file_name = "raw/reddit/reddit_output.csv"
    obj = s3.get_object(Bucket= bucket, Key= file_name)
    
    df_reddit = pd.read_csv(io.BytesIO(obj['Body'].read()))
    column = df_reddit['comment']
    
    pro_docs, cleaned_text = pre_processing(column)
    df_reddit['pro_docs'] = pro_docs
    df_reddit['cleaned_text'] = cleaned_text

    
    df_reddit.drop(columns=['title', 'id', 'score', 'num_comments', 'comment', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8'], inplace=True)
    df_reddit['source'] = 'reddit'
    
    return df_reddit

df_twitter = twitter()
df_reddit = reddit()

df_combined = pd.concat([df_twitter, df_reddit], axis=0)
# final columns should be ["topic", 'country', 'source', 'subreddit', "text", 'cleaned_text', 'pro_docs']

df_combined.to_csv('s3://hindun-is459-project/cleaned/cleaned_data.csv', index=False)
