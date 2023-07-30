import json
import queue

import skills
import sounddevice as sd
import vosk
from vosk import Model, KaldiRecognizer

import words
from skills import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()
model = vosk.Model('vosk_model_small')
device = sd.default.device = 9, 7
samplerate = int(sd.query_devices(device, 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return
    d = data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    func = answer.split()[0]

    if func == "browser" or func == "opener":
        exec(func + '(d)')
    else:
        speaker(answer.replace(func, ''))
        exec(func + '()')

def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))
    del words.data_set
    skills.speaker("Привет, я твой голосовой ассистент, обращайся ко мне по имени Арсений!")
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                           dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)


if __name__ == "__main__":
    main()