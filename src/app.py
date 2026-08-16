import telebot
import base 
import app_db

bot = telebot.TeleBot(base.TOKEN)

print("Bot created")

@bot.message_handler(commands=['start'])
def say_hello(message):
    # print(message)
    bot.send_message(message.chat.id, 'به بات کنترل دانشجویان خوش آمدید')




if __name__ == '__main__':
    bot.infinity_polling()