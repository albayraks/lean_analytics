# alben_mert'in kodu 
# kopyalarken hata olmus olabilir.

import tweepy
from tweepy.parsers import RawParser

def twitter_authorize():
	access_token = "1243687225-5B61D09E54pYoh9KwmUEJL0c38cqSb"
	access_token_secret = "SlczoBG6woA8EdeWK2HkJ5gejD5T6YKbX"
	consumer_key = "bTsiBjA1hLVuayAX"
	consumer_secret = "1a82IF14ddmD0AapAFQIQ3Dpbt7O4l6k"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api

def twitter_search_tweets(q, lang, geocode, since, until):
	api = twitter_authorize()
	data = tweepy.Cursor(api.search, q=q, lang=lang, geocode=geocode, since=since, until=until, include_entities=True).items(1)
	return data


'''7.2.TWITTER DATA CLEANING PROCESS'''
import sqlite3

con = sqlite3.connect("data.db")
cur = con.cursor()
sql = "select * from tbTweetIst"
sql2 = "select * from tbTweetNy"
cur.execute(sql)
data = cur.fetchall()
cur.execute(sql2)
data2 = cur.fetchall()
super_id = [iforiinrange(1, len(data2) + 1)]
id_ny = [i[0] foriindata2]
text_ny = [i[1] foriindata2]
followers_ny = [i[2] foriindata2]
status_ny = [i[3] foriindata2]

from ttp import ttp

p = ttp.Parser()49
foriintext_ny:
result = p.parse(i)
a = result.reply
b = result.users
c = result.tags
e = result.urls


'''7.3.TRANSLATE API'''

import requests
from gtts_token import gtts_token

def translate(target, source, text):
	tokenizer = gtts_token.Token()
	token = tokenizer.calculate_token(text)
	payload = {'q': text, 'tl': target, "sl": source, 'client': 't', 'tk': token, "dt": "t", "ie": "UTF-8",
	"oe": "UTF-8"}
	r = requests.get('https://translate.google.com/translate_a/single', params=payload,
	timeout=10).json()
	res = r[0][0][0]
	return res


'''7.4.TRANSLATE PY'''

import sqlite3
from translate_api import translate
import time

con = sqlite3.connect("data.db")
cur = con.cursor()
sql = "select * from tbTweetIst"
cur.execute(sql)
data = cur.fetchall()
text_ist = [i[1] for i in data]
sent = []
for i in text_ist:
	i = i.replace("\xa0", " ")
	i = i.replace("\n", " ")
	a = i.split(" ")
	x = []

for j in a:
	j = j.strip()
try:
if j == "RT" or j[0] == "@" or j[0] == "#" or j[0:4] == "http":
	pass
else:
x.append(j)
except:
pass
sent.append(" ".join(x))
x = []
sql = "CREATE TABLE IF NOT EXISTS tbTranslate(text TEXT)"
cur.execute(sql)
con.commit()
foriinsent:
try:
trns = translate("en", "tr", i)
except:
time.sleep(10)
trns = translate("en", "tr", i)
print(i)
print(trns)
param = (trns,)
sql = "INSERT INTO tbTranslate VALUES(?)"
cur.execute(sql, param)
con.commit()
cur.close()
con.close()



'''7.5 TONE API'''


import requests

def tone(sentence):
	api_url = 'https://tone-analyzer-demo.mybluemix.net/api/tone'
	data = {'text': '{}'.format(sentence)}
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
	req = requests.post(api_url, data, headers=headers, timeout=20)
	res = req.json()
	category = res["document_tone"]["tone_categories"]
	tones = {}
	foriincategory:51
	forjini['tones']:
	tones[j['tone_name']] = j['score']
	return tones


'''7.6 SENTIMENTAL'''


import sqlite3
from tone_api import tone
import time

con = sqlite3.connect("data.db")
cur = con.cursor()
sql = "select * from tbTweetIst"
sql2 = "select * from tbTweetNy"
cur.execute(sql)
data = cur.fetchall()
cur.execute(sql2)
data2 = cur.fetchall()
super_id = [iforiinrange(1, len(data2) + 1)]
id_ny = [i[0] foriindata2]
text_ny = [i[1] foriindata2]
followers_ny = [i[2] foriindata2]
status_ny = [i[3] foriindata2]
sent = []
foriintext_ny:
i = i.replace("\xa0", " ")
i = i.replace("\n", " ")
a = i.split(" ")
x = []
forjina:
j = j.strip()
try:
if j == "RT" or j[0] == "@" or j[0] == "#" orj[0:4] == "http":
pass
else:
x.append(j)
except:
pass
sent.append(" ".join(x))
x = []


'''7.7 SENTIMENTAL LIST'''


import sqlite3
import time
from tone_api import tone

con = sqlite3.connect("data.db")
cur = con.cursor()
sql = "SELECT * FROM tbTranslate"
cur.execute(sql)
data = cur.fetchall()
sent = []
foriindata:
sent.append(i[0])
super_id = [iforiinrange(1, len(data) + 1)]

def insert_sentemental(param):
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	sql = """ INSERT INTO tbSentementalIst(super_id,Anger,Disgust,Fear,Joy,Sadness,Analytical,Confident,Tentative,Openness,Conscientiousness,Extraversion,Agreeableness,Emotional_Range) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
	param = param
	cur.execute(sql, param)
	con.commit()
	cur.close()
	con.close()
	
	for tweet in zip(sent[983:], super_id[983:]):
		print(tweet[0])
		try:
		result = tone('{}'.format(tweet[0]))
		except:
		time.sleep(20)
		result = tone('{}'.format(tweet[0])
		data = (tweet[1], result["Anger"], result["Disgust"], result["Fear"], result["Joy"],
		result["Sadness"],
		result["Analytical"], result["Confident"], result["Tentative"], result["Openness"],
		result["Conscientiousness"], result["Extraversion"], result["Agreeableness"],
		result["Emotional Range"])
		insert_sentemental(data)


'''7.8 DATABASE'''

import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()
sql_database = "CREATE TABLE IF NOT EXISTS tbTweetIst(id INT, text TEXT, followers INT, statuses INT )"
sql_database2 = "CREATE TABLE IF NOT EXISTS tbTweetNy(id INT, text TEXT, followers INT, statuses INT )"
cur.execute(sql_database)
cur.execute(sql_database2)
con.commit()
cur.close()
con.close()


'''7.9.DOWNLOAD'''

import tweepy
import sqlite3
import time

def access_twitter_api():
	access_token = "1243687225-5B61D09E54pYoh9KwmUSbGr9BFV"
	access_token_secret = "SlczoBG6woA8EdeWK2HkJ5geXk6RhzBObX"
	consumer_key = "bTsiBjA1hLVu3AX"
	consumer_secret = "1a82IF14ddmD0AapXkfwAFQIjKQ3D6bnk"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api

def filter_twitter_api(api, q, rpp, lang, geocode):
	data = tweepy.Cursor(api.search, q=q, rpp=rpp, lang=lang, geocode=geocode).items()
	return data

def insert_database(data, table):
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	foriindata:
	sql_database = "INSERT INTO {}(id , text, followers, statuses) VALUES(?,?,?,?)".format(table)
	param = (i.user.id, i.text, i.user.followers_count, i.user.statuses_count)
	cur.execute(sql_database, param)
	con.commit()
	cur.close()
	con.close()
	return