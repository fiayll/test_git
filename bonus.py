import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
data = dict()

with open("data.json", 'r') as outfile:
    jsondata = json.load(outfile)
dic = dict()
for movie in jsondata:
    s = ""
    for x in jsondata[movie]["summery"]:
        s += x + ' '
    dic[jsondata[movie]["title"]] = s
data["plot"] = dic
ldata = pd.DataFrame(data)
print(ldata.head())
tfidfvec = TfidfVectorizer() 
tfidf_movieid = tfidfvec.fit_transform((ldata["plot"])) 
cos_sim = cosine_similarity(tfidf_movieid, tfidf_movieid) 
print(tfidf_movieid)

indices = pd.Series(ldata.index) 
  
def recommendations(title, cosine_sim = cos_sim): 
    recommended_movies = [] 
    index = indices[indices == title].index[0] 
    similarity_scores = pd.Series(cosine_sim[index]).sort_values(ascending = False) 
    top_5_movies = list(similarity_scores.iloc[1:6].index) 
    for i in top_5_movies: 
        recommended_movies.append(list(ldata.index)[i]) 
    return recommended_movies 

print(recommendations("The Dark Knight") )