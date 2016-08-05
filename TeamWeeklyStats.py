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

# TODO add warning about exact name. FIX LINKS!!!!
message = """Hello {name}.

Check-in for this week started last Friday, and continues until Wednesday...
and it appears that you have not yet weighed in!

Please see the [Weigh-in thread] (https://www.reddit.com/r/loseit/comments/4fy7l5/challenge_spring_into_summer_week_1/) for details.
You can also go directly to the [Weigh-in form] (https://docs.google.com/forms/d/1oNgsBuziGwJY5imw7osmZZqu56gsZt0GCuFpkn-R7tE/viewform?c=0&w=1)

This is just a PM from a reminder program, if you need help, please contact one of the challenge admins: u/bookishgeek, u/axecutable, u/Mega-Starpuncher, and u/EosEnthusiast.
If you have a comment, please see the
[loseit_helper comment thread] (https://www.reddit.com/r/loseit/comments/4eqmo6/loseit_helper_discussion_thread/)

"""


def main():
    r = praw.Reddit(user_agent='Send message to loseit weight loss challenge '
                               'subscribers who have not weighed in by /u/jeffles2')
    username = input('Reddit username: ')
    password = input('Password: ')
    current_week = input('Week number:')
    message_title = 'Lose It - Week ' + str(current_week) + ' weigh in reminder'
    current_week = int(current_week)
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

    total = 0
    for entry in all_records:
        reddit_name = entry['Reddit username?']
        if reddit_name == '':  # No name
            continue
        team_subreddit = 'https://www.reddit.com/r/' + subreddits[entry['Team']]
        # print(reddit_name)

        weeks_not_entered = [entry['W1'], entry['W2'], entry['W3'],
                             entry['W4'], entry['W5'], entry['W6'],
                             entry['W7'], entry['W8'],
                             entry['W9'], entry['W10']].count('')
        weeks_entered = 10 - weeks_not_entered

        if weeks_entered + 2 < current_week:  # Miss two weeks max
            continue

        current_week_header = 'W' + str(current_week)
        if entry[current_week_header] != '':
            continue

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
            time.sleep(2)  # Max 30 messages per minute
        print("/u/{name} {team}".format(name=reddit_name, team=entry['Team']))
        total += 1
    print("")
    print("Total is ", total)

if __name__ == '__main__':
    main()
