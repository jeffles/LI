import gspread
import httplib2
import os
import praw

# https://github.com/burnash/gspread

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://spreadsheets.google.com/feeds https://docs.google.com/feeds'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
LOSEIT_ID = '1-EKK8u-6lP7eaaMSmuPeadhg44rgyhkf0EMXPo7wHgw'

CHALLENGE_SPREADSHEET_NAME = 'The Summer Challenge 2016'
subreddits = {'BUMBLEBEE': 'TeamBumblebee'}

def get_credentials():
    """Gets valid user credentials from storage for google.

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

message = """Hello {name}.

Thank you for joining the Summer 2016 /r/loseit challenge.

You are on Team BumbleBee!
Your team captains /u/thegirlfrompa and /u/TaylorKun would like to invite
you to join and subscribe to the
[Team BumbleBee subreddit] (https://www.reddit.com/r/TeamBumblebee/).

We will be having daily discussions in a fun, friendly and encouraging
environment.
Come on over and get to know your team members!
Share your story, help out someone who is struggling, tell us all
about your latest victory or just say hello.

We are so glad you are with us on Team BumbleBee!

"""


def main():
    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge '
                               'subscribers who have not weighed in '
                               'by /u/jeffles2')
    r.login()


    # r.refresh_access_information()
    # r.set_oauth_app_info(client_id=REDDIT_CLIENT_ID,
    #                      client_secret=REDDIT_CLIENT_SECRET,
    #                      redirect_url='http://127.0.0.1:65010/authorize_callback')

    message_title = 'Lose It - Summner Challenge!'
    send_email = input('Send email? (Y/N):')
    if send_email.upper() == 'Y':
        send_email = True
    else:
        send_email = False

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    # service = discovery.build('drive', 'v2', http=http)

    gc = gspread.authorize(credentials)
    sheet = gc.open(CHALLENGE_SPREADSHEET_NAME)

    wks = sheet.get_worksheet(1)

    all_records = wks.get_all_records()

    # hit = False
    total = 0
    for entry in all_records:
        reddit_name = entry['Reddit username?']
        reddit_team = entry['TEAM']
        if reddit_team != 'BUMBLEBEE':
            continue
        # if reddit_name == 'dirtywordplay90':
        #     hit = True
        #     continue
        # if not hit:
        #     continue
        if reddit_name == '':  # No name
            continue
        team_subreddit = 'https://www.reddit.com/r/' + subreddits[reddit_team]
        # print(reddit_name)

        custom_message = message.format(name=reddit_name,
                                        team=reddit_team,
                                        team_subreddit=team_subreddit)

        if send_email:
            try:
                r.send_message(reddit_name, message_title, custom_message)

            except praw.errors.InvalidUser:
                print("\n!!! ", reddit_name, " is an Invalid User")
                continue

            import time
            time.sleep(2)  # Max 30 messages per minute
        print("/u/{name} {team}".format(name=reddit_name, team=reddit_team))
        total += 1
    print("")
    print("Total is ", total)

if __name__ == '__main__':
    main()
