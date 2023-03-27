import io
import nltk 
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim
from numpy import array

import boto3
nltk.data.path.append("s3://bigdataproject-testing-raw-data/library")
nltk.download('stopwords', download_dir="s3://bigdataproject-testing-raw-data/library")
nltk.download('punkt', download_dir="s3://bigdataproject-testing-raw-data/library")
nltk.download('wordnet', download_dir="s3://bigdataproject-testing-raw-data/library")

bucket = "bigdataproject-testing-raw-data"
file_name = "raw/reddit_output.csv"

s3 = boto3.client('s3') 

obj = s3.get_object(Bucket= bucket, Key= file_name) 


#load text
data = pd.read_csv(io.BytesIO(obj['Body'].read()))

column = data['comment']

stop_list = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

docs1 = []
#tokenisation:
for row in data['comment']: 
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


data.drop(columns=['title', 'id', 'score', 'num_comments', 'comment', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8'], inplace=True)
data['pro_vecs'] = pro_vecs

print(data)

data.to_csv('s3://bigdataproject-testing-raw-data/write/reddit_output_cleaned.csv', index=False)

