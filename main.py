import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import json
import re
import os
import math
from collections import OrderedDict
from numpy.linalg import norm

# import requests_html
# header = {"User_Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
# s = requests.Session()
# movies = requests.get("https://m.imdb.com/chart/top/", headers = header)
# print(movies.content)
# filename = "Ht.txt"
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
rx = "\w+"
name_list = []
# soup = BeautifulSoup(movies.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib 
# print(soup.prettify())
# s.get() 
# option = webdriver.ChromeOptions() 
# option.headless = True
# for row in soup.find_all('a', {'class':'ipc-title-link-wrapper'}):
	# if row.h3.text[0] not in ['0','1', '2', '3', '4', '5','6','7','8','9']:
		# continue
# 	if int(row.h3.text[1]) < 5 and int(row.h3.text[0]) == 1:
# 		continue

# 	# print(row)
	# temp = row['href']
	# name = row.h3.text
	# file_size = os.path.getsize(f'plot summary/{name}.txt')
	# with open(f'plot summary/titles.txt', 'a+') as file:
		# file.write(name + '\n')

	# name_list.append(name)
	# continue
	# continue

# 	if os.path.exists(f'plot summary/{name}.txt'):
# 		continue
# 	# print(type(row['href']))
# 	# print (temp)
# 	# if row.h3.text[0] in ['1', '2', '3', '4', '5','6','7','8','9']:
# 		# print(row.h3.text)
	# sub = temp[0:17]
	# if sub[len(sub) - 1] != '/':
	# 	sub = sub + '/'
	# movie = requests.get('https://m.imdb.com' + sub + 'plotsummary/', headers = header)
# 	# print('https://m.imdb.com' + temp[0:17] + 'plotsummary/')
	# movie = requests.get('https://m.imdb.com/title/tt23849204/plotsummary/', headers = header)

	# response = BeautifulSoup(movie.content, 'html.parser')
# 	# print(response.prettify())	
# 	# summary = requests.get('https://m.imdb.com' + '/title/tt0111161/plotsummary?ref_=tt_stry_pl', headers = header)
# 	# x = BeautifulSoup(summary.content, 'html.parser')
# 	# print(x.prettify())
# 	# break
# 	# sl = BeautifulSoup(movie.content, 'html.parser')
# 	# print(sl.prettify())
# 	# print('https://m.imdb.com' + row['href'] + '/js')
# 	# s = HTMLSession()
# 	# r = s.get('https://m.imdb.com' + row['href'] + '/js')
# 	# r.html.render(sleep = 1)
# 	# print(r.text)
# 	# browser = webdriver.Chrome()
# 	# browser.get('https://m.imdb.com' + temp[0:17] + 'plotsummary/')
# 	# browser.get('https://m.imdb.com/title/tt0068646/plotsummary/')
# 	# browser.find_element("xpath", '//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[1]/div[2]/ul/div/span[1]/button').click()
# 	# sleep(20)
# 	# html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
# 	# page = BeautifulSoup(response, "html.parser")
# 	# print(page.prettify())	
# 	for row2 in response.find_all('div', {'class' : 'ipc-html-content-inner-div'}):
# # 	print(name)
# # 		# print(type(row2.text))
		# x = [w.lower() for w in re.findall(rx, row2.text) if w.lower() not in stop_words]
# 		with open(f'plot summary/{name}.txt', 'a+') as file:
# 			file.truncate(0)
# 			for word in x:
# 				file.write(word + ' ')
# 	print(x)
# 	print('--------------------------')
	# sleep()
	# break
		# print(row2.get_text())
	# print(row2)
	# elements = browser.find_elements(By.CLASS_NAME, 'ipc-link ipc-link--base ipc-link--inline') 
	# for title in elements: 
	# # select H2s, within element, by tag name 
	# 	heading = title.find_element(By.TAG_NAME, 'a').text 
	# # print H2s 
	# 	print(heading)
	# break
	# break
df1 = pd.read_csv('data.csv')
count = 0
for i in df1:
	if count == 0 or i == "sum":
		count += 1
		continue
	name_list.append(i)
