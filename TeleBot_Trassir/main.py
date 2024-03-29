import telebot
from netmiko import ConnectHandler
from telebot import types
from datetime import datetime
import base64

white_list = [938775711, 1164584848, 1776437089]
bot = telebot.TeleBot('5733208508:AAGci784PLTtyEABcBvDGCVHR_ZMHfo0JqE')
today_date = datetime.now().strftime('%d-%m-%Y %H:%M')

"""
divice types: "cisco_ios", "huawei", "linux"
cisco_ios_telnet - если нужно подключение по телнет

adminbot  JMkrnLvof2$k
"""
# user1 = (base64.b64decode('bmFpZGVub3YuaXM='.encode('UTF-8'))).decode()
# pass1 = (base64.b64decode('Y2FsaXBzMTFP'.encode('UTF-8'))).decode()

def get_device_cisco(ip):
    device = {
        "device_type": "cisco_ios_telnet",
        "host": ip,
        "username": 'admin',
        "password": 'Pphz55p1AX',
        "port": 23
    }
    return device

def get_device(ip, pass1):
    device = {
        "device_type": "linux",
        "host": ip,
        "username": 'trassir',
        "password": pass1,
        "port": 22
    }
    return device

ping_list = []
with open('ip_list.txt', 'r', encoding='UTF-8') as file:
    for i_line in file:
        k = i_line.split(',')
        ping_list.append([k[0], k[1], k[2].strip()])

cisco_list =[]
with open('ip_list_cisco1.txt', 'r', encoding='UTF-8') as file1:
    for i_line in file1:
        k = i_line.split(',')
        cisco_list.append([k[0], k[1].strip()])


@bot.message_handler(func=lambda message: message.chat.id not in white_list)
def fig_vam(message):
    bot.send_message(message.chat.id, 'Access denied')
    with open('var/log/_telebot.log', 'a', encoding='utf-8') as file:
        line = f'{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} ' \
               f'{message.from_user.username} {message.text}\n'
        file.write(line)


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard (Создание кнопок и приветствие)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Trassir")
    item2 = types.KeyboardButton("Cisco")
    item3 = types.KeyboardButton("help")

    markup.add(item1, item2, item3)
    mess = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, добро пожаловать!".format(message.from_user,
                                                                                                    bot.get_me())
    with open('var/log/_telebot.log', 'a', encoding='utf-8') as file:
        line = f'{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} ' \
               f'{message.from_user.username}\n'
        file.write(line)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':

        if message.text == 'Trassir':
            markup = types.InlineKeyboardMarkup(row_width=1)
            for i_device in ping_list:
                item = types.InlineKeyboardButton(i_device[0],
                                        callback_data=str(ping_list.index([i_device[0], i_device[1], i_device[2]])))
                markup.add(item)

            bot.send_message(message.chat.id, 'Выберите устройство', reply_markup=markup)

        elif message.text == "Cisco":
            markup = types.InlineKeyboardMarkup(row_width=1)
            for i_device in cisco_list:
                item = types.InlineKeyboardButton(i_device[0],
                                                  callback_data=str(cisco_list.index([i_device[0], i_device[1]])+100))
                markup.add(item)

            bot.send_message(message.chat.id, 'Выберите устройство', reply_markup=markup)

        elif message.text == "help":
            bot.send_message(message.chat.id, 'в разработке')

        else:
            bot.send_message(message.chat.id, 'я тебя не понимаю')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if int(call.data) < 100:
                # keyboard (Работа с кнопками под текстом)
                ip_dev = ping_list[int(call.data)][1]
                pass_dev = ping_list[int(call.data)][2]
                device = ConnectHandler(**get_device(ip_dev, pass_dev))
                device.send_command('sudo reboot')
                output = f'Трассир {ping_list[int(call.data)][0]} будет перезагружен'
                bot.send_message(call.message.chat.id, output)


                with open(f'var/log/{call.message.chat.id}_{call.message.chat.first_name}.log', 'a', encoding='utf-8') as file:
                    line = f'{today_date} - {ip_dev} reboot\n'
                    file.write(line)

                # remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                                      reply_markup=None)
            elif int(call.data) >= 100:
                ip_dev = cisco_list[int(call.data)-100][1]
                device = ConnectHandler(**get_device_cisco(ip_dev))
                output = device.send_command('sh ip int br')
                #output = f'Трассир {cisco_list[int(call.data)][0]} будет перезагружен'
                bot.send_message(call.message.chat.id, output)

                with open(f'var/log/{call.message.chat.id}_{call.message.chat.first_name}.log', 'a',
                          encoding='utf-8') as file:
                    line = f'{today_date} - {ip_dev} show interfaces\n'
                    file.write(line)

                #remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                                     reply_markup=None)

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)