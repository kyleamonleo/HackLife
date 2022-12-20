import os 
import time 
import playsound
import speech_recognition as sr
import gtts 
num =0


'''
function for assistant to speak 
args : prompt assistant to say the text 
save mp3 file in audio folder
'''
def speak(text):
    global num
    tts = gtts.gTTS(lang="en", text=text)
    
    num =+ 1
    tts.save(f"./audio/voice{num}.mp3")
    filename = f"./audio/voice{num}.mp3"
    playsound.playsound(filename)

# speak("hello hello this is what im talking about the company")
'''
function to make listen for commands
'''
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Recognize the speech in the audio
    try:
    # Print the recognized text
        recogText = r.recognize_google(audio)
        print(recogText)
        # speak("you said: "+recogText)
    except sr.UnknownValueError:
    # If the speech is unrecognizable, print an error message
        speak("This is jarvy, Sorry, I could not understand what you said.")
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
    # If there is an error with the speech recognition service, print an error message
        speak("This is jarvy, Sorry, there was an error with the speech recognition service.")        
        print("Sorry, there was an error with the speech recognition service: {0}".format(e))


        return recogText

# listen()