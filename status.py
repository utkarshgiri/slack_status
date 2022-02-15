#!/Users/utkarshgiri/miniforge3/bin/python


''' A simple script to set slack status based on whether you are connected to home or office network. 
It can be set so as to run automatically whenever your network connection is reset '''

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ['SLACK_TOKEN'])

result = os.popen('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I').read()

for line in result.split('\n'):
    if line.strip()[:4] == 'SSID':
        ssid = line.strip()[5:].strip()

statuses = {
                os.environ['HOME_NETWORK']: 'Working from Home',
                os.environ['OFFICE_NETWORK']: '@Chamberlin'
           }

status = statuses[ssid]
try:
    response = client.users_profile_set(profile={"status_text": statuses[ssid], "status_emoji": ":mountain_railway:"})
except KeyError as e:
    response = client.users_profile_set(profile={"status_text": 'Cafe', "status_emoji": ":mountain_railway:"})
except SlackApiError as e:
    pass
