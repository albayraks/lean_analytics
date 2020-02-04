# Pagination and Cursor, PART phase3_v2
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

import twitter_credentials


# # # # TWITTER CLIENT # # # #
# Within help of Cursor Object we can get specific types of tweets
class TwitterClient():
	# defaults to None for having functionality of using empty for own timeline tweets
	def __init__(self, twitter_user=None):
		self.auth = TwitterAuthenticator().authenticate_twitter_app()
		self.twitter_client = API(self.auth)

		self.twitter_user = twitter_user

	# by default this method gets users own timeline tweets if there is no other indication
	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets

	def get_friend_list(self, num_friends):
		friend_list = [] 
		for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
			friend_list.append(friend)
		return friend_list

	def get_home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []
		for tweet in  Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(tweet)
		return home_timeline_tweets

	
	# MY VERY FIRST TRY
	# details on 'http://docs.tweepy.org/en/latest/api.html#help-methods'
	def filter_specific_tweets(self, q, lang, geocode, until, num_tweets):
		filtered_tweets = []
		for tweet in Cursor(self.twitter_client.search, q=q, lang=lang, geocode=geocode, until=until).items(num_tweets):
			filtered_tweets.append(tweet)
		return filtered_tweets


# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		return auth


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
	
	def __init__(self, fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename

	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename, 'a') as tf:
				tf.write(data)
			return True
		except BaseException as e:
			print('Error on data: %s' % str(e))

	def on_error(self, status):
		if status == 420:
			# Returning False on_data method in case of rate limit occurs.
			return False
		print(status)


class TwitterStreamer():

	def __init__(self):
		self.twitter_authenticator= TwitterAuthenticator()
	
	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

		listener = TwitterListener(fetched_tweets_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app() 
				
		stream = Stream(auth, listener)
		stream.filter(track=hash_tag_list)

if __name__ == '__main__':

	hash_tag_list = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
	fetched_tweets_filename = "tweets.json"

	
	# twitter_streamer = TwitterStreamer()
	# twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

	# INSTEAD OF STREAMER, WE ARE CALLING OUR NEW CLIENT CLASS
	# twitter_client = TwitterClient('pycon') # if nothing specified for username, it gets my own timeline tweets
	# print(twitter_client.get_user_timeline_tweets(1))

	
	# MY FIRST TRY

	q = 'brexit'
	lang = 'en'
	geocode = '51.507496,-0.127285,20km'
	until = '2020-02-03'
	num_tweets = 2

	twitter_client = TwitterClient()
	print(twitter_client.filter_specific_tweets(q, lang, geocode, until, num_tweets))

	# def filter_specific_tweets(self, q, lang, geocode, until, num_tweets):
	# 	filtered_tweets = []
	# 	for tweet in Cursor(self.twitter_client.search, q=q, lang=lang, geocode=geocode, until=until).items(num_tweets):
	# 		filtered_tweets.append(tweet)
	# 	return filtered_tweets
