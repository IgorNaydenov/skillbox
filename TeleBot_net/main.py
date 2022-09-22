import telebot
import requests
import json
import netmiko
from telebot import types
from datetime import datetime

white_list = [938775711]
bot = telebot.TeleBot('5492924379:AAEijHKoeq4tP2LBgieORtG5Ph1FIuMeoho')


@bot.message_handler(func=lambda message: message.chat.id not in white_list)
def fig_vam(message):
    bot.send_message(message.chat.id, 'sorry')


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
    with open('telebot.log', 'w', encoding='utf-8') as file:
        line = f'{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} {message.from_user.username}\n'
        file.write(line)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)