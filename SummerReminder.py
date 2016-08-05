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
CHALLENGE_SPREADSHEET_NAME = 'The Summer Challenge 2016'

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

message = """Hello {name}

Check-in for this week started last Friday, and continues until Wednesday...
and it appears that you have not yet weighed in!

Please see the [Weigh-in thread] (https://www.reddit.com/r/loseit/comments/4v6def/challenge_the_summer_challenge_2016_week_1/) for details.
You can also go directly to the [Weigh-in form] (https://docs.google.com/forms/d/e/1FAIpQLSeHeBPueWWtCiwWBSU_NK2Dd7SaB55hCmLUW0jOL7vjpPzxdw/viewform?c=0&w=1).

This is just a PM from a reminder program, if you need help, please [contact one of the challenge admins] (https://www.reddit.com/message/compose/?to=/r/LoseitChallengeAdmin)

"""

def main():
    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    r.login()

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
    except errors.HttpError as error:
        print('An error occurred: %sfor k,v ' % error)

    gc = gspread.authorize(credentials)
    sheet = gc.open(CHALLENGE_SPREADSHEET_NAME)


    wks = sheet.get_worksheet(1)
    # import pdb; pdb.set_trace()
    # for row_num in range(wks.row_count):
    #     row = wks.row_values(row_num)
    #     print (row)
    # exit()
    team_list = wks.range('B2:B2114')
    name_list = wks.range('C2:C2114')
    week0_weight_list = wks.range('L2:L2114')
    week1_weight_list = wks.range('V2:V2114')

    total = 0
    send = False
#    for team, name, weight1, weight2, weight3 in zip(team_list, name_list, week1_weight_list, week2_weight_list, week3_weight_list ):
    for team, name, weight0, weight1 in zip(team_list, name_list, week0_weight_list, week1_weight_list):
        if weight0.value == '':
            continue
        if weight1.value != '':
            continue
        # if weight3.value == '' and team.value != 'TEAM ICICLE':
        #     if weight1.value == '' and weight2.value == '':
        #         continue

        recipient = name.value

        custom_message = message.format(name=recipient)

        if send:  # TODO up date to current week column and message title below
            try:
                r.send_message(recipient, 'Lose It - Week 1 weigh in reminder', custom_message)
            except praw.errors.InvalidUser:
                print("\n!!! ", recipient, " is an Invalid User")
                continue
            except praw.errors.APIException:
                print("\n!!! ", recipient, " is a really Invalid User and broke the API")
                continue

            import time
            time.sleep(2)

        if recipient == 'clndstnkim':
            send = True
        print ("/u/{name} {team}".format(name=recipient, team=team.value))
        total +=1
    print ("")
    print ("Total is ", total)

if __name__ == '__main__':
    main()