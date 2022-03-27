# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity


dt=pd.read_csv("Fichier de base/Hotels.csv", sep=";")

df=dt.drop(["Language_Spoken","Near_Attractions","Near_Restaurants","Walking_Grade","Value_Rating","Service_Rating","Cleanliness_Rating","Location_Rating","Number_Rating","Rating","Mail","Hotel_Style","Number_of_Rooms","Description","Website","Phone","Adress","Rank","Price_night","Name","ID"], axis=1)



cosine_sim=cosine_similarity(df)



indices = pd.Series(dt.ID.values,index=dt["Name"])

def content_recommender(Name, cosine_sim=cosine_sim, hotel=dt, indices=indices):
    idx=indices[Name]
    sim_scores= list(enumerate(cosine_sim[idx]))
    sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
    sim_scores=sim_scores[1:11]
    hotel_indices=[i[0] for i in sim_scores]
    return hotel['Name'].iloc[hotel_indices]


x="The Peninsula Paris"
list_recom=content_recommender(x)

print("Hotel recommandé pour : "+x)
print(list_recom)
