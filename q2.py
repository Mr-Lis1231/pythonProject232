import openai
import time
import random
import string
import time

import subprocess

# Проверка интернета
def check_internet_connection():
    try:
        subprocess.check_output("ping -n 1 www.google.com", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
# Генерируем ключ
def generate_random_letters(length):
    characters = string.ascii_letters + string.digits
    random_characters = ''.join(random.choice(characters) for _ in range(length))
    return random_characters

print('''
   ____  _____  ______ _   _          _____    _____ _   _ _____ _____  ______ _____  
  / __ \|  __ \|  ____| \ | |   /\   |_   _|  / ____| \ | |_   _|  __ \|  ____|  __ \ 
 | |  | | |__) | |__  |  \| |  /  \    | |   | (___ |  \| | | | | |__) | |__  | |__) |
 | |  | |  ___/|  __| | . ` | / /\ \   | |    \___ \| . ` | | | |  ___/|  __| |  _  / 
 | |__| | |    | |____| |\  |/ ____ \ _| |_   ____) | |\  |_| |_| |    | |____| | \ \ 
  \____/|_|    |______|_| \_/_/    \_\_____| |_____/|_| \_|_____|_|    |______|_|  \_\

Copyright © 2023 Група шизанутых программистов Chill & Code''')

input('Нажмите Enter что-бы начать...')

# Добавляем ключ в текстовый файл
def add_text_to_file(text):
    file_path = 'openai_free_keys.txt'
    with open(file_path, 'a') as file:
        file.write(text + '\n')

# Начинаем проверять ключи
while True:
    if check_internet_connection() is True:
        test_api_key = 'sk-' + generate_random_letters(48)
        try:
            # Берём сгенерированый ключ
            openai.api_key = test_api_key

            # Берём наш запрос
            prompt = "hi"

            # Пробуем наш ключ. max_tokens было поставлено на 1 что-бы не было заметно что кто-то использовал его
            response = openai.Completion.create(
            engine="davinci-codex",
            prompt=prompt,
            max_tokens=1,
            temperature=0.7,
            n=1,
            stop=None
            )
            print(f'Успешно найдено бесплатный ключ OpenAI API: ( {test_api_key} ). Все ключи которые программа нашла добавляються в txt файл с названием openai_free_keys.txt')

            # Проверяем существует ли txt файл

            import os
            if not os.path.exists(file_path):
                open(file_path, 'w').close()  # Создаём файл если не существует

            add_text_to_file(test_api_key)
            time.sleep(0.000000001)
        except:
            print(f'Ключ {test_api_key} от OpenAI API не есть рабочим, продолжаю искать ключи')
    else:
        print('Проверьте ваше подключение к интернету...')
        time.sleep(1)
    time.sleep(0.000000001)

