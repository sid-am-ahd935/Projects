import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import webbrowser
from datetime import date

engine = pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
# recognizer = sr.Recognizer()

def speak(*text):
    text = ' '.join(text)
    print(text)
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <12:
        speak("Good Morning")

    elif hour >= 12 and hour< 18:
        speak("Good Afternoon")

    else:
        speak("Good Evening")

    speak("I am Mini Alexa. Please tell me how can I help You?")

def what_can_do():
    engine.setProperty("rate", 200)
    speak(
        '''I can play songs and videos on YouTube,
        Tell You a Joke,
        Search On Wikipedia,
        Tell Date and Time,
        Find your Location,
        Locate Area on Map,
        Open different websites like Insta Gram, YouTube, Gmail, GitHub, StackOverflow,
        And Search on Google.
        
        How may I Help You?'''
    )
    engine.setProperty("rate", 150)



def execute(command : str) -> None:
    if "hello" in command:
        wishMe()

    elif "who are you" in command:
        wishMe()
        speak("I am a virtual assistant. I can listen to you and do tasks you require tme to do")

    elif "can you do" in command:
        what_can_do()

    elif "play" in command:
        command = command.replace("play", '')
        speak("Playing ", command)
        pywhatkit.playonyt(command)

    elif "date and time" in command:
        speak("Today's date is", date.today().strftime("%B %d, %Y"))
        speak("The time is", datetime.datetime.now().strftime("%I:%M %p"))
    
    elif "time and date" in command:
        speak("Today's date is", date.today().strftime("%B %d, %Y"))
        speak("The time is", datetime.datetime.now().strftime("%I:%M %p"))

    elif "date" in command:
        speak("Today's date is", date.today().strftime("%B %d, %Y"))

    elif "time" in command:
        speak("The time is", datetime.datetime.now().strftime("%I:%M %p"))

    elif "wikipedia" in command:
        speak(wikipedia.summary(command.replace('wikipedia', ""), 1))

    elif "what is" in command:
        speak(wikipedia.summary(command.replace('what is', ""), 1))

    elif "who is" in command:
        speak(wikipedia.summary(command.replace('who is', ""), 1))

    elif "where is" in command:
        command = command.replace("where is", '').replace("on map", '').replace("find", '') 
        speak("Here is the location of", command)
        webbrowser.get().open('https://google.nl/maps/place/'+ command +'/&amp;'),
    
    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "my location" in command:
        speak("According to Google Maps, You must be somewhere near here.")
        webbrowser.open("https://www.google.com/maps/search/Where+am+I+?/")
    
    elif "where am i" in command:
        speak("According to Google Maps, You must be somewhere near here.")
        webbrowser.open("https://www.google.com/maps/search/Where+am+I+?/")
    
    elif "locate" in command:
        command = command.replace("locate", '').replace("on map", '')
        speak("Here is the location of", command)
        webbrowser.get().open('https://google.nl/maps/place/'+ command + '/&amp;')
    
    elif "on map" in command:
        command = command.replace("locate", '').replace("on map", '')
        speak("Here is the location of", command)
        webbrowser.get().open('https://google.nl/maps/place/'+ command +'/&amp;')
    
    elif "location of" in command:
        command = command.replace("location of", '').replace("on map", '').replace("in map", '').replace("find", '')
        speak("Here is the location of", command)
        webbrowser.get().open('https://google.nl/maps/place/'+ command +'/&amp;')


    elif "open" in command:
        command = command.replace("open", '').replace(" ", '').strip()
        speak("Opening %s ..." % (command))
        webbrowser.open_new("https://%s.com/" % (command))
    
    elif "bye" in command:
        speak('Good Bye and Have A Nice Day')
        exit()
    
    elif "thank you" in command:
        speak("You are very welcome")
    
    elif "stop" in command:
        speak("Stopping the assistant, exiting... Have a Nice Day")
    
    
    else:
        speak("Here are the search results for", command)
        webbrowser.open('https://www.google.com/search?q='+command)


def run_alexa():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration= 1)
        print("\n")
        print("Start speaking!!")
        speak("Listening...")
        recordedaudio = recognizer.listen(source)
        print("Done.\n")

    try:
        print('Recognizing command...')
        command = recognizer.recognize_google(recordedaudio, language= 'en-in')
        command = command.lower().replace("alexa", '')

        print("User said:", command)
        print("Coumputer said:")
        execute(command)
        print()


    except Exception as e:
        print(e)
        speak("Please say again...")
            

if __name__ == "__main__":

    speak("Clearing Background Noise, please wait...")
    print("\n\n")
    execute('hello')

    # run_alexa()
    while True:
        try:
            run_alexa()
        except KeyboardInterrupt:
            speak("Exiting the app, Have a good day.")
            break

print("////Exit////")