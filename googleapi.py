
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import requests
import json
import socket
import random

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    #Checker for if you want to use past stored credentials
    override = 2
    print(override)
                     
    
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid or override == 2:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    days = 15
    dataList = []
    prev = None
    dayData = []
    i=0
    #iterating over each event in the given data pull from google cal
    for event in events:
        #Grabs the start date and time for the event
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start)
        #condenses the start variable to just the date value in the format YYYY-MM-DD
        time = start[11:16]
        time = time.replace(':', '')
        time = int(time[:2])
        start = start[:10]
        summary = str(event['summary']) #Event Title
        location = str(event['location']) #Event Location
        if i > days: #breaks loop as i reaches wanted num of days
            break
        if start != prev: #Checks for the current event and its predecessor having the same date or not
            #if not the same date, starts a new day list
            i+=1 #i is the day counter to reach the desired num of days
            dataList.append(dayData) #appends the last days list to the main data return
            dayData = [] #sets the new day data to a blank list
            evDetailList = [location, summary, time] #sets the event details to its name and sum
            dayData.append(evDetailList) #appends event to day
            evDetailList = [] #clears event list
            prev = start #sets prev day to current
        else:
            #literally same as previous just not moving forward in days
            evDetailList = [location,summary, time]
            dayData.append(evDetailList)
            evDetailList = []
        #print(i, 'i')
    dataList.pop(0)
    #print(dataList)
    return dataList


if __name__ == '__main__':
    print(main())
                
        

