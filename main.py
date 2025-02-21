import config
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import GetWeather
import sqlite3

bot = telebot.TeleBot(config.API_TOKEN)

# Connect to SQLite database
conn = sqlite3.connect('weatherbot.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    city TEXT NOT NULL
)
''')
conn.commit()

def save_city(user_id, city):
    cursor.execute('SELECT city FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        cursor.execute('UPDATE users SET city = ? WHERE user_id = ?', (city, user_id))
    else:
        cursor.execute('INSERT INTO users (user_id, city) VALUES (?, ?)', (user_id, city))
    
    conn.commit()

@bot.message_handler(commands=["start"])
def answer_to_start(message):
    bot.send_message(message.chat.id, 'Hello, Send me Your city name, and I`ll answer with information :) \n It must be in Latin \n(do not use Cyrillic and numbers)', reply_markup=ReplyKeyboardRemove())

@bot.message_handler(content_types=["text"])
def get_weather(message):
    user_id = message.from_user.id
    city = message.text.lower()

    cursor.execute('SELECT city FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        markup = ReplyKeyboardMarkup(row_width=2)
        btn1 = KeyboardButton('Get Weather')
        btn2 = KeyboardButton('Change City')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'You already have a city recorded. Choose an option:', reply_markup=markup)
    else:
        save_city(user_id, city)
        weather = GetWeather.getWeather(city)
        bot.send_message(message.chat.id, weather)

@bot.message_handler(func=lambda message: message.text == 'Get Weather')
def send_weather(message):
    user_id = message.from_user.id
    cursor.execute('SELECT city FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        city = result[0]
        weather = GetWeather.getWeather(city)
        bot.send_message(message.chat.id, weather)

@bot.message_handler(func=lambda message: message.text == 'Change City')
def change_city(message):
    bot.send_message(message.chat.id, 'Send me your new city name:', reply_markup=ReplyKeyboardRemove())

if __name__ == '__main__':
    bot.infinity_polling()