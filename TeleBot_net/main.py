import telebot
from netmiko import ConnectHandler
from telebot import types
from datetime import datetime

white_list = [938775711, 544702979, 244741604]
bot = telebot.TeleBot('5492924379:AAEijHKoeq4tP2LBgieORtG5Ph1FIuMeoho')
today_date = datetime.now().strftime('%d-%m-%Y %H:%M')

"""
divice types: "cisco_ios", "huawei", "linux"
"""
def get_device(ip):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "naidenov.is",
        "password": "calips11O",
        "port": 22
    }
    return device

ping_list = []
with open('ip_list.txt', 'r') as file:
    for i_line in file:
        k = i_line.split(',')
        ping_list.append([k[0], k[1].strip()])


@bot.message_handler(func=lambda message: message.chat.id not in white_list)
def fig_vam(message):
    bot.send_message(message.chat.id, 'Access denied')
    with open('logs/_telebot.log', 'a', encoding='utf-8') as file:
        line = f'{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} ' \
               f'{message.from_user.username} {message.text}\n'
        file.write(line)


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard (Создание кнопок и приветствие)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Пинг")
    item2 = types.KeyboardButton("Ребут")
    item3 = types.KeyboardButton("help")

    markup.add(item1, item2, item3)
    mess = "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, добро пожаловать!".format(message.from_user,
                                                                                                    bot.get_me())
    with open('logs/_telebot.log', 'a', encoding='utf-8') as file:
        line = f'{message.from_user.id} - {message.from_user.first_name} {message.from_user.last_name} ' \
               f'{message.from_user.username}\n'
        file.write(line)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':

        if message.text == 'Пинг':
            markup = types.InlineKeyboardMarkup(row_width=1)
            for i_device in ping_list:
                item = types.InlineKeyboardButton(i_device[0],
                                                  callback_data=str(ping_list.index([i_device[0], i_device[1]])))
                markup.add(item)

            bot.send_message(message.chat.id, 'Выберите устройство', reply_markup=markup)

        elif message.text == "Ребут":
            bot.send_message(message.chat.id, 'Че ты уже ребутить собрался, тут еще ничего нет')

        elif message.text == "help":
            bot.send_message(message.chat.id, 'в разработке')

        else:
            bot.send_message(message.chat.id, 'я тебя не понимаю')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            # keyboard (Работа с кнопками под текстом)
            ip_dev = ping_list[int(call.data)][1]
            device = ConnectHandler(**get_device(ip_dev))
            output = device.send_command('show interface status')
            bot.send_message(call.message.chat.id, output)

            with open(f'logs/{call.message.chat.id}_{call.message.chat.first_name}.log', 'a', encoding='utf-8') as file:
                line = f'{today_date} - {ip_dev} show interface status\n'
                file.write(line)

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                                  reply_markup=None)


    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)