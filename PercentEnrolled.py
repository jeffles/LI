import httplib2
import gspread
import os
import praw
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

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
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run(flow, store)
    return credentials


def main():
    credentials = get_credentials()
    credentials.authorize(httplib2.Http())

    gc = gspread.authorize(credentials)

    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    username = input('Enter your reddit username: ')
    password = input('Enter your password: ')
    r.login(username, password, disable_warning=True)

    sheet = gc.open("Spring into Summer Challenge")
    wks = sheet.get_worksheet(1)
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
    enrolled = 0
    for message in messages:
        total += 1
        if message.dest.upper() in upper_name_list:
            enrolled += 1
            continue
        upper_name_list.append(message.dest.upper().strip())

    print("I sent ", total, " message and ", enrolled, " enrolled")


if __name__ == '__main__':
    main()
