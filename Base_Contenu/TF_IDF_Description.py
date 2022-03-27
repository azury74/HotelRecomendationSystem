# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity



dt=pd.read_csv("Hotels.csv", sep=";")
dt=dt.drop_duplicates(subset=['Name'])


tfidf = TfidfVectorizer(stop_words='english')
x=dt["Description"]
y=dt["ID"]
z=dt["Name"]

x=x.replace("None",None)
x=x.dropna()


tfidf_matrix = tfidf.fit_transform(x)


cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
cosine_sime= cosine_similarity(tfidf_matrix,tfidf_matrix)
cosine_sim1=cosine_sim[:,0:3]
cosine_sim2=cosine_sime[:,0:3]


indices = pd.Series(dt.ID.values,index=dt["Name"])

def content_recommender(Name, cosine_sim=cosine_sim, hotel=dt, indices=indices):
    idx=indices[Name]
    sim_scores= list(enumerate(cosine_sim[idx]))
    sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
    sim_scores=sim_scores[1:11]
    hotel_indices=[i[0] for i in sim_scores]
    return hotel['Name'].iloc[hotel_indices]


x="Hotel Edouard 7"
list_recom=content_recommender(x)

print("Hotel recommandé pour : "+x)
print(list_recom)
