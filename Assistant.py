from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
import AppOpener
import webbrowser

with open("./meta.json", "r") as metaFile:
    meta = json.load(metaFile)


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
            cleaned_data: str = text.replace("\n", "").replace("the ", "")
            json_object = json.loads(cleaned_data)
            query: str = json_object["text"]
            querys = query.split("and")
            for query in querys:
                print(query)
                command(query)


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def command(query: str) -> None:
    if "close yourself" in query:
        speak("exiting")
        exit()

    elif "open" in query:
        application = query.split()
        indexOfOpen = application.index("open") + 1
        application = " ".join(application[indexOfOpen:])
        try:
            if meta["websites"].get(application) != None:
                webbrowser.open(meta["websites"].get(application))
                speak(f"opening {application}")
            else:
                AppOpener.open(application, match_closest=True, throw_error=True)
                speak(f"opening {application}")
        except:
            speak(f"could not open {application}")

    elif "close" in query:
        application = query.split()
        indexOfClose = application.index("close") + 1
        application = " ".join(application[indexOfClose:])
        try:
            AppOpener.close(application, match_closest=False, throw_error=True)
            speak(f"closeing {application}")
        except:
            speak(f"could not find any process named {application} running")

    elif "what is" in query:
        search: list[str] = query.split()
        indexOfStripStart = search.index("is") + 1
        searchQuery: str = " ".join(search[indexOfStripStart:])
        URL: str = f"https://duckduckgo.com/?q={searchQuery}"
        speak(f"searching on duck duck go")
        webbrowser.open(URL)

    elif "search" in query and "on stack" in query:
        search: list[str] = query.split()
        indexOfStripStart = search.index("search") + 1
        indexOfStripEnd = search.index("on")
        searchQuery = " ".join(search[indexOfStripStart:indexOfStripEnd])
        URL: str = f"https://stackoverflow.com/serach?q={searchQuery}"
        speak(f"searching on stack overflow")
        webbrowser.open(URL)

    elif "search" in query and "on duck duck go" in query:
        search: list[str] = query.split()
        indexOfStripStart = search.index("search") + 1
        indexOfStripEnd = search.index("on")
        searchQuery = " ".join(search[indexOfStripStart:indexOfStripEnd])
        URL: str = f"https://duckduckgo.com/?q={searchQuery}"
        speak(f"searching on duck duck go")
        webbrowser.open(URL)

    elif "search" in query and "on google":
        search: list[str] = query.split()
        indexOfStripStart = search.index("search") + 1
        indexOfStripEnd = search.index("on")
        searchQuery = " ".join(search[indexOfStripStart:indexOfStripEnd])
        URL: str = f"https://www.google.com/search?q={searchQuery}"
        speak(f"searching on google")
        webbrowser.open(URL)

    else:
        if meta["responces"].get(query) != None:
            speak(meta["responces"].get(query))
        else:
            pass
