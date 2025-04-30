import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные окружения из файла .env

BOT_TOKEN = os.getenv("BOT_TOKEN")