#!/usr/bin/python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from time import sleep
ckey = "z9SgFgi6o9c2vzFUfMySv4qqx"
csecret = "ehWvgG6ngqLEpSkayoDj57Oqq2HOcjuC0NfVOyhxnh29fBKGkN"
atoken = "1125875555046322176-jtaNvPFLRnTLl6YJ9u7tZ8ChlDTnov"
asecret = "McWLBux3BDXfMimgxsdw6HFio272AtcWuTR3kNsaqtNBB"

AUS_GEO_CODE = [113.03, -39.06, 154.73, -12.28]
running = True
delay = 10

class listener (StreamListener):
	def on_data(self, data):
		try:
			print(data)
			print("\n")
		except BaseException as e:
			print('error getting data')
			sleep(delay)
			
print('authorizing')	
try:	
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	print('done')
	twitterStream = Stream(auth, listener())
	twitterStream.filter(locations=AUS_GEO_CODE)
except BaseException as e:
	print('error authorizing')
	sleep(delay)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(locations=AUS_GEO_CODE)