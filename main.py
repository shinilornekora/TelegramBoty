import telebot
import requests
from bs4 import BeautifulSoup
import random

token = '5950110623:AAFsvO_828UWf6rrAoUUWVRp7IKILvG05Ks'
bot = telebot.TeleBot(token)

# Как пропатчить kde2 под freeBSD?
# pip install <Имя_библиотеки>==<Версия>
# Декоратор - это расширение функции, написанной через @, фунцией под @.
# 3.6.6 pyTelegramBotAPI, 0.0.4 telebot


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = """
    Привет! Я умею рассказывать стихи, знаю очень много интересных фактов и смогу показать милых котиков!
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton("Факт")
    button2 = telebot.types.KeyboardButton("Стихотворение")
    button3 = telebot.types.KeyboardButton("Котики")
    button4 = telebot.types.KeyboardButton("Стикеры")
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


@bot.message_handler(commands=["poem"])
def send_poem(message):
    print("Запрос на стихотворение")
    poem_text = """
    Муха села на варенье, вот и всё стихотворение...
    """
    bot.send_message(message.chat.id, poem_text)
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    button_url = telebot.types.InlineKeyboardButton("Перейти", url="https://stihi.ru/")
    keyboard.add(button_url)
    bot.send_message(message.chat.id, 'Больше стихов по ссылке ниже:', reply_markup=keyboard)


@bot.message_handler(commands=["stickers"])
def send_stickers(message):
    print("Запрос на стикеры")
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEG_FpjpxvOsQty5vs57K0od8w6bERAvAACUygAAnArIUkXmnJpnCTU-iwE")


@bot.message_handler(commands=["cats"])
def send_cat(message):
    print("Запрос на кошку")
    cat = str(random.randint(1, 10))
    # r w r+ w+ a rb wb -- file-read modes
    cat_img = open("img/" + cat + ".jpg", 'rb')
    bot.send_photo(message.chat.id, cat_img)


@bot.message_handler(commands=["fact"])
def send_fact(message):
    print("Запрос на факт")
    # Гет запрос выдаёт нам код
    response = requests.get("https://i-fakt.ru/").content
    html = BeautifulSoup(response, 'lxml')
    fact = random.choice(html.find_all(class_='p-2 clearfix'))
    fact_link = fact.a.attrs['href']
    fact_text = fact.text
    bot.send_message(message.chat.id, fact_link + fact_text)


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == "Стихотворение":
        send_poem(message)
    elif message.text == "Стикеры":
        send_stickers(message)
    elif message.text == "Котики":
        send_cat(message)
    elif message.text == "Факт":
        send_fact(message)
    else:
        bot.send_message(message.chat.id, "Я не знаю, что на это ответить :c")


bot.polling()
