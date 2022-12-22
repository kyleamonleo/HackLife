from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz


import virtual_assistant 


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXT = ["rd","th","st","nd"]


# If modifying these scopes, delete the file token.json.


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/kyle/sideProjects/python/virtualAssistant/HackLife/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    
    service = build('calendar', 'v3', credentials=creds)

    return service





def get_events(day, service):

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                    singleEvents=True,
                                    orderBy='startTime').execute()
    
    events = events_result.get('items', [])

    if not events:
        virtual_assistant.speak('No upcoming events found.')
    
    else:
        virtual_assistant.speak(f"you have {len(events)} events on this day")


        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            
            start_time = str((start.split("T")[1]).split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)
                start_time = start_time+"pm"

            virtual_assistant.speak(event["summary"])+" at "+ start_time



def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    words = text.split()

    for i, word in enumerate(words):
        if word in MONTHS:
            month = MONTHS.index(word)+1

        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXT:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass


    # check if the word next (indicating the future)

        if word == "next" and i < len(words)-1:
            if words[i+1] in DAYS:
                day_of_week = DAYS.index(words[i+1])
                day_of_week += 7

            elif words[i+1] in MONTHS:
                month = MONTHS.index(words[i+1]) +1
                if month <= today.month:
                    year += 1
            elif words[i+1].isdigit():
                day = int(words[i+1])
                if month == today.month and day < today.day:
                    month += 1
                    if month > 12:
                        month =1
                        year += 1
            
    
    if month < today.month and month != -1:
        year = year +1

    if day< today.day and month == -1 and day != -1:
        month = month + 1
    
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()

        dif = day_of_week - current_day_of_week

        if dif <0 : 
            dif += 7
            if text.count("next")>=1:
                dif += 7

        return today + datetime.timedelta(dif)
    
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)


# CALENDAR_CALLS = {"jarvy, what do i have", "jarvy, calendar check"}
# text = virtual_assistant.listen()
# for p in CALENDAR_CALLS:
#     if p in text.lower():
#         d = print(get_date(text))
#         if d:
#             get_events(d, authenticate_google())
#         else:
#             virtual_assistant.speak("something with day and events is wonky")

s = authenticate_google()
# t=virtual_assistant.listen()
d = get_date("next friday")
get_events(d,s)