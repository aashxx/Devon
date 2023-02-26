import datetime
import os
import sys
import time
import webbrowser as wb
from tkinter import *
from tkvideo import tkvideo
import pyautogui as auto
import pyjokes as pj
import pyttsx3
import pywhatkit as pw
import speech_recognition as sr
import wikipedia

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Enables Devon to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#Devon greets the user
def greetUser():
    hour = int(datetime.datetime.now().hour)
    if hour>=4 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<16:
        
        speak("Good Afternoon!")
    elif hour>=16 and hour<20:
        speak("Good Evening!")
    else:
        speak("Hello!")
    speak("I am Devon. Please tell me how may I help you")

#The input command is taken by the device's microphone
def userCommand():
    mic = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)
    try:
        print("Recognizing...")
        command = mic.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
    except Exception as e:
        return "None"
    return command.lower()

#Main function
def tasks():
    command = userCommand()

    #Testing mic and speech
    if 'hello' in command:
        speak("Hello...I am Devon. Please tell me how may I help you")
    
    #Testing mic and speech
    elif 'how are you' in command:
        speak("I am fine...And you")
        you = userCommand()
        speak("Good to hear that...How may I help you?")

    #Says the current time
    elif 'the time' in command:
        strTime = datetime.datetime.now().strftime("%I %M %p")
        speak(f"The time is {strTime}")

    #Says the current date
    elif 'date today' in command:
        strDate = datetime.date.today()
        speak(f"Today's date is {strDate}")

    #Stores a reminder
    elif 'remember that' in command:
        command = command.replace("remember that","")
        speak("Done...I will remember that for you")
        rem = open("reminders.txt","a")
        rem.write(command)
        rem.close()
    
    #Tells the reminders
    elif 'reminders' in command:
        rem = open("reminders.txt","r")
        remi = rem.read()
        speak(f"You told me that {remi}")
        rem.close()

    #Tells a joke
    elif 'a joke' in command:
        joke = pj.get_joke(language='en')
        print(joke)
        speak(joke)

    #Browses Wikipedia
    elif 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia","")
        results = wikipedia.summary(command, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    #Opens youtube.com
    elif 'open youtube' in command:
        wb.open("https://www.youtube.com/")
        time.sleep(7)
        for click in ['tab','tab','tab','tab']:
            time.sleep(1)
            auto.press(click)
        speak("What are you searching for?")
        auto.write(str(userCommand()),interval=0.1)
        auto.press('enter')
        time.sleep(4)               
        for click in ['enter','k']:
            time.sleep(2)
            auto.press(click)  

    #Opens google.com
    elif 'open google' in command:
        wb.open("https://www.google.com/")
        time.sleep(5)
        speak("What are you searching for?")
        auto.write(str(userCommand()),interval=0.1)
        auto.press('enter')

    #Play Music
    elif 'play music' in command:
        os.system("spotify")
        time.sleep(7)
        auto.hotkey('ctrl','l')
        speak("Which song do you want me play?")
        auto.write(str(userCommand()),interval=0.1)
        for click in ['enter','pagedown','tab','enter','enter']:
            time.sleep(2)
            auto.press(click)
    
    #Sends WhatsApp message
    elif 'send a message in whatsapp' in command:
        speak("Whom do you want to send?")
        phnos = {
            #  Add your names as well as WhatsApp numbers in a dictionary format.
            #  Eg: "John":"+911111111111"
            "farooq":"+917401773395",
            "muqeem": "+919150768519",
            "kabir" : "+917200356474",
            "hussain": "+919629327633",
            "aashir" : "+917358728447"
        }
        phno = phnos[userCommand()]
        speak("What do you want to send?")
        text = userCommand()
        pw.sendwhatmsg_instantly(phno,text)

    #Closes the assistant
    elif 'bye' in command:
        speak("Thank you... It was my pleasure helping you")
        hour = int(datetime.datetime.now().hour)
        if hour>=20 and hour<4:
            speak("Good Night") 
        sys.exit()

if __name__ == '__main__':
    root = Tk()
    root.title("DEVON")
    root.iconbitmap("C:\\Users\\acer\\Documents\\programming\\devon\\asicon.ico")
    root.geometry("1000x700")
    root.configure(background='black')

    #User commands
    greetUser()
    
    # Visual Animations
    visual_label = Label(root, bg='black')
    visual_label.pack()
    play_visual = tkvideo("C:\\Users\\acer\\Documents\\programming\\devon\\visuals.mp4", visual_label, loop=1, size=(700,400))
    play_visual.play()
    
    #Description
    name_label = Label(root, text="D E V O N", font=("Arial Black",40), fg="#00bcd4", bg='black')
    name_label.pack()
    des_label = Label(root, text="I'm a Virtual Assistant How can I help you", font=("Verdana",20), fg="#324042", bg='black')
    des_label.pack()

    # Mic button
    mic_btn = PhotoImage(file="C:\\Users\\acer\\Documents\\programming\\devon\micbtn.png")
    mic_label = Label(image=mic_btn, bg='black')
    mic_button = Button(root, image=mic_btn, command= tasks, borderwidth=0, bg='black', activebackground='black')
    mic_button.pack()
    
    root.mainloop()
