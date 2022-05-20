from flask import Flask,render_template,request, url_for, redirect, render_template
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
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

import difflib
import ast
import json

import numpy as np
  


app = Flask(__name__)

dt=pd.read_csv("../Fichier de base/Matrice_Rating.csv", sep=";")
reader=Reader(rating_scale=(1,5))
dt=dt[0:25000]

metadata=Dataset.load_from_df(dt[['Id_user','Id_hotel','Note']],reader)

trainset = metadata.build_full_trainset()

model=KNNBasic(k=10,sim_options={'user_based':True})
model.fit(trainset)

@app.route('/')
def index():

    return render_template('index.html',titre="Bienvenue")



@app.route('/Register', methods=['GET', 'POST'])
def Register():
    return render_template('Register.html')

@app.route('/SignIn', methods=['GET', 'POST'])
def SignIn():
    return render_template('SignIn.html')

@app.route('/SignInWrong', methods=['GET', 'POST'])
def SignInWrong():
    return render_template('SignInWrong.html')


@app.route('/PageAccueil', methods=['GET', 'POST'])
def PageAccueil():
    return render_template('PageAccueil.html',mode=0)
        
@app.route('/verif', methods=['GET', 'POST'])
def verif():
    if(request.form.get('Login')=='louis.laurent@esme.fr'):

        if(request.form.get('Mdp')=="esme"):
            return redirect(url_for('PageAccueil'))
        else:
            return redirect(url_for('SignInWrong'))
    else:
        return redirect(url_for('SignInWrong'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/form_envoi', methods=['GET', 'POST'])
def form_envoi():
    dt=pd.read_csv("../Fichier de base/Hotels_without_none.csv", sep=";")
    df=dt[["Price_night","Air_conditioning","Breakfast","Wifi","Taxi","Suites","Dry_cleaning","Concierge","Safe","Room_service","Breakfast_in_the_room","Soundproof_rooms"]]
    newHotelList=[(request.args.get('Price_night'),request.args.get('Air_conditioning'),request.args.get('Breakfast'),request.args.get('Wifi'),request.args.get('Taxi'),request.args.get('Suites'),request.args.get('Dry_cleaning'),request.args.get('Concierge'),request.args.get('Safe'),request.args.get('Room_service'),request.args.get('Breakfast_in_the_room'),request.args.get('Soundproof_rooms'))]
    
    for i in range(0,len(df)):
        p=df.iloc[i]['Price_night']
        p=str(p)
        p=p.replace(",",".")
        p=(float(p))
        df.at[i,'Price_night']=p
        
    dfNew=pd.DataFrame(newHotelList, columns = ["Price_night","Air_conditioning","Breakfast","Wifi","Taxi","Suites","Dry_cleaning","Concierge","Safe","Room_service","Breakfast_in_the_room","Soundproof_rooms"])
    df=df.append(dfNew,ignore_index=True)
    cosine_sim=cosine_similarity(df)
    indices = pd.Series(dt.ID.values,index=dt["Name"])
    d={"NewHotel":1111}
    s1 = pd.Series(data=d,index=["NewHotel"])
    indices=indices.append(s1)

    def content_recommender(Name, cosine_sim=cosine_sim, hotel=dt, indices=indices):
        idx=indices[Name]
        sim_scores= list(enumerate(cosine_sim[idx]))
        sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
        sim_scores=sim_scores[1:11]
        hotel_indices=[i[0] for i in sim_scores]
        if(1111 in hotel_indices):
            hotel_indices.remove(1111)
        return hotel['Name'].iloc[hotel_indices]
  
    list_recom=content_recommender("NewHotel")
    if(len(list_recom)==0):
        return render_template('like_search.html',mode=1)
    else:
        return render_template('like.html',recommendation=list_recom,hotel="your criterias")



@app.route('/form_creer', methods=['GET', 'POST'])
def form_creer():
    name=request.args.get('Nom')
    liste_like=[]
    liste_like_rename=[]
    
    liste_reco_ID=[]
    liste_reco_name=[]
    
    liste_like.append(request.args.get('Hotel1'))
    liste_like.append(request.args.get('Hotel2'))
    
    liste_like_id=[]
    
    dz=pd.read_csv("../Fichier de base/Hotels_without_none.csv", sep=";")
    
    existing_titles=dz["Name"].unique()
  
    
    for i in range(2):
        closest_titles = difflib.get_close_matches(liste_like[i], existing_titles)
        liste_like_rename.append(closest_titles[0])
        x=dz.loc[dz['Name']==closest_titles[0]]
        liste_like_id.append(x["ID"].values[0])

    
    def generate_recommendation(hotel_IDS, model, dt, thresh=5):
        
        for hotel_ID in hotel_IDS:
            rating = model.predict(uid=999999, iid=hotel_ID)
            if rating.est == thresh:
                liste_reco_ID.append(hotel_ID)
                
        for i in liste_reco_ID:
            x=dt.loc[dt['Id_hotel'] == i,['Hotel']]
            res=x["Hotel"].iloc[0]
            liste_reco_name.append(res)
        
        return liste_reco_name[0:5]
    
    reco=generate_recommendation(liste_like_id,model,dt)
    return render_template('recherche_filtrage_1.html',recommendation=reco,choice=liste_like_rename,user=name)



@app.route('/like_search', methods=['GET', 'POST'])
def like_search():
    return render_template('like_search.html',mode=0)


@app.route('/like', methods=['GET', 'POST'])
def like():
    
    dt=pd.read_csv("../Fichier de base/Hotels.csv", sep=";")
    df=dt.drop(["Language_Spoken","Near_Attractions","Near_Restaurants","Walking_Grade","Value_Rating","Service_Rating","Cleanliness_Rating","Location_Rating","Number_Rating","Rating","Mail","Hotel_Style","Number_of_Rooms","Description","Website","Phone","Adress","Rank","Price_night","Name","ID"], axis=1)



    cosine_sim=cosine_similarity(df)



    indices = pd.Series(dt.ID.values,index=dt["Name"])

    def content_recommender(Name, cosine_sim=cosine_sim, hotel=dt, indices=indices):
        try:
            result={}
            idx=indices[Name]
            sim_scores= list(enumerate(cosine_sim[idx]))
            sim_scores= sorted(sim_scores, key=lambda x : x[1], reverse=True)
            
            sim_scores=sim_scores[1:11]
            hotel_indices=[i[0] for i in sim_scores]
            sim=[i[1] for i in sim_scores]
            
            for i in range(len(hotel_indices)):
                result[hotel['Name'].iloc[hotel_indices[i]]]=round(round(sim[i],4)*100,2)
            return result
        except:
            return []

    
    
    x=request.args.get('hotel')
    list_recom=content_recommender(x)
    if(len(list_recom)==0):
        existing_titles=dt["Name"].unique()
        closest_titles = difflib.get_close_matches(x, existing_titles)
        if(len(closest_titles)==0):
            return render_template('like_search.html',mode=1)
     
        list_recom=content_recommender(closest_titles[0]).items()
        return render_template('like.html',recommendation=list_recom,hotel=closest_titles[0])
    else:
        return render_template('like.html',recommendation=list_recom.items(),hotel=x)


@app.route('/filtrage', methods=['GET', 'POST'])
def filtrage():
    return render_template('filtrage.html')
    
@app.route('/create_new', methods=['GET', 'POST'])
def create_new():
    return render_template('create_new.html')
    





@app.route('/recherche_filtrage', methods=['GET', 'POST'])
def recherche_filtrage():
    
    
    def generate_recommendation(user_id, model, dt, thresh=5):
        
        liste_reco_ID=[]
        liste_reco_name=[]
        
        y=dt.loc[dt['Id_user']==user_id,['Id_hotel']]
        y=y['Id_hotel'].values
        

        for i in y :
            dt=dt[dt["Id_hotel"]!=i]
            
            
        hotel_IDS = dt['Id_hotel'].unique()
    
        
        for hotel_ID in hotel_IDS:
            rating = model.predict(uid=user_id, iid=hotel_ID)
            if rating.est == thresh:
                liste_reco_ID.append(hotel_ID)
                
        for i in liste_reco_ID:
            x=dt.loc[dt['Id_hotel'] == i,['Hotel']]
            res=x["Hotel"].iloc[0]
            liste_reco_name.append(res)
        
        return liste_reco_name[0:5]
    
    y=dt.loc[dt['Id_user']==int(request.args.get('UserID')),['Hotel']]
    choice=y.values
    
    choice=np.unique(choice)
    print(choice)
    return render_template('recherche_filtrage_1.html',recommendation=generate_recommendation(int(request.args.get('UserID')),model,dt),choice=choice,user=request.args.get('Name'))

app.run(debug=False)
