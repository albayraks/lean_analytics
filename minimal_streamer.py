# PHASE 2, for having more concise and robust build of our app
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

import twitter_credentials

# # # BASIC LISTENER CLASS THAT JUST PRINTS RECEIVED TWEETS TO STDOUT. # # #
class StdOutListener(StreamListener): #inherits from StreamListener class
	
	# for the purpose of being able to create object that may be directly associated with 
	# a filename that these are going to be writing to. So where do we want store the tweets.
	def __init__(self, fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename

	# improving on_data method
	# HERE I HAVE CREATE A PIPE FOR DB #
	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename, 'a') as tf:
				tf.write(data)
			return True
		except BaseException as e:
			print('Error on data: %s' % str(e))

	def on_error(self, status):
		print(status)


# # # CLASS FOR STREAMING AND PROCESSING LIVE TWEETS. # # #
class TwitterStreamer():
	
	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
		# This handles Twitter authentication and the connection to the Twitter Streaming API.
		# plus, writing streamed tweets to the txt or json file instead of twitter and also handles searched keywords

		listener = StdOutListener(fetched_tweets_filename) 
		auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
		auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
		
		stream = Stream(auth, listener)
		stream.filter(track=hash_tag_list)

if __name__ == '__main__':

	hash_tag_list = ['AAPL', 'GOOGL', 'AMZN', 'MSFT'] # instead of hard coding just wrote concise code 
	fetched_tweets_filename = "tweets.json" # we can also use txt file if necessary

	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

	
