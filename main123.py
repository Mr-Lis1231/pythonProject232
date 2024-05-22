import g4f
import subprocess
import speech_recognition as sr
from PIL import Image
from googletrans import Translator, constants
import requests
translator = Translator()
import datetime
import telebot
import os
bot = telebot.TeleBot("6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c")
token = "6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c"




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hi i gpt 35 turbo on russian'.format(message.from_user))


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
        bot.send_message(message.chat.id, GPT4(format(result)))
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
        max_tokens=10000,
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
        max_tokens=10000,
        top_p=1.0,
        frequency_penalty=0.0,
        presensce_penalty=0.6,
        stop=['You:'],
        messages=[{'role': 'system', 'content': 'Помоги'}, {'role': 'user', 'content': q}]
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
