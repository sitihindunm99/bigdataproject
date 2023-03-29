import pandas as pd
import gensim
import ast

df = pd.read_csv('cleaned_data.csv') #change file location


def topic_modelling(pro_docs):
    cleaned_docs = []
    for row in range(len(pro_docs)): 
        if pro_docs[row] != []: 
            text = ast.literal_eval(pro_docs[row])
            cleaned_docs.append(text)

    dictionary = gensim.corpora.Dictionary(cleaned_docs)
    vecs1 = [dictionary.doc2bow(doc) for doc in cleaned_docs]
    tfidf = gensim.models.TfidfModel(vecs1)
    reviews_vecs = [tfidf[vec] for vec in vecs1]

    reviews_lda = gensim.models.ldamodel.LdaModel(corpus=reviews_vecs, id2word=dictionary, num_topics=5)
    topics = reviews_lda.show_topics(5, 20)

    topics_split = []
    for topic in range(0,5):
        split = topics[topic][1].split(" + ")
        topics_split.append(split)

    topic_split_df = pd.DataFrame(topics_split).T
    for i in range(5):
        word_prob_df = topic_split_df[i].str.split("*", n = 1, expand = True)
        topic_split_df["probability-" + str(i)]= word_prob_df[0]
        topic_split_df["word-" + str(i)]= word_prob_df[1]
    
    return topic_split_df

#overall topics: 
overall_docs = list(df['pro_docs'].values)
overall_topics = topic_modelling(overall_docs)
overall_topics.to_csv('topic_modelling_output_overall.csv') #change file location 

#elementary topics: 
elem_df = df.loc[df['topic'] == 'elementary']
elem_docs = list(df['pro_docs'].values)
elem_topics = topic_modelling(elem_docs)
elem_topics.to_csv('topic_modelling_output_elem.csv')#change file location 

#highschool topics: 
hs_df = df.loc[df['topic'] == 'highschool']
hs_docs = list(df['pro_docs'].values)
hs_topics = topic_modelling(hs_docs)
hs_topics.to_csv('topic_modelling_output_hs.csv')#change file location 

#university+college topics: 
uni_df = df.loc[df['topic'] == 'highschool']
uni_docs = list(df['pro_docs'].values)
uni_topics = topic_modelling(uni_docs)
uni_topics.to_csv('topic_modelling_output_uni.csv')#change file location 







