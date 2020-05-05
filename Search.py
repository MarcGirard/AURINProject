#!/usr/bin/python

import tweepy
from datetime import datetime
from time import sleep
ckey = "z9SgFgi6o9c2vzFUfMySv4qqx"
csecret = "ehWvgG6ngqLEpSkayoDj57Oqq2HOcjuC0NfVOyhxnh29fBKGkN"
atoken = "1125875555046322176-jtaNvPFLRnTLl6YJ9u7tZ8ChlDTnov"
asecret = "McWLBux3BDXfMimgxsdw6HFio272AtcWuTR3kNsaqtNBB"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

		
api = tweepy.API(auth)

query = '*'
max_tweets = 100
running = True
delay = 900
megadelay = 1500
i = 0
while running:
	try:
		searched_tweets = [ status for status in tweepy.Cursor(api.search, q=query,geocode="-37.6390981,145.0434407,10km").items(max_tweets)]		
		if searched_tweets == []:
			running = False
			print("stopping")
		else:
			for tweet in searched_tweets:
					if (tweet.lang) == "en":
						print(tweet)
						print("\n")
			print(" ran" ,i, "th time")
			i = i+1
			sleep(delay)
						
	except BaseException as e:
		sleep(megadelay)
