import datetime
import os, webbrowser, sys, requests, subprocess
import pyttsx3
import words
from fuzzywuzzy import fuzz
from pyowm import OWM
from pyowm.utils.config import get_default_config
# Инициализация голосового движка
engine = pyttsx3.init()
engine.setProperty('rate', 180) # скорость речи

def speaker(text):
    engine.say(text)
    engine.runAndWait()

def browser(data):
    """ Функция поиска в браузере """
    words_list = ['найди', 'поиск', 'нужен интернет', 'в интернете', 'в браузер', 'найти' ]
    for w in words_list:
        if w in data:
            data = data.replace(w, '')
    webbrowser.open(f'https://www.google.com/search?q={data}&sxsrf=APwXEdf-WkxYjTq3AH9OOlBTnQAMXirq3w%3A1685103330299&ei=4qJwZLrzEc72rgT1-r-oBg&ved=0ahUKEwi67KWL-5L_AhVOu4sKHXX9D2UQ4dUDCA8&oq={data}&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQDEoECEEYAFAAWABgAGgAcAB4AIABAIgBAJIBAJgBAA&sclient=gws-wiz-serp', new=2)

def opener(data):
    """ Функция перехода на некоторые сайты """
    links = {
        ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
        ('вк', 'вконтакте', 'контакт', 'vk'): 'https://vk.com/',
        ('браузер', 'интернет', 'browser'): 'https://google.com/',
        ('insta', 'instagram', 'инстаграм', 'инста', 'инсту'): 'https://www.instagram.com/',
        ('twitch', 'твич', 'твитч'): 'https://www.twitch.tv/',
        ('почта', 'почту', 'gmail', 'гмейл', 'гмеил', 'гмаил', 'майл'): 'http://gmail.com/',
    }
    j = 0
    if 'и' in data:
        data = data.replace('и', '').replace('  ', ' ')
    double_task = data.split()
    if j != len(double_task):
        for i in range(len(double_task)):
            for vals in links:
                for word in vals:
                    if fuzz.ratio(word, double_task[i]) > 75:
                        webbrowser.open(links[vals])
                        speaker('Открываю ' + double_task[i])
                        j += 1
                        break

def weather():
    """ Функция определения погоды на данный момент """
    place = words.SETTINGS['place']
    country = words.SETTINGS['country']
    country_and_place = place + ", " + country
    owm = OWM('3b5c9afce9afd6dafad72bce32c94592')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(country_and_place)
    w = observation.weather
    status = w.detailed_status
    w.wind()
    humidity = w.humidity
    temp = w.temperature('celsius')[
        'temp']
    speaker("В городе " + str(country) +
              "\nТемпература " + str(
        round(temp)) + " градусов по цельсию" +
              "\nВлажность составляет " + str(humidity) + "%" +
              "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")


def off_pc():
    """ Функция выключения компьютера """
    speaker("пк выключается")
    os.system('shutdown')




def time():
    now = datetime.datetime.now()
    speaker("Сейчас {h} часов {m} минут".format(h=now.hour, m=now.minute))

def off_assistant():
    sys.exit()