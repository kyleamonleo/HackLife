from open_ai import DaVincibot
import datetime
from virtual_assistant import speak, listen
from google_calendar_api import get_date, get_events, authenticate_google, create_event

WAKE_UP = "leo"
CALENDAR_CALLS = {"calendar check", "calendar"}
CALENDAR_BOOKINGS = {"booking"}
OPEN_AI = {'question'}
SERVICE = authenticate_google()

def main():
    speak("Welcome my creator kyle amon")
    
    while True:
        print("start of loop")

        text = listen()
        # text = 'hey leo'

        if text.count(WAKE_UP)>0:
            print("caught wake up")
            speak("ready")
            # speak('Jah')

            
            text = listen()
            # text = 'booking'


            for phrase in CALENDAR_CALLS:
                if phrase in text.lower():
                    speak("checking calendar")
                    d = get_date(text)

                    speak(f"checking {d}")
                    
            # if d:
                    get_events(d, SERVICE)
                    speak("calendar search complete")
                    
                    continue
            # else:
                # speak("something with day and events is wonky")

            for phrase in CALENDAR_BOOKINGS:

                if phrase in text.lower():
                    speak("checking bookings")
                    d= get_date(text)
                    speak("what is the description?")
                    summary = listen()
                    # summary = "workout"
                    speak("what is the location?")
                    
                    location = listen()

                    
                    create_event(SERVICE,summary, location, d, d)

                    speak('booking complete')
                
                    continue
            
            for phrase in OPEN_AI:
                if phrase in text.lower():
                    speak('what is your question')
                    text = listen()
                    # text = "how tall is the tallest building"
                    answer = DaVincibot(text)
                    speak(answer)
                    speak("question search complete")
                    

    
    # vini = DaVincibot(listen())
    # speak(vini)


    

if __name__ == "__main__":
    main()
