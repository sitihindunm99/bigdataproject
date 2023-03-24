import nltk 
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import gensim

#load text
data = pd.read_csv('...')
column = data['column_name']

stop_list = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

docs1 = []
#tokenisation:
for row in data['column_name']: 
    doc = nltk.word_tokenize(data["column_name"])
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