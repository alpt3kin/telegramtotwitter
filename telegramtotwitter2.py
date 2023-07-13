import tweepy
import telebot
import requests
import os
from datetime import datetime, timedelta
from pytz import timezone

# Twitter ve Telegram API anahtarlarını buraya yerleştirin
consumer_key = "Twitter API Key"
consumer_secret = "Twıtter API Secret"
bearer_token = r"Twitter Bearer Token"
access_token = "Twitter Access Token"
access_token_secret = "Twitter Access Token Secret"
telegram_token = "Telegram Bot Token"

# Twitter API Bağlantısı
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Medya dosyalarının kaydedileceği klasörü oluştur
media_folder = "media"
if not os.path.exists(media_folder):
    os.makedirs(media_folder)

# Tarih ve saat formatı
date_format = "%d.%m.%Y %H:%M:%S %Z%z"

# Zaman dilimini ayarla (GMT+3)
timezone = timezone("Etc/GMT+3")

# Fotoğraf sayısı sınırı
photo_limit = 100

# Telegram botunu oluştur
bot = telebot.TeleBot(telegram_token)

# Telegram mesajlarını işlemek için kullanılacak decorator
@bot.message_handler(content_types=['photo'])
def handle_message(message):
    # Fotoğraf dosyasını indir
    file_info = bot.get_file(message.photo[-1].file_id)
    photo_url = f"https://api.telegram.org/file/bot{telegram_token}/{file_info.file_path}"
    response = requests.get(photo_url)

    # Fotoğrafı kaydet ve dosya adına tarih ve saat damgası ekle
    now = datetime.now(timezone)
    timestamp = now.strftime("%d%m%Y_%H%M")
    media_path = f"{media_folder}/{timestamp}.jpg"
    with open(media_path, 'wb') as f:
        f.write(response.content)

    # Fotoğraftan mesajın text bilgisini al
    text = message.caption if message.caption else "EĞER FOTOĞRAF AÇIKLAMASI YOKSA BURAYA YAZDIĞIN ŞEYİ PAYLAŞACAK"

    # Medya yükleme
    media = api.media_upload(media_path)

    # Medya bilgisini kullanarak tweet atın
    client.create_tweet(text=text, media_ids=[media.media_id])

    # Fotoğraf sayısını kontrol et ve fazlaysa eski fotoğrafları sil
    check_and_clean_photos()

def check_and_clean_photos():
    photo_files = sorted(os.listdir(media_folder))
    num_photos = len(photo_files)
    if num_photos > photo_limit:
        num_to_delete = num_photos - photo_limit
        for i in range(num_to_delete):
            file_to_delete = os.path.join(media_folder, photo_files[i])
            os.remove(file_to_delete)

# Botu çalıştırın
bot.polling()
