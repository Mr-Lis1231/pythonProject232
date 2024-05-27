import g4f
import telebot
import json
import subprocess
import speech_recognition as sr
import wikipedia
from googletrans import Translator, constants
translator = Translator()
import datetime
import os
bot = telebot.TeleBot("6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c")
token = "6607529150:AAHnO24RneV49PNkhZdGSdKf8VKFL3c0-9c"
import time
from telebot.types import InputFile
import requests
import base64


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Актуальные команды:'
                                      '\n/start - Перезапуск бота. 💣'
                                      '\n/wiki "запрос" - Поиск статьи по запросу в Википедии. 💫'
                                      '\n/donate - Поддержать автора закинув ему на кофе. 🤑'
                                      '\n/photo "запрос" - Генерирует фото по запросу. 🥳'.format(message.from_user))


@bot.message_handler(commands=['donate'])
def send_welcome(message):
    bot.send_message(message.chat.id, '🤑Поддержать автора:'
                                      '\nhttps://www.donationalerts.com/r/mrlis_'.format(message.from_user))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Hi i gpt 35 turbo on russian \n'
                                      'Привет я телеграмм бот сделанный на основе Chat GPT 35 '
                                      '\n\nВ данный момент я могу обрабатывать голосовые и текстовые сообщения'
                                      '\n\nМой создатель Лис 🥰🥰🥰'
                                      '\n\nGitHub создателя, на котором я мб когда-то буду - '
                                      'https://github.com/Mr-Lis1231'.format(message.from_user))


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


@bot.message_handler(commands=['photo'])
def search(message):
    query = message.text[6:]
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '3BE5852B362E5BA9FEEF6E322979EDC8',
                        '26582C8171B1B48207008D499B2FEAC0')
    model_id = api.get_model()
    if query != '':
        try:
            uuid = api.generate(f"{query}", model_id)
            images = api.check_generation(uuid)
            image_base64 = images[0]
            image_data = base64.b64decode(image_base64)
            with open("image.jpg", "wb") as file:
                file.write(image_data)
            bot.send_photo(message.chat.id, InputFile('image.jpg'))
        except:
            bot.send_message(message.chat.id, 'Попробуйте переделать запрос. ☠')
    else:
        bot.send_message(message.chat.id, "Прошу прощения, но я не разобрал сообщение или же оно пустое...")


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
    except Exception as e:
        bot.send_message(message.chat.id, "Наши смелые инженеры уже трудятся над решением...")
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
