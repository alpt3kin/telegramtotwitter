import tweepy

##WHEN YOU FILL IN THE RELEVANT SECTIONS, IT WILL PRINT THE TWITTER USERNAME TO WHICH THE TWITTER API IS CONNECTED. IT IS FOR CONTROL PURPOSES.
consumer_key = "Twitter API Key"
consumer_secret = "Twıtter API Secret"
access_token = "Twitter Access Token"
access_token_secret = "Twitter Access Token Secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.verify_credentials()
print("Twitter kullanıcı adı:", user.screen_name)
