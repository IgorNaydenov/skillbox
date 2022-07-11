import telebot
import requests
import json
from telebot import types
from datetime import datetime

smile_dict = {
    'Clear': 'Ясно \U00002600',
    'Clouds': 'Облачно \U00002601',
    'Rain': 'Дождь \U00002614',
    'Drizzle': 'Мелкий дождь \U00002614',
    'Snow': 'Снег \U0001F328',
    'Mist': 'Туман \U0001F32B',
    'Thunderstorm': 'Гроза \U000026C8'
}

bot = telebot.TeleBot('5492924379:AAEijHKoeq4tP2LBgieORtG5Ph1FIuMeoho')
open_weather_token = 'fa1cda49b21d24c8b1eef8d501cad413'


def get_weather(city, open_weather_token):
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city,
                                                                                                            open_weather_token))
        data = r.json()
        city = data['name']
        cut_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        weather_description = data['weather'][0]['main']
        if weather_description in smile_dict:
            wd = smile_dict[weather_description]
        else:
            wd = 'Посмотри в окно'
        result = (f'Погода в городе: {city} \nТемпература: {cut_weather}°C {wd}\n'
                  f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nВетер {wind} м/с')
    except Exception as ex:
        result = ('Проверьте название города')
    return result


def Exchange_Rates(value5='USD'):
    req = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    response = req.json()
    er_date = datetime.now().strftime('%d-%m-%Y')
    if value5 == 'USD':
        er_eur = str(response['Valute']['EUR']['Name']) + ' ' + str(response['Valute']['EUR']['Value'])
        er_usd = str(response['Valute'][value5]['Name']) + ' ' + str(response['Valute'][value5]['Value'])
        result = 'На {} следующий курс валют: \n{} \n{}'.format(er_date, er_eur, er_usd)
    else:
        try:
            er_value = str(response['Valute'][value5]['Name']) + ' ' + str(response['Valute'][value5]['Value'])
            result = 'На {} курс запрашиваемой валюты: \n{}'.format(er_date, er_value)
        except Exception:
            result = 'Нет такой валюты, проверьте написанное'
    return result


def Exchange_Rates2():
    result = ''
    req = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    response = req.json()
    for i in response['Valute']:
        result += i + ' ' + response['Valute'][i]['Name'] + '\n'
    # er_usd = str(response['Valute']['USD']['Name']) + ' ' + str(response['Valute']['USD']['Value'])
    return result


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard (Создание кнопок и приветствие)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода")
    item2 = types.KeyboardButton("Курс валют")
    item3 = types.KeyboardButton("help")

    markup.add(item1, item2, item3)
    mess = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, добро пожаловать!".format(message.from_user,
                                                                                                    bot.get_me())
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Погода':

            # keyboard (Создание кнопок под текстом)
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Погода в Краснодаре", callback_data='1')
            item2 = types.InlineKeyboardButton("Погода в другом городе", callback_data='2')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Что вам нужно?', reply_markup=markup)

        elif message.text.lower().split()[0] == "погода":
            city1 = message.text.lower().split()[1]
            bot.send_message(message.chat.id, get_weather(city1, open_weather_token))
        elif message.text == "Курс валют":
            #bot.send_message(message.chat.id, Exchange_Rates())
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Курс доллара/евро", callback_data='3')
            item2 = types.InlineKeyboardButton("Курс других валют", callback_data='4')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Что вам нужно?', reply_markup=markup)
        elif message.text.lower().split()[0] == "валюта":
             currency = message.text.upper().split()[1]
             bot.send_message(message.chat.id, Exchange_Rates(currency))
        elif message.text == "help":
            bot.send_message(message.chat.id, 'в разработке')
        else:
            bot.send_message(message.chat.id, 'я тебя не понимаю')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            # keyboard (Работа с кнопками под текстом)
            if call.data == '1':
                bot.send_message(call.message.chat.id, get_weather('Краснодар', open_weather_token))
            elif call.data == '2':
                bot.send_message(call.message.chat.id,
                                 'Напишите слово погода и через пробел город, например: <b>погода москва</b>',
                                 parse_mode='html')
            elif call.data == '3':
                bot.send_message(call.message.chat.id, Exchange_Rates())
            elif call.data == '4':
                bot.send_message(call.message.chat.id, Exchange_Rates2())
                bot.send_message(call.message.chat.id,
                                 'Напишите слово валюта и через пробел саму на латинице валюту валюту, например: <b>валюта BYN</b>',
                                 parse_mode='html')


            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                                  reply_markup=None)

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #    text="Пишите, всегда поможем!")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)