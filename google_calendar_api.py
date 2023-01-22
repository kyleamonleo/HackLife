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

# https://www.googleapis.com/auth/calendar

SCOPES = ['https://www.googleapis.com/auth/calendar']
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
                'credentials.json', SCOPES)
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
        virtual_assistant.speak(f"you have {len(events)} events on this day. Collecting events")


        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            
            start_time = str((start.split("T")[1]).split("-")[0])

            end_time = str((start.split("T")[1]).split("-")[1])
            


            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12) + start_time.split(":")[1]
                start_time = start_time+"pm"

            virtual_assistant.speak(f'{event["summary"]}" at "{start_time}" to "{end_time}')



def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    
    print(today)

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    hour = -1
    minute = -1
    am_pm = "am"

    words = text.split()

    for i, word in enumerate(words):
        if word in MONTHS:
            month = MONTHS.index(word)+1

        elif word in DAYS:
            day_of_week = DAYS.index(word)
        
        elif word.isdigit():
            if hour == -1:
                hour = int(word)
            else:
                minute = int(word)

            # day = int(word)
        
        elif word == "am" or word == "pm":
            am_pm = word        

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
    
    
    # if we have a day in the week, use that determine the date

    # if month == -1 and day == -1 and day_of_week != -1:
    if day_of_week > -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif <0 : 
            dif += 7
            if text.count("next")>=1:
                dif += 7

        return today + datetime.timedelta(dif)
    
    
    # if we dont have a day of the week, use the day and month we have

    # if month == -1 or day == -1:
        # return None
    if day > -1 and month > -1:
        if hour < 0:
            hour = 0
        if minute < 0:
            minute = 0
        
        # adjust for PM

        if am_pm == "pm":
            if hour < 12:
                hour += 12

        return datetime.datetime(year, month,day, hour, minute)

        


    return today






def create_event(service, summary, location, start_time, end_time):
    
# 2015-05-28T09:00:00-07:00

#     d=get_date('next friday')
# # print(d)
# print(datetime.datetime.combine(d,datetime.datetime.min.time()).isoformat('T', 'seconds'))


    s = datetime.datetime.combine(start_time,datetime.datetime.min.time()).isoformat('T', 'seconds')
    e = datetime.datetime.combine(end_time,datetime.datetime.max.time()).isoformat('T', 'seconds')
    event = {
    'summary': 'virtual assistant ling',
    'location': location,
    'description': summary,
    
    'start': 
    {
        'dateTime': s,
        'timeZone': 'UTC',
    },

    # '2015-05-28T17:00:00-07:00'
    'end': {
        'dateTime': e,
        'timeZone': 'UTC',
    },
    
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
        {'email': 'test1@example.com'},
        {'email': 'test2@example.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }


    # event = {
    #     'summary': 'Virtual Assistant Ling',
    #     'location': location,
    #     'description': summary,
    #     'start': {
    #         'dateTime': start_time,
    #         'timeZone': 'UTC',
    #     },
    #     'end': {
    #         'dateTime': end_time,
    #         'timeZone': 'UTC',
    #     },
    #     'reminders': {
    #         'useDefault': True
    #     },
    # }

    event = service.events().insert(calendarId='primary', body=event).execute()

    # print(f"Event created: {event.get('htmlLink')}")
    print('Event created: %s' % (event.get('htmlLink')))



# CALENDAR_CALLS = {"jarvy, what do i have", "jarvy, calendar check"}
# text = virtual_assistant.listen()
# for p in CALENDAR_CALLS:
#     if p in text.lower():
#         d = print(get_date(text))
#         if d:
#             get_events(d, authenticate_google())
#         else:
#             virtual_assistant.speak("something with day and events is wonky")

# s = authenticate_google()
# # t=virtual_assistant.listen()
# d = get_date("next friday")
# get_events(d,s)