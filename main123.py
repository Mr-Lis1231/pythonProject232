import g4f
import subprocess
import speech_recognition as sr
from PIL import Image
import wikipedia
from googletrans import Translator, constants
import requests
translator = Translator()
import datetime
import telebot
import os
bot = telebot.TeleBot("6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c")
token = "6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c"


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Актуальные команды:'
                                      '\n/start - Перезапуск бота. 💣'
                                      '\n/wiki "запрос" - Поиск статьи по запросу в Википедии. 💫'
                                      '\n/donate - Поддержать автора закинув ему на кофе. 🤑'.format(message.from_user))


@bot.message_handler(commands=['donate'])
def send_welcome(message):
    bot.send_message(message.chat.id, '🤑Поддержать автора:'
                                      '\nhttps://www.donationalerts.com/r/mrlis_'.format(message.from_user))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hi i gpt 35 turbo on russian \nПривет я телеграмм бот сделанный на основе Chat GPT 35 '
                                      '\n\nВ данный момент я могу обрабатывать голосовые и текстовые сообщения\n\nМой создатель Лис 🥰🥰🥰'
                                      '\n\nGitHub создателя, на котором я мб когда-то буду - https://github.com/Mr-Lis1231'.format(message.from_user))

@bot.message_handler(commands=['wiki'])
def search(message):
    wikipedia.set_lang('ru')
    query = message.text[5:]
    if query == '':
        bot.reply_to(message, 'Ваш запрос пуст 💀 ,\nвведите слово после команды,\nа я постараюсь найти статью.')
    else:
        try:
            results = wikipedia.search(query)
            if not results:
                bot.send_message(message.chat.id, 'Ничего не найдено. ☠')
            else:
                page = wikipedia.page(results[0])
                bot.reply_to(message, page.url)
        except:
            bot.send_message(message.chat.id, 'Ничего не найдено. ☠')


logfile = str(datetime.date.today()) + '.log'


def audio_to_text(dest_name: str):
    r = sr.Recognizer()
    # Read our .vaw file.
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio, language="ru_RU")
    return result

@bot.message_handler(content_types=['voice'])
def get_audio_messages(message):
    try:
        print("Started recognition...")
        file_info = bot.get_file(message.voice.file_id)
        path = os.path.splitext(file_info.file_path)[0]
        fname = os.path.basename(path)
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open(fname+'.oga', 'wb') as f:
            f.write(doc.content)
        process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])
        result = audio_to_text(fname+'.wav')
        bot.reply_to(message, GPT4(format(result)))
    except sr.UnknownValueError as e:
        bot.send_message(message.chat.id, "Прошу прощения, но я не разобрал сообщение или же оно пустое...")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) + ':Message is empty.\n')
    except Exception as e:
        bot.send_message(message.chat.id, "наши смелые инженеры уже трудятся над решением...")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')
    finally:
        os.remove(fname+'.wav')
        os.remove(fname+'.oga')



def GPT4(q):
    res = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presensce_penalty=0.6,
        stop=['You:'],
        messages=[{'role': 'system', 'content': 'Помоги'}, {'role': 'user', 'content': q}]
    )
    translation = translator.translate(f'{res}', dest="ru")
    return translation.text





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
        messages=[{'role': 'system', 'content': 'Помоги'}, {'role': 'user', 'content': q}]
    )
    translation = translator.translate(f'{res}', dest="ru")
    bot.reply_to(message, f'{translation.text}'.format(message.from_user))


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
