import pandas as pd 
from surprise import SVD
from surprise import accuracy
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader
from surprise import NormalPredictor
from surprise.model_selection import GridSearchCV
from collections import defaultdict

from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Reader,Dataset,KNNBasic,KNNWithMeans,KNNBaseline,KNNWithZScore


import ast
import json


dt=pd.read_csv("Fichier de base/Matrice_Rating.csv", sep=";")

def selet_top(predictions, n):
    # First map the predictions to each user.
    top_r = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_r[uid].append((iid, est))
        err=abs(est - true_r)
    #print(err)

 # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_r.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_r[uid] = user_ratings[:n]
    
    return top_r

reader=Reader(rating_scale=(1,5))
Data1=Dataset.load_from_df(dt[['Id_hotel','Id_user','Note']],reader)
trainset,testset = train_test_split(Data1,test_size=0.3,random_state=10)
models=[KNNBasic,KNNWithMeans,KNNBaseline,KNNWithZScore]
mesure=['cosine','pearson']

list_k=[10,20,30,40]

dfObj=pd.DataFrame(columns=['model','mesure','k','resman','value'])

for i in range(0,4):
    print('-----------------------')
    print("Modèle utilisé : ",models[i])
    for j in range(0,1):
   
        for k in list_k:
            print('Valeur de K testé : ',k)
            algo=models[i](k=k,sim_options={'name':mesure[j],'user_based':True})
            algo.fit(trainset)
            test_pred=algo.test(testset)
            valeur=accuracy.rmse(test_pred,verbose=True)
            print('-----------------------')
            top_r=selet_top(test_pred,n=5)
            
            dfObj=dfObj.append({'model':models[i],'measure':mesure[j],'k':k,'resman':valeur,'value':top_r},ignore_index=True)

dfObj.sort_values(by='resman',inplace=True)
resu=dfObj.iloc[0,dfObj.columns.get_loc('value')]



for uid,user_ratings in resu.items():
    print(uid,[iid for (iid, _) in user_ratings])
    