import config
import telebot
import GetWeather

bot = telebot.TeleBot(config.API_TOKEN)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=["start"])
def answer_to_start(message):
    bot.send_message(message.chat.id, 'Hello, Send me Your city name, and I`ll answer with information :)')

@bot.message_handler(content_types=["text"])
def get_weather(message):
    weather = GetWeather.getWeather(message.text.lower())
    bot.send_message(message.chat.id, weather)
    print(type(message))

if __name__ == '__main__':
     bot.infinity_polling()