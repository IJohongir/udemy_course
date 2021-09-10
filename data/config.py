import os
from dotenv import load_dotenv

load_dotenv()

path_db = str(os.getenv("PATH_TO_DB"))
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    557371080,884666206
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
