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

CHALLENGE_SPREADSHEET_NAME = 'Spring into Summer Challenge'
subreddits = {'CROCUS': 'TeamCrocus',
              'THUNDERSTORM': 'TeamThunderstorm',
              'DAFFODIL': 'TeamDaffodil',
              'SEEDLING': 'TeamSeedling',
              'LADYBUG': 'TeamLadybug',
              'DUCKLING': 'TeamDuckling',
              'FAWN': 'TeamFawn',
              'ROBIN': 'Team_Robin',
              'HAYFEVER': 'TeamHayfever',
              'POLLEN': 'TeamPollen'}

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

Thank you for joining the Spring into Summer /r/loseit challenge.
Today is the first day!

If you want to update starting weight use the [Weigh-in form] (https://docs.google.com/forms/d/1HnyMYMGnv1p3o9piaUPdJIK75i7ZcFduB4jXqUsH06I/viewform?c=0&w=1) to enter your weight and name ({name}).
[Weigh-in thread] (https://www.reddit.com/r/loseit/comments/4ewliy/challenge_spring_into_summer_week_0/)

You are on Team {team}, which has its own [team subreddit] ({team_subreddit}) which you should check out and subscribe to.

You have until end of day Thursday each week to weigh in, but you should do it right away.

This is just a PM from a reminder program, if you have questions or comments, please see the
[loseit_helper comment thread] (https://www.reddit.com/r/loseit/comments/4eqmo6/loseit_helper_discussion_thread/)
"""


def main():
    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge subscribers who have not weighed in by /u/jeffles2')
    username = input('Reddit username: ')
    password = input('Password: ')
    message_title = 'Lose It - Spring Into Summer starts today!'
    send_email = input('Send email? (Y/N):')
    if send_email.upper() == 'Y':
        send_email = True
    else:
        send_email = False
    r.login(username, password, disable_warning=True)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    # service = discovery.build('drive', 'v2', http=http)

    gc = gspread.authorize(credentials)
    sheet = gc.open(CHALLENGE_SPREADSHEET_NAME)

    wks = sheet.get_worksheet(0)

    all_records = wks.get_all_records()

    hit = False
    total = 0
    for entry in all_records:
        reddit_name = entry['Reddit username?']
        if reddit_name == 'dirtywordplay90':
            hit = True
            continue
        if not hit:
            continue
        if reddit_name == '': #No name
            continue
        team_subreddit = 'https://www.reddit.com/r/' + subreddits[entry['Team']]
        # print(reddit_name)


        custom_message = message.format(name=reddit_name,
                                        team=entry['Team'],
                                        team_subreddit=team_subreddit)


        if send_email:
            try:
                r.send_message(reddit_name, message_title, custom_message)

            except praw.errors.InvalidUser:
                print("\n!!! ", reddit_name, " is an Invalid User")
                continue

            import time
            time.sleep(2)  #Max 30 messages per minute
        print("/u/{name} {team}".format(name=reddit_name, team=entry['Team']))
        total += 1
    print("")
    print("Total is ", total)

if __name__ == '__main__':
    main()