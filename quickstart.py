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

As you may know, you signed up for the /r/loseit weight loss challenge, and you have been assigned to
**Team Icicle**! Week 3 weigh-in is now active. Please go to the [link for the week 3 weigh ins ](http://goo.gl/forms/Abyj6crsw7)
and enter your reddit user name ({name}), and your current weight.

Gained weighed this week? Me too! Please log it anyway.
Lost weight this week? Awesome! Keep up the good work.
Have questions? Go to our team subreddit, /r/teamicicle, or /r/loseit and ask away.

"""


last_sent = ""
skip_list = ['Gigi tweekz', 'TourmanlineTart', 'ThunderCatsServent', 'Pirite', 'lositinSD', 'JohnS1821', 'evitable_betrayal', 'Doktor_Rutherz']

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
    team_list = wks.range('A1200:A2000')
    name_list = wks.range('B1200:B2000')
    week1_weight_list = wks.range('W1200:W2000')
    week2_weight_list = wks.range('X1200:X2000')
    week3_weight_list = wks.range('Y1200:Y2000') #TODO Currently week3
    total = 0
    for team, name, weight1, weight2, weight3 in zip(team_list, name_list, week1_weight_list, week2_weight_list, week3_weight_list ):
        if weight3.value == '' and team.value == 'TEAM ICICLE':
            if weight1.value == '' and weight2.value == '':
                continue

            recipient = name.value
            if last_sent and recipient.lower() < last_sent.lower():
                #print ("Skipping ", recipient)
                continue

            if recipient in skip_list:
                #print (recipient, " is in the skip list")
                continue
            custom_message = message.format(name=recipient)
            if False: #TODO up date to current week column and message title below
                try:
                    r.send_message(recipient, 'Lose It - Week 3 weigh in', custom_message)
                except praw.errors.InvalidUser:
                    print ("\n!!! ", recipient, " is an Invalid User")
                    continue

                import time
                time.sleep(2)
            print ("/u/{name} ".format(name=name.value), end=" ")
            total +=1
    print ("")
    print ("Total is ", total)

if __name__ == '__main__':
    main()