from vosk import Model, KaldiRecognizer
import pyaudio
import json
import pyttsx3
import AppOpener
import webbrowser
import datetime
import time
import threading

with open("./meta.json", "r") as metaFile:
    meta = json.load(metaFile)

try:
    with open("./Shedule.json", "r") as sheduleFile:
        shedule = json.load(sheduleFile)
except FileNotFoundError:
    shedule = None


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
        try:
            application = query.split()
            indexOfOpen = application.index("open") + 1
            application = " ".join(application[indexOfOpen:])
            if meta["websites"].get(application) != None:
                webbrowser.open(meta["websites"].get(application))
                speak(f"opening {application}")
            else:
                AppOpener.open(application, match_closest=True, throw_error=True)
                speak(f"opening {application}")
        except:
            speak(f"could not open {application}")

    elif "what to do now" in query:
        if shedule != None:
            time_array = list(shedule.keys())
            for time in time_array:
                if event_happened(time):
                    continue
                else:
                    speak(f"as per your shedule you need to {shedule[time]}")

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

    elif "search" in query and "on google" in query:
        search: list[str] = query.split()
        indexOfStripStart = search.index("search") + 1
        indexOfStripEnd = search.index("on")
        searchQuery = " ".join(search[indexOfStripStart:indexOfStripEnd])
        URL: str = f"https://www.google.com/search?q={searchQuery}"
        speak(f"searching on google")
        webbrowser.open(URL)

    elif "timer for" in query:
        querySplit = query.split()
        indexForStart = querySplit.index("for") + 1
        timer = " ".join(querySplit[indexForStart:])
        parse_string_time_and_start_timer(timer)

    else:
        if meta["responces"].get(query) != None:
            speak(meta["responces"].get(query))
        else:
            pass


def event_happened(target_time_str):
    target_hour, target_minute = map(int, target_time_str.split(":"))

    current_time = datetime.datetime.now().time()

    target_time = datetime.time(target_hour, target_minute)

    if current_time >= target_time:
        return True
    else:
        return False


def timer_thread(total_seconds, time_str):
    speak(f"Timer started for {time_str}")
    time.sleep(total_seconds)
    speak(f"Timer ended for {time_str}")


def parse_string_time_and_start_timer(time_str):
    word_to_number = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
    }

    words = time_str.lower().split()
    if "and" in words:
        words.remove("and")

    hours, minutes, seconds = 0, 0, 0

    for i in range(len(words)):
        if words[i] == "hour" or words[i] == "hours":
            hours += word_to_number.get(words[i - 1], 0)
        elif words[i] == "minute" or words[i] == "minutes":
            minutes += word_to_number.get(words[i - 1], 0)
        elif words[i] == "second" or words[i] == "seconds":
            seconds += word_to_number.get(words[i - 1], 0)

    total_seconds = hours * 3600 + minutes * 60 + seconds

    timer_thread_obj = threading.Thread(
        target=timer_thread, args=(total_seconds, time_str)
    )
    timer_thread_obj.start()
