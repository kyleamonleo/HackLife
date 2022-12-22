from open_ai import DaVincibot
from virtual_assistant import speak, listen
from google_calendar_api import get_date, get_events, authenticate_google
CALENDAR_CALLS = {"jarvy, what do i have", "calendar check"}

def main():
    speak("Welcome I am jarvy, my creator kyle amon has given me many capabilities please feel free to get involved.")
    SERVICE = authenticate_google()
    print("Start")

    text = listen()
    for p in CALENDAR_CALLS:
        if p in text.lower():
            d = print(get_date(text))
            # if d:
            get_events(d, SERVICE)
            # else:
                # speak("something with day and events is wonky")

    
    # vini = DaVincibot(listen())
    # speak(vini)


    

if __name__ == "__main__":
    main()
