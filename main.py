import PySimpleGUI as sg
from Jarvis import JarvisAssistant
import pyjokes
import pywhatkit
import random
import datetime
import re
import sys

obj = JarvisAssistant()

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there jarvis"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

# =======================================================================================================================================================

def speak(text):
    obj.tts(text)

def startup():
    speak("Initializing Jarvis")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Calibrating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    speak("Now I am online")
    hour = int(datetime.datetime.now().hour)

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready sir. Please tell me how may I help you")

def run_jarvis():
    startup()
    wish()

    while True:
        command = obj.mic_input()

        if isinstance(command, str):
            if re.search('date', command):
                date = obj.tell_me_date()
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                speak(f"Sir the time is {time_c}")

            elif command in GREETINGS:
                response = random.choice(GREETINGS_RES)
                speak(response)

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)

            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif "joke" in command:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "system" in command:
                sys_info = obj.system_info()
                speak(sys_info)

            elif "what is" in command or "who is" in command or "where is" in command or "tell me about" in command:
                ai_output = obj.answering(command)
                speak(ai_output)

            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright sir, going offline. It was nice working with you")
                sys.exit()

def create_window():
    layout = [
        [sg.Text('', size=(50, 1), background_color='black')],
        [sg.Button('Run', size=(10, 1), button_color=('white', 'grey'), border_width=0, pad=(5, 20)),
         sg.Button('Exit', size=(10, 1), button_color=('white', 'grey'), border_width=0, pad=(5, 20))]
    ]

    window = sg.Window('Jarvis', layout, background_color='black', resizable=True, finalize=True,
                       return_keyboard_events=True, use_default_focus=False, no_titlebar=False)

    return window

def main():
    global window
    window = create_window()

    while True:
        event, values = window.read(timeout=1000)

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            sys.exit()

        if event == 'Run':
            run_jarvis()


if __name__ == "__main__":
    main()
