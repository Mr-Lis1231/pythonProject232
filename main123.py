import g4f
from googletrans import Translator, constants
import telebot

translator = Translator()
bot = telebot.TeleBot("6607529150:AAFIWGwxhX_LgxpV0b0dyEJK86HUSWWG4w0")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hi i gpt 35 turbo on russian'.format(message.from_user))

@bot.message_handler(content_types=['text'])
def bot_message(message):
    q = message.text
    res = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presensce_penalty=0.6,
        stop=['You:'],
        messages=[{'role': 'system', 'content':'Помоги'}, {'role':'user', 'content':q}]
    )
    translation = translator.translate(f'{res}', dest="ru")
    bot.send_message(message.chat.id, f'{translation.text}'.format(message.from_user))


# translator = Translator()
# while True:
#
#     q = input()
#     res = g4f.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         temperature=0.9,
#         max_tokens=1000,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presensce_penalty=0.6,
#         stop=['You:'],
#         messages=[{'role': 'system', 'content':'Помоги'}, {'role':'user', 'content':q}]
#     )
#     translation = translator.translate(f'{res}', dest="ru")
#     print(f"{translation.text}")



while True:
    try:
        bot.polling(none_stop=True)
    except:
        bot.polling(none_stop=True)
