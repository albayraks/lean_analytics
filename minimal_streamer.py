# Pagination and Cursor, PART 3
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

import twitter_credentials

# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator(): # defined this class for authentication. Making more modular

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

	# constructor for authentication
	def __init__(self):
		self.twitter_authenticator= TwitterAuthenticator()
	
	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):

		listener = TwitterListener(fetched_tweets_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app() # and making use of in method
				
		stream = Stream(auth, listener)
		stream.filter(track=hash_tag_list)

if __name__ == '__main__':

	hash_tag_list = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
	fetched_tweets_filename = "tweets.json"

	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)


