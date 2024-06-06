import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import re
def remove_stopwords(txt):
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
    'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
    'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
    'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
    's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
    'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
    'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
    "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    rx = r'\w+'
    x = [w.lower() for w in re.findall(rx, txt) if w.lower() not in stop_words]
    x = [w for w in x if w.isalpha()]
    s = ""
    for wrd in x:
        s += wrd + ' '
    return s
data = dict()

with open("data.json", 'r') as outfile:
    jsondata = json.load(outfile)
dic = dict()
for movie in jsondata:
    s = ""
    for x in jsondata[movie]["summery"]:
        s += x + ' '
    dic[jsondata[movie]["title"]] = s
plot = input("enter a new summery")
plot = remove_stopwords(plot)
dic['aim'] = plot
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
for mv in recommendations('aim'):
    print(mv)