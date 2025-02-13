import tweepy
import telebot
import requests
import os
from datetime import datetime, timedelta
from pytz import timezone

# Insert Twitter and Telegram API keys here
consumer_key = "Twitter API Key"
consumer_secret = "Twıtter API Secret"
bearer_token = r"Twitter Bearer Token"
access_token = "Twitter Access Token"
access_token_secret = "Twitter Access Token Secret"
telegram_token = "Telegram Bot Token"

# Twitter API Connection
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Create folder to save media files
media_folder = "media"
if not os.path.exists(media_folder):
    os.makedirs(media_folder)

# Date and time format
date_format = "%d.%m.%Y %H:%M:%S %Z%z"

# Set time zone (GMT+3)
timezone = timezone("Etc/GMT+3")

# Photo count limit
photo_limit = 100

# Create Telegram bot
bot = telebot.TeleBot(telegram_token)

# Decorator to be used to render Telegram messages
@bot.message_handler(content_types=['photo'])
def handle_message(message):
    # Download photo file
    file_info = bot.get_file(message.photo[-1].file_id)
    photo_url = f"https://api.telegram.org/file/bot{telegram_token}/{file_info.file_path}"
    response = requests.get(photo_url)

    # Save the photo and add a date and time stamp to the file name
    now = datetime.now(timezone)
    timestamp = now.strftime("%d%m%Y_%H%M")
    media_path = f"{media_folder}/{timestamp}.jpg"
    with open(media_path, 'wb') as f:
        f.write(response.content)

    # Get text information of message from photo
    text = message.caption if message.caption else "EĞER FOTOĞRAF AÇIKLAMASI YOKSA BURAYA YAZDIĞIN ŞEYİ PAYLAŞACAK"

    # Media upload
    media = api.media_upload(media_path)

    # Tweet with using media info
    client.create_tweet(text=text, media_ids=[media.media_id])

    # Check the number of photos and delete old photos if too many
    check_and_clean_photos()

def check_and_clean_photos():
    photo_files = sorted(os.listdir(media_folder))
    num_photos = len(photo_files)
    if num_photos > photo_limit:
        num_to_delete = num_photos - photo_limit
        for i in range(num_to_delete):
            file_to_delete = os.path.join(media_folder, photo_files[i])
            os.remove(file_to_delete)

# Run bot
bot.polling()
