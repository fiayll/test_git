import requests
from bs4 import BeautifulSoup 
from time import sleep
import json
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import math
from collections import OrderedDict
from numpy.linalg import norm

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
    return x

def scraping():
    dic = {}
    header = {"User_Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    session = requests.Session()
    retry = Retry(connect = 4, backoff_factor = 0.5)
    adapter = HTTPAdapter(max_retries = retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    req = session.get("https://m.imdb.com/chart/top/", headers = header)
    main = BeautifulSoup(req.content, 'html.parser')
    for obj in main.find_all('div', {"class" : 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title'}):
        dic_in = {}
        href = obj.a['href'] 
        title = obj.h3.text
        update_title = title.split()
        href_split = href.split('/')
        dic_in["summery_url"] = 'm.imdb.com/title/' + href_split[2] + '/plotsummary'
        dic_in["title"] = " ".join(update_title[1:])
        dic[title] = dic_in
    with open("data.json", "w") as outfile:
        json.dump(dic, outfile)
    with open("data.json", 'r') as ll:
        jsondata = json.load(ll)
    for x in jsondata:
        req = session.get('http://' + jsondata[x]["summery_url"], headers = header)
        print(req.status_code)
        sleep(1)
        plot = BeautifulSoup(req.content, 'html.parser')

        words = []
        for sm in plot.find_all('div', {'data-testid' : "sub-section-summaries",'class' : 'sc-f65f65be-0 bBlII'}):
            for pl in sm.find_all('div', {'class' : 'ipc-html-content-inner-div'}):
                words += remove_stopwords(pl.text)
        jsondata[x]["summery"] = words
        with open("data.json", 'w') as outfile:
            json.dump(jsondata, outfile)

def make_matrix_tf():
    dic = dict()
    with open("data.json", 'r') as outfile:
        jsondata = json.load(outfile)
    total_count = 0
    for movie in jsondata:
        temp = dict()
        for word in jsondata[movie]["summery"]:
            if word in temp:
                temp[word] += 1
                total_count += 1
            else:
                temp[word] = 1 
                total_count += 1
        for word in temp:
            temp[word] /= total_count
        dic[movie] = temp
    data_frame = pd.DataFrame(dic)
    data_frame = data_frame.fillna(0)
    data_frame = data_frame.astype(float)
    return data_frame


def make_matrix_idf():
    tf = make_matrix_tf()
    dic = dict()
    with open("data.json", 'r') as outfile:
        jsondata = json.load(outfile)
    temp = dict()
    for word in tf.index:
        count = 0
        for mv in jsondata:
            if tf[mv][word]:
                count += 1
        temp[word] = math.log(250.0 / count, 10)
    return temp

    

def make_matrix_tf_idf():
    tf = make_matrix_tf()
    idf = make_matrix_idf()
    words = tf.index
    dic = dict()
    with open("data.json", 'r') as outfile:
        jsondata = json.load(outfile)
    for movie in jsondata:
        temp = dict()
        for word in words:
            temp[word] = tf[movie][word] * idf[word]
        dic[movie] = temp
    data_frame = pd.DataFrame(dic)
    data_frame = data_frame.fillna(0)
    data_frame = data_frame.astype(float)
    return data_frame

def vectoraziation(vec):
    return np.array(vec)

def KNN(vec):
    dic = dict()
    point1 = vec
    matrix = make_matrix_tf_idf()
    for col in matrix:
        point2 = vectoraziation(matrix[col])
        dist = np.dot(point1,point2)/(norm(point1)*norm(point2))
        dic[col] = dist
    keys = list(dic.keys())
    values = list(dic.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    out = 0
    for movie in reversed(sorted_dict):
        out += 1
        if (out <= 5):
            print(movie)
        else:
            break
def tf_idf_cal(summery):
    tfidf = []
    words = make_matrix_tf().index
    idf = make_matrix_idf()
    summery = [w for w in summery if w in words]
    total = len(summery)
    for word in words:
        tfidf.append(summery.count(word) * idf[word] / total)
    return vectoraziation(tuple(tfidf))
        

def test_git():
    print("wowwww")


def summery_input():
    summery = input("here:")
    summery = remove_stopwords(summery)
    KNN(tf_idf_cal(summery))

# scraping()
summery_input()
test_git()




