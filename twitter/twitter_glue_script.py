import io
import nltk 
import pandas as pd
import re
import gensim
import boto3

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.data.path.append("s3://hindun-is459-project/library")
nltk.download('stopwords', download_dir="s3://hindun-is459-project/library")
nltk.download('punkt', download_dir="s3://hindun-is459-project/library")
nltk.download('wordnet', download_dir="s3://hindun-is459-project/library")

bucket = "hindun-is459-project"
file_name = "read/twitter/all_tweets.csv"

s3 = boto3.client('s3') 

obj = s3.get_object(Bucket= bucket, Key= file_name) 

#load text
data = pd.read_csv(io.BytesIO(obj['Body'].read()))

column = data['text']

stop_list = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

docs1 = []
#tokenisation:
for row in data['text']: 
    doc = nltk.word_tokenize(str(row))
    docs1.append(doc)

#make all words in lowercase
docs2 = [[w.lower() for w in doc] for doc in docs1]

#remove punctuation+numbers
docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]

#remove stopwords 
docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]

#lemmatize
pro_docs = [[lemmatizer.lemmatize(w) for w in doc] for doc in docs4]

#convert words to vectors 
dictionary = gensim.corpora.Dictionary(pro_docs)
vecs1 = [dictionary.doc2bow(doc) for doc in pro_docs]
tfidf = gensim.models.TfidfModel(vecs1)
pro_vecs = [tfidf[vec] for vec in vecs1]

data.drop(columns=['id', 'edit_history_tweet_ids', 'geo', 'place_type', 'withheld'], inplace=True)
data['pro_vecs'] = pro_vecs
data['source'] = 'twitter'

data.to_csv('s3://hindun-is459-project/write/twitter_output_cleaned.csv', index=False)