# data = dict()
# for nm in name_list:
# 	dic = dict()
# 	with open(f'plot summary/{nm}.txt', 'r') as file:
# 		for ln in file:
# 			for w in ln.split():
# 				if w in dic:
# 					dic[w] = dic[w] + 1
# 				else:
# 					dic[w] = 1
# 	data[nm] = dic
# df = pd.DataFrame(data)
# df = df.fillna(0)
# df = df.astype(int)
# print(df)
# print(df)
# with open(f'plot summary/titles.txt', 'r+') as file:
# 	for line in file:
# 		temp = ""
# 		for w in line.split():
# 			# print(w)
# 			# print('-----')
# 			temp = temp + w + ' '
# 			# print(temp)
# 		# print(temp)
# 		temp = temp[0:len(temp) - 1]
# 		name_list.append(temp)
# # print(data)
# df = pd.DataFrame(data)
# df = df.fillna(0)
# df = df.astype(int)
df = pd.read_csv('data2 c.csv')
# print(df)


tf = dict()
count = 0
for col in df:
	if count == 0:
		count = count + 1
		continue
	temp = dict()
	x = np.array(df[col]).sum()
	for i in range(0, len(df[col])):
		temp[df['words'][i]] = df[col][i] / x
	tf[col] = temp
# # print(tf)
idf = dict()
count = 0
for row in df.iterrows():
	j = np.array(row[1])
	j = j[1:]
	x = 0
	for ind in j:
		if ind:
			x += 1
	if x == 0:
		print(row)
		x += 1
	ans = math.log(250.0 / x, 10)
	count = 0
	idf[df['words'][row[0]]] = ans

# print(idf)

tf_idf = dict()
count = 0
for col in df:
	if count == 0:
		count = count + 1
		continue
	temp = dict()
	for i in range(0, len(df[col])):
		temp[df['words'][i]] = tf[col][df['words'][i]] * idf[df['words'][i]]
	tf_idf[col] = temp
# print(tf_idf)
last_df = pd.DataFrame(tf_idf)
# pt = input("salam")
new_tf_idf = dict()
temp = dict()

# x = [w.lower() for w in re.findall(rx, pt) if w.lower() not in stop_words]
# new_sum = 0
# for word in x:
# 	if word not in name_list:
# 		continue
# 	if word in temp:
# 		temp[word] += 1
# 		new_sum += 1
# 	else:
# 		temp[word] = 1
# 		new_sum += 1
# for i in range(0, len(df['words'])):
# 	if df['words'][i] in temp:
# 		temp[df['words'][i]] /= new_sum
# 		temp[df['words'][i]] *= idf[df['words'][i]]
# 		continue
# 	temp[df['words'][i]] = 0

# new_tf_idf["given movie"] = temp
# # print(temp)
# # print(new_tf_idf)
# new_df = pd.DataFrame(new_tf_idf)
# print(new_df)
# new_arr = np.array(new_df["given movie"])
# print(new_arr)

# print(df['1. The Shawshank Redemption'][0])
# initializing points in
# numpy arrays
point1 = np.array(last_df['15. Star Wars: Episode V - The Empire Strikes Back'])
sim = dict()
count = 0
for i in last_df:
	if count == 0 or i == "sum":
		count += 1
		continue
	point2 = np.array(last_df[i])
	dist = np.dot(point1,point2)/(norm(point1)*norm(point2))
 
# # calculating Euclidean distance
# # using linalg.norm()
	sim[i] = dist
keys = list(sim.keys())
values = list(sim.values())
sorted_value_index = np.argsort(values)
sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
print(sorted_dict)
# for i in df.iterrows():
# 	j = np.array(i[1])
# 	j = j[1:-1]
# 	print(len(j))
# 	print(j.sum())
# 	break
# printing Euclidean distance

# print(df)
# df['sum'] = df.sum(axis = 1, numeric_only = True)
# df = df[df['sum'] >= 20]
# print(df.iloc[2])
# print(df.head(10))
# df = df.reset_index()
# df = df.drop('index', axis = 1)
# df.rename(columns={
# 'Unnamed: 0': 'words' }, inplace=True)
# df.drop('Unnamed: 0.1', axis = 1)
# df.drop('words', axis = 1)
# df.drop('Unnamed: 0', axis = 1)
# df.to_csv('data.csv')


# df_tf = df
# for i in range(2366):
# 	for j in name_list:
# 		df_tf.iloc[i][j] = df.iloc[i][j] / (df[j].sum())
# print(df.iloc[0]['1. The Shawshank Redemption'])
# print(df_tf)
# print(df_tf)



				