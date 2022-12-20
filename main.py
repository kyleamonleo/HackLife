from open_ai import DaVincibot
from virtual_assistant import speak, listen

def main():
    print("Start")
    
    
    vini = DaVincibot(listen())
    speak(vini)
    speak("BREAK! Let me know if you need anything else, see you later")


    

if __name__ == "__main__":
    main()
