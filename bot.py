import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import credentials
import texts
import design
import menu
import registration
import services
import appointments

from credentials import bot

# Commands
bot.set_my_commands([
    telebot.types.BotCommand("/start", "Welcome message"),
    telebot.types.BotCommand("/home", "Welcome message"),
    telebot.types.BotCommand("/services", "Welcome message"),
    telebot.types.BotCommand("/aboutus", "Welcome message"),
    telebot.types.BotCommand("/appointments", "Welcome message"),
    telebot.types.BotCommand("/help", "Information about bot")
])

# HELP message
@bot.message_handler(["help"])
def send_help(message):
    user_id = message.from_user.id
    print(user_id)
    pass

'''
# Inline Keyboard Button handler
@bot.callback_query_handler(func=lambda message:True)
def button_press_handler(call):
    data = call.data
    user_id = call.from_user.id
    pass
'''
    
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()
