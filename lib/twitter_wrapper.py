from lib import tweepy


def tweet(message):

	ATX_TWITTER_CONSUMER_KEY = 'Eocco88eVgvXkz63sAiVg'
	ATX_TWITTER_CONSUMER_SECRET = 'qVU5r8opJXPf6pDpnXOO5k5GMHfWLNqev0Kagoxk'
	ATX_TWITTER_ACCESS_TOKEN_KEY = '432247818-YNZ6yb8OcQTE9Yodk9KtabDgGQCZRQWi9rkJP5w0'
	ATX_TWITTER_ACCESS_TOKEN_SECRET = 'gzR2OI9c4JS6Ght5bTAdTMRwtZA2LBoPyvI3HrcQw'


	# == OAuth Authentication ==
	#
	# This mode of authentication is the new preferred way
	# of authenticating with Twitter.

	# The consumer keys can be found on your application's Details
	# page located at https://dev.twitter.com/apps (under "OAuth settings")
	consumer_key=ATX_TWITTER_CONSUMER_KEY
	consumer_secret=ATX_TWITTER_CONSUMER_SECRET

	# The access tokens can be found on your applications's Details
	# page located at https://dev.twitter.com/apps (located 
	# under "Your access token")
	access_token=ATX_TWITTER_ACCESS_TOKEN_KEY
	access_token_secret=ATX_TWITTER_ACCESS_TOKEN_SECRET

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	

	# If the application settings are set for "Read and Write" then
	# this line should tweet out the message to your account's 
	# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
	api.update_status(message)
	


