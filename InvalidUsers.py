from __future__ import print_function
import httplib2
import os
import gspread
import praw
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

def main():
    participants = {}
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    gc = gspread.authorize(credentials)
    sheet = gc.open("Spring into Summer Challenge")
    wks = sheet.get_worksheet(0)
    c3_name_list = wks.col_values(3)

    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    username = input('Enter your reddit username: ')
    password = input('Enter your password: ')
    r.login(username, password)


    for recipient in c3_name_list:
        if not recipient:
            continue
        if recipient == 'Reddit Username':
            continue

        try:
            user = r.get_redditor(recipient)
            user.link_karma
        except praw.errors.InvalidUser:
            print("\n", recipient)
        except praw.errors.NotFound:
            print("\n", recipient)


if __name__ == '__main__':
    main()