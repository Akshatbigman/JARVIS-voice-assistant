import speech_recognition as sr
import pyttsx3

from Jarvis.features import date_time
from Jarvis.features import website_open
from Jarvis.features import system_stats
from Jarvis.features.query import ai 

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

class JarvisAssistant:
    def __init__(self):
        pass

    def mic_input(self):
        """
        Fetch input from mic
        return: user's voice input as text if true, false if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
            except:
                print('Please try again')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return  False

    def tts(self, text):
        """
        Convert any text to speech
        :param text: text(String)
        :return: True/False (Play sound if True otherwise write exception to log and return  False)
        """
        try:
            engine.say(text)
            engine.runAndWait()
            engine.setProperty('rate', 175)
            return True
        except:
            t = "Sorry I couldn't understand and handle this input"
            print(t)
            return False

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)
    
    def system_info(self):
        return system_stats.system_stats()

    def answering(self, command):
        return ai(command) 
