from vosk import Model, KaldiRecognizer
import pyaudio
import json


def init():
    model = Model(r".\vosk-model")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    stream.start_stream()

    while True:
        data = stream.read(4096, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            cleaned_data = text.replace("\n", "").replace(" ", "")
            json_object = json.loads(cleaned_data)
            query = json_object["text"]
            if query == "exit":
                break
            print(query)
