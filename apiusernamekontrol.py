import tweepy

consumer_key = "JAireK4gNsgiR1kyHthv96sYd"
consumer_secret = "m0Pva7gVg4vTuMWQTkjDRdBOzVg8aH1WhJ2SrQGmB6DciY8qoA"
access_token = "1577251423259136000-2eHWx2gnJQd4UP4O4dIARjnFG185uz"
access_token_secret = "Q1y449CFLVv9yIJyrkH9ZnxDF4axCNOfcVq8AzdONrMOh"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.verify_credentials()
print("Twitter kullanıcı adı:", user.screen_name)