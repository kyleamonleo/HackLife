from open_ai import DaVincibot
from virtual_assistant import speak, listen

def main():
    print("Start")
    
    command = listen()
    vini = DaVincibot(command)
    speak(vini)


    

if __name__ == "__main__":
    main()
