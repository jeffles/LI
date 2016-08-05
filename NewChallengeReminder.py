from __future__ import print_function
import httplib2
import gspread
import os
import praw
import re
import time
from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# https://github.com/burnash/gspread

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://spreadsheets.google.com/feeds https://docs.google.com/feeds'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
LOSEIT_ID = '1-EKK8u-6lP7eaaMSmuPeadhg44rgyhkf0EMXPo7wHgw'

MESSAGE = """Hello {name}.

[Spring into Summer Challenge] (https://www.reddit.com/r/loseit/comments/4d68k1/challenge_spring_into_summer_official_signup/)
 is now accepting sign ups.
My program sees that you participated in one of the last two challenges, but have not yet signed up for Spring Into Summer.
If you are interested, please see the [Reddit post] (https://www.reddit.com/r/loseit/comments/4d68k1/challenge_spring_into_summer_official_signup/)

This is just a PM from a reminder program. I am not affiliated with the actual contest organizers... just a zealous programmer.

I've had some technical problems and I think they are resolved, but my apologies if you received this message twice.
"""


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
                                   'drive-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
    return credentials

def main():
    participants = {}
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    gc = gspread.authorize(credentials)

    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    username = input('Enter your reddit username: ')
    password = input('Enter your password: ')
    r.login(username, password)


    sheet = gc.open("Spring into Summer Challenge")
    wks = sheet.get_worksheet(0)
    c3_name_list = wks.range('C2:C3500')
    upper_name_list = []
    for i in range(len(c3_name_list)):
        name = c3_name_list[i].value
        if not name:
            continue
        if name.upper() in upper_name_list:
            continue
        upper_name_list.append(name.upper().strip())

    print(len(upper_name_list), " have registered already")
    messages = r.get_content('https://www.reddit.com/message/sent/', '', 1000)
    total = 0
    for message in messages:
        total += 1
        if message.dest.upper() in upper_name_list:
            continue
        upper_name_list.append(message.dest.upper().strip())


    print("I sent ", total, " message for ", len(upper_name_list), " total")

    sheet = gc.open("/r/loseit Holiday 2015 Challenge (Responses)")
    wks = sheet.get_worksheet(1)
    c1_name_list = wks.range('B2:B3500')
    c1_lost_percent = wks.range('S2:S3500')
    c1_lost_weight = wks.range('U2:U3500')
    c1_to_goal = wks.range('V2:V3500')
    c1_week = list()
    c1_week.append(wks.range('W2:W3500'))
    c1_week.append(wks.range('X2:X3500'))
    c1_week.append(wks.range('Y2:Y3500'))
    c1_week.append(wks.range('Z2:Z3500'))
    c1_week.append(wks.range('AA2:AA3500'))
    c1_week.append(wks.range('AB2:AB3500'))
    c1_week.append(wks.range('AC2:AC3500'))
    c1_week.append(wks.range('AD2:AD3500'))
    c1_week.append(wks.range('AE2:AE3500'))
    for i in range(len(c1_name_list)):
        weeks_missed = 0        for week_num in range(9):
            if not c1_week[week_num][i].value:
                weeks_missed += 1
        name = c1_name_list[i].value
        if name.upper().strip() in upper_name_list:
            # print ('Skipping', name)
            continue
        if weeks_missed > 7:
            continue
        participants[name] = {'lost_percent_1': c1_lost_percent[i].value,
                              'lost_weight_1': c1_lost_weight[i].value,
                              'to_goal_1': c1_to_goal[i].value,
                              'weeks_missed_1': weeks_missed}

    sheet = gc.open("NEW YEAR, NEW YOU 2016 CHALLENGE - Master Spreadsheet")
    wks = sheet.get_worksheet(0)
    c2_name_list = wks.range('D2:D1945')

    c2_lost_percent = wks.range('R2:R1945')
    c2_lost_weight = wks.range('T2:T1945')
    c2_to_goal = wks.range('U2:U1945')
    c2_week = list()
    c2_week.append(wks.range('V2:V1945'))
    c2_week.append(wks.range('W2:W1945'))
    c2_week.append(wks.range('X2:X1945'))
    c2_week.append(wks.range('Y2:Y1945'))
    c2_week.append(wks.range('Z2:Z1945'))
    c2_week.append(wks.range('AA2:AA1945'))
    c2_week.append(wks.range('AB2:AB1945'))
    c2_week.append(wks.range('AC2:AC1945'))
    c2_week.append(wks.range('AD2:AD1945'))
    c2_week.append(wks.range('AE2:AE1945'))
    for i in range(len(c2_name_list)):
        weeks_missed = 0
        for week_num in range(10):
            if not c2_week[week_num][i].value:
                weeks_missed += 1
        name = c2_name_list[i].value
        if name.upper().strip() in upper_name_list:
            # print ('Skipping', name)
            continue
        if weeks_missed > 8:
            continue
        if not c2_name_list[i].value in participants:
            participants[name] = {}
        participants[name]['lost_percent_2'] = c2_lost_percent[i].value
        participants[name]['lost_weight_2'] = c2_lost_weight[i].value
        participants[name]['to_goal_2'] = c2_to_goal[i].value
        participants[name]['weeks_missed_2'] = weeks_missed

    total = 0
    print('Mailing to this many ->', len(participants))
    for recipient in sorted(participants):
        if not recipient:
            continue
        if re.search('^[/\-_A-Za-m0-9]', recipient):
            continue
        print(recipient)
        custom_message = MESSAGE.format(name=recipient)
        if True: #TODO up date to current week column and message title below
            try:
                r.send_message(recipient, 'Spring into Summer /r/loseit challenge is open!', custom_message)
            except praw.errors.InvalidUser:
                print("\n!!! ", recipient, " is an Invalid User")
                continue
            except praw.errors.APIException:
                print("\n!!! ", recipient, " caused an API Exception")
                continue

            time.sleep(2)
        total +=1
    print ("")
    print ("Total is ", total)

if __name__ == '__main__':
    main()