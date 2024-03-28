import Assistant
import threading


def __init__():
    AssistantThread = threading.Thread(target=Assistant.init)

    AssistantThread.start()

    AssistantThread.join()


if __name__ == "__main__":
    __init__()
