from __future__ import print_function
import httplib2
import os
import gspread
import praw

# https://github.com/burnash/gspread

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

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://spreadsheets.google.com/feeds https://docs.google.com/feeds'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
LOSEIT_ID = '1-EKK8u-6lP7eaaMSmuPeadhg44rgyhkf0EMXPo7wHgw'

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
    print (credential_path)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

message = """Hello {name}.

Week 9 final check-ins have been active since last Friday, but you have not weighed in yet!
Please go to the [link for the week 9 weigh ins ](http://goo.gl/forms/aJnKJjTVGW)
and enter your reddit user name ({name}), and your current weight.
You have until end of day Thursday to weigh in for Week 9.

***ALSO-> You may also be interested in the next 2016 New Year, New you challenge. [Google form] (http://goo.gl/forms/VnWeWOBl14) or [Reddit post] (https://www.reddit.com/r/loseit/comments/401074/challenge_as_the_winter_2015_challenge_comes_to_a/)

This is just a PM from a reminder program written by jeffles2, I am not affiliated with the actual contest organizers.. just a zealous Icicle.

"""


skip_list = ['Gigi tweekz', 'TourmanlineTart', 'ThunderCatsServent', 'Pirite', 'lositinSD', 'JohnS1821', 'evitable_betrayal', 'Doktor_Rutherz', 'Brick_Pudding']

def main():
    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    username = raw_input('Enter your reddit username: ')
    password = raw_input('Enter your password: ')
    r.login(username, password)


    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    try:
        file = service.files().get(fileId=LOSEIT_ID).execute()

        print('Title: %s' % file['title'])
        print('MIME type: %s' % file['mimeType'])
        #for k,v in file.iteritems():
        #    print (k,v)
        selflink = file['selfLink']
        print ('selflink %s' % selflink)
#        import pdb;pdb.set_trace()
#        print ('Export Links %s' % file['exportLinks'])
    except errors.HttpError, error:
        print('An error occurred: %sfor k,v ' % error)

    gc = gspread.authorize(credentials)
    sheet = gc.open("/r/loseit Holiday 2015 Challenge (Responses)")


    wks = sheet.get_worksheet(1)
    # import pdb; pdb.set_trace()
    # for row_num in range(wks.row_count):
    #     row = wks.row_values(row_num)
    #     print (row)
    # exit()
    team_list = wks.range('A2:A3500')
    name_list = wks.range('B2:B3500')
    week1_weight_list = wks.range('AC2:AC3500')
    week2_weight_list = wks.range('AD2:AD3500') #TODO Currently week
    week3_weight_list = wks.range('AE2:AE3500') #TODO Currently week
    total = 0
    for team, name, weight1, weight2, weight3 in zip(team_list, name_list, week1_weight_list, week2_weight_list, week3_weight_list ):
        if weight3.value == '' and team.value != 'TEAM ICICLE':
            if weight1.value == '' and weight2.value == '':
                continue

            recipient = name.value

            if recipient in skip_list:
                #print (recipient, " is in the skip list")
                continue
            custom_message = message.format(name=recipient)
            if True: #TODO up date to current week column and message title below
                try:
                    r.send_message(recipient, 'Lose It - Week 9 weigh in reminder', custom_message)
                except praw.errors.InvalidUser:
                    print ("\n!!! ", recipient, " is an Invalid User")
                    continue

                import time
                time.sleep(2)
            print ("/u/{name} {team}".format(name=recipient, team=team.value))
            total +=1
    print ("")
    print ("Total is ", total)

if __name__ == '__main__':
    main()