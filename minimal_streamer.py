from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

import twitter_credentials

class StdOutListener(StreamListener): #inherits from StreamListener class

	def on_data(self, data): #streaming method for tweets
		print(data)
		return True
	def on_error(self, status): #streaming method for if any errors occur
		print(status)

if __name__ == '__main__':
	listener = StdOutListener() # creating object of our class 
	auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET) # take two args for authentication
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET) # method provided by OAuthHandlet class

	# after successful authentication 
	# we need to create the Twitter Stream
	stream = Stream(auth, listener)


	# specifying which tweets taht we wanted to see
	# otherwise it streams all tweets
	stream.filter(track=['AAPL', 'GOOGL', 'AMZN', 'MSFT']) # method provided by Stream class. Here, streaming tweets focused on these keywords




