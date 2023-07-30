import speech_recognition

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

def listen_command():
        try:
            with speech_recognition.Microphone() as mic:
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)
                query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
            return query
        except speech_recognition.UnknownValueError:
            return "Я не могу разобрать что ты говоришь.."


if __name__ == '__main__':

    # sr = speech_recognition.Recognizer()
    # sr.pause_threshold = 0.5
    print("Слушаю тебя..")
    with speech_recognition.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(source=mic)
        query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
    print(query)
    # инициализация инструментов распознавания и ввода речи
    # recognizer = speech_recognition.Recognizer()
    # microphone = speech_recognition.Microphone()
    #
    # while True:
    #     # старт записи речи с последующим выводом распознанной речи
    #     # и удалением записанного в микрофон аудио
    #     voice_input = record_and_recognize_audio()
    #     os.remove("microphone-results.wav")
    #     print(voice_input)


