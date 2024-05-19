import telebot, wikipedia
from telebot import types
bot = telebot.TeleBot("6351726411:AAF_eqKlbMItiOHV-RxCI2-P9QzJvPm6ClY")

#Я бот для поиска информации в Википедии. Введите ваш запрос:!

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    iten1 = types.KeyboardButton('Русский')
    iten2 = types.KeyboardButton('English')
    markup.add(iten1, iten2)
    bot.send_message(message.chat.id, 'Hi set langue'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Русский':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton('<-Назад')
        iten1 = types.KeyboardButton('Еще cлово:')
        markup.add(iten1, back)

        bot.send_message(message.chat.id, 'Введите слово а я найду его в вики'.format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, search)



    elif message.text == 'English':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton('<-Return')
        iten1 = types.KeyboardButton('Again')
        markup.add(iten1, back)

        bot.send_message(message.chat.id, '''Type a word and I'll find it on the wiki'''.format(message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, searchEG)


    elif message.text == 'Еще cлово:':
        bot.register_next_step_handler(message, search)

    elif message.text == 'Again':
        bot.register_next_step_handler(message, searchEG)


    elif message.text == '<-Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        iten1 = types.KeyboardButton('Русский')
        iten2 = types.KeyboardButton('English')

        markup.add(iten1, iten2)
        bot.send_message(message.chat.id, '<-Назад'.format(message.from_user), reply_markup=markup)

    elif message.text == '<-Return':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        iten1 = types.KeyboardButton('Русский')
        iten2 = types.KeyboardButton('English')

        markup.add(iten1, iten2)
        bot.send_message(message.chat.id, '<-Return'.format(message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def search(message):
    wikipedia.set_lang('ru')
    query = message.text
    results = wikipedia.search(query)
    if not results:
        bot.send_message(message.chat.id, 'Ничего не найдено.')
    else:
        page = wikipedia.page(results[0])
        bot.send_message(message.chat.id, page.url)


@bot.message_handler(func=lambda message: True)
def searchEG(message):
    wikipedia.set_lang('en')
    query = message.text
    results = wikipedia.search(query)
    if not results:
        bot.send_message(message.chat.id, 'No results found.')
    else:
        page = wikipedia.page(results[0])
        bot.send_message(message.chat.id, page.url)

while True:
    try:
        bot.polling(none_stop=True)
    except:
        bot.polling(none_stop=True)
