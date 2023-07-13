import tweepy

##İLGİLİ BÖLÜMLERİ DOLDURDUĞUNDA TWITTER API'NIN BAĞLI OLDUĞU TWITTER KULLANICI ADINI EKRANA YAZDIRIR. KONTROL AMAÇLI KULLANIM İÇİNDİR.
consumer_key = "Twitter API Key"
consumer_secret = "Twıtter API Secret"
access_token = "Twitter Access Token"
access_token_secret = "Twitter Access Token Secret"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.verify_credentials()
print("Twitter kullanıcı adı:", user.screen_name)
