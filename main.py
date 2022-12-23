from open_ai import DaVincibot
from virtual_assistant import speak, listen
from google_calendar_api import get_date, get_events, authenticate_google, create_event

WAKE_UP = "haley"
CALENDAR_CALLS = {"what do i have", "calendar check"}
CALENDAR_BOOKINGS = {"make a booking", "add to my schedule", "calendar booking"}
SERVICE = authenticate_google()

def main():
    speak("Welcome my creator kyle amon")
    
    while True:
        print("start of loop")

        text = listen()

        if text.count(WAKE_UP)>0:
            print("caught wake")
            speak("ready sir")

            text = listen()


            for phrase in CALENDAR_CALLS:
                if phrase in text.lower():
                    d = get_date(text)
            # if d:
                    get_events(d, SERVICE)
                    
                    continue
            # else:
                # speak("something with day and events is wonky")
            for phrase in CALENDAR_BOOKINGS:
                if phrase in text.lower():
                    d= get_date(text)
                    speak("what is your summary?")
                    summary = listen()
                    location = "CPT"

                    
                    create_event(SERVICE,summary, location, d, d)
                
                    continue

    
    # vini = DaVincibot(listen())
    # speak(vini)


    

if __name__ == "__main__":
    main()
