import telebot
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
URL = "https://t.me/dnd_roll_dice_bot"
bot = telebot.TeleBot(BOT_TOKEN)
database = "superbarbershop.db"
