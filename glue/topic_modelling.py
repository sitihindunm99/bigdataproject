import pandas as pd
import gensim
import ast
import boto3
import io

s3 = boto3.client('s3')
bucket = "is459_group5_project"

file_name = "cleaned/cleaned_data_combined.csv"
obj = s3.get_object(Bucket= bucket, Key= file_name)

df = pd.read_csv(io.BytesIO(obj['Body'].read()))
# df = pd.read_csv('cleaned_data_new.csv')
# df = pd.read_excel('cleaned_data_combined.xlsx')

def topic_modelling(pro_docs):
    cleaned_docs = []
    for row in range(len(pro_docs)): 
        # text = pro_docs[row].strip('][').split(', ')
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

    # word_split = []
    # probability_split = []
    # for topic in topics_split: 
    #     word_list = []
    #     probability_list = []
    #     for word in topic:
    #         split = word.split("*")
    #         word_list.append(split[1])
    #         probability_list.append(split[0])

    #     word_split.append(word_list)

    # word_split_df = pd.DataFrame(word_split)
    # word_split_df = word_split_df.T

    topic_split_df = pd.DataFrame(topics_split).T
    for i in range(5):
        word_prob_df = topic_split_df[i].str.split("*", n = 1, expand = True)
        topic_split_df["probability-" + str(i)]= word_prob_df[0]
        topic_split_df["word-" + str(i)]= word_prob_df[1]
    
    return topic_split_df

# #overall topics: 
# overall_docs = list(df['pro_docs'].values)
# overall_topics = topic_modelling(overall_docs)
# overall_topics.to_csv('topic_modelling_output_overall.csv')

# #elementary topics: 
# elem_df = df.loc[df['topic'] == 'elementary']
# elem_docs = list(df['pro_docs'].values)
# elem_topics = topic_modelling(elem_docs)
# elem_topics.to_csv('topic_modelling_output_elem.csv')

# #highschool topics: 
# hs_df = df.loc[df['topic'] == 'highschool']
# hs_docs = list(df['pro_docs'].values)
# hs_topics = topic_modelling(hs_docs)
# hs_topics.to_csv('topic_modelling_output_hs.csv')

# #university+college topics: 
# uni_df = df.loc[df['topic'] == 'university']
# uni_docs = list(df['pro_docs'].values)
# uni_topics = topic_modelling(uni_docs)
# uni_topics.to_csv('topic_modelling_output_uni.csv')

#overall topics: 
overall_docs = list(df['pro_docs'].values)
overall_topics = topic_modelling(overall_docs)
overall_topics.to_csv('topic_modelling_output_overall.csv')
# overall_topics.to_excel('topic_modelling_output_overall_2.xlsx')
s3.upload_file('topic_modelling_output_overall.csv',"is459_group5_project","insights/topic_modelling/overall.csv")
# overall_topics.to_csv('s3://bda-proj-bucket1-test/write/topic_modelling/overall.csv', index=False)
# 

#elementary topics: 
elem_df = df.loc[df['topic'] == 'elementary']
elem_docs = list(elem_df['pro_docs'].values)
elem_topics = topic_modelling(elem_docs)
elem_topics.to_csv('topic_modelling_output_elem.csv')
# elem_topics.to_excel('topic_modelling_output_elem_2.xlsx')
s3.upload_file('topic_modelling_output_elem.csv',"is459_group5_project","insights/topic_modelling/elementary_school.csv")
# s3.Bucket('bda-proj-bucket1-test').upload_file("write/topic_modelling/elementary_school.csv")
# elem_topics.to_csv('s3://bda-proj-bucket1-test/write/topic_modelling/elementary_school.csv', index=False)
# 

#highschool topics: 
hs_df = df.loc[df['topic'] == 'highschool']
hs_docs = list(hs_df['pro_docs'].values)
hs_topics = topic_modelling(hs_docs)
hs_topics.to_csv('topic_modelling_output_hs.csv')
# hs_topics.to_excel('topic_modelling_output_hs_2.xlsx')
s3.upload_file('topic_modelling_output_hs.csv',"is459_group5_project","insights/topic_modelling/high_school.csv")
# overall_topics.to_csv('s3://bda-proj-bucket1-test/write/topic_modelling/high_school.csv', index=False)
# 

#university+college topics: 
uni_df = df.loc[df['topic'] == 'university']
uni_docs = list(uni_df['pro_docs'].values)
uni_topics = topic_modelling(uni_docs)
uni_topics.to_csv('topic_modelling_output_uni.csv')
# uni_topics.to_excel('topic_modelling_output_uni_2.xlsx')
s3.upload_file('topic_modelling_output_uni.csv',"is459_group5_project","insights/topic_modelling/uni.csv")
# s3.Bucket('bda-proj-bucket1-test').upload_file("write/topic_modelling/university.csv")
# overall_topics.to_csv('s3://bda-proj-bucket1-test/write/topic_modelling/university.csv', index=False)
# 






