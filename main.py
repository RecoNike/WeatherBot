import config
import telebot

bot = telebot.TeleBot(config.API_TOKEN)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=["start"])
def answer_to_start(message):
    bot.send_message(message.chat.id, 'You writed START')

if __name__ == '__main__':
     bot.infinity_polling()