
"""
    core/__audio.py

    helpful with development of programs
    that work with audio

    author: @alexzander
"""


# python
import os
import threading

# 3rd party
import pyttsx3 # pip install pyttsx3
import sounddevice # pip install sounddevice
from gtts import gTTS # pip install gtts
from pydub import AudioSegment # pip install pydub
from playsound import playsound # pip install playsound
import speech_recognition as sr # pip install SpeechRecognition
from scipy.io.wavfile import write # pip install scipy

# core package (pip install python-core)
from core.system import *
from core.__path import *
from core.aesthetics import *


def playaudio(path, __threaded=True):
    # validation
    if type(path) != str:
        raise TypeError("param @absolute_path should be str.")
    if not is_file(path):
        raise ValueError("param @absolute_path is not an absolute path.")
    if not path.endswith(".wav") and not path.endswith(".mp3"):
        raise ValueError("param @absolute_path should end with .wav or .mp3")
    # /validation

    if __threaded:
        threading.Thread(target=playsound, args=(path, )).start()
    else:
        playsound(path)


def save_text_to_speech(text: str, dst: str, lang="en", slowmotion=False, __print=False):
    # validation
    # @text
    if type(text) != str:
        text = str(text)
    if text == "":
        raise ValueError("param @text is void-string.")

    # @dst
    if type(dst) != str:
        raise TypeError("param @dst should be type str.")
    if not dst.endswith(".mp3") and not dst.endswith(".wav"):
        raise ValueError("param @dst should end with .mp3")
    if not is_abs(dst):
        raise ValueError

    # @lang
    if type(lang) != str:
        lang = str(lang)

    speech = gTTS(text, lang=lang, slow=slowmotion)
    speech.save(dst)

    if __print:
        message = "Text: '{}'\nwas saved to speech here: {}\n{}".format(yellow(text), cyan(dst), green_bold("successfully."))
        print(message)


def save_recorded_mic(dst, duration):
    # validation
    if type(dst) != str:
        raise TypeError("param @dst should be type str.")
    if type(duration) != int:
        raise TypeError("param @duration should be type int.")

    if not is_abs(dst):
        raise ValueError("param @dst should be absolute path.")

    if not dst.endswith(".wav"):
        raise ValueError("param @dst should end with .wav extension.")

    if duration <= 0:
        raise ValueError("param @duration should be bigger than 0.")
    # /validation

    try:
        sample_rate = 44100
        print("you have {} seconds to speak:".format(duration))
        print("recording...")

        myrecording = sounddevice.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
        sounddevice.wait()

        write(dst, sample_rate, myrecording)

        print("recording saved to path: {}.".format(dst))

    except OSError as error:
        print(type(error))
        print(error)
        print("turn OFF your anti-virus application.")


def speech_to_text_from_mic():
    """ listens to your voice, if understands:
        return speech to text else return None.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("listening...")
    with microphone as audio:
        recognizer.adjust_for_ambient_noise(audio)
        recorded_audio = recognizer.listen(audio)
    try:
        text = recognizer.recognize_google(recorded_audio)
    except sr.UnknownValueError:
        print("your speech was incomprehensible. None was returned.")
        return None
    return text


def speech_to_text_from_file(path):
    if not is_file(path):
        raise ValueError
    if not path.endswith(".mp3") and not path.endswith(".wav"):
        raise ValueError

    r = sr.Recognizer()
    with sr.AudioFile(path) as audio_file:
        data = r.record(audio_file)
        try:
            text = r.recognize_google(data)
            return text
        except sr.UnknownValueError as error:
            print(error)
            print(error.message)
            print(type(error))


def speak_engine(message, speech_speed=150):
    if type(message) != str:
        raise TypeError("param @message should be type str.")
    if message == "":
        raise ValueError("param @message shouldn't be void-string.")

    engine = pyttsx3.init("sapi5")
    engine.setProperty("rate", speech_speed)
    engine.setProperty("volume", 0.8)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(message)
    engine.runAndWait()


def modify_volume(src, dst, units=15):
    """ applicable only to .wav and .mp3 files. """
    # validation
    if type(src) != str:
        message = ConsoleColored("param @absolute_path should be type str.", "red", bold=1)
        raise TypeError(message)
        del message
    if type(units) != int:
        message = ConsoleColored("param @quantity should be type int.", "red", bold=1)
        raise TypeError(message)
        del message

    if not os.path.isfile(src):
        message = ConsoleColored("param @absolute_path is not an absolut path.", "red", bold=1)
        raise ValueError(message)
        del message

    if not src.endswith(".wav") and not src.endswith("mp3"):
        message = ConsoleColored("param @absolute_path should end with .wav or .mp3.", "red", bold=1)
        raise ValueError(message)
        del message
    # /validation

    extension = get_file_extension(src)
    if extension == "wav":
        audio_file = AudioSegment.from_wav(src)
    elif extension == "mp3":
        audio_file = AudioSegment.from_mp3(src)
    else:
        raise InvalidExtensionError("{} has {} extension".format(src, extension))

    filename = get_file_name(src)
    audio_file += units
    if units < 0:
        modified_file = dst + "\\{}_minus_{}.{}".format(filename, -units, extension)
    else:
        modified_file = dst + "\\{}_plus_{}.{}".format(filename, units, extension)

    audio_file.export(modified_file, extension)

    # code=0
    return True





# TESTING
if __name__ == '__main__':
    p = "path to wav"
    # save_text_to_speech("hello my name is andrew", p, __print=True)
    # sleep(1)
    t = speech_to_text_from_file(p)
    print(t)