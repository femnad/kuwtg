# Package kuwtg.cmd.console
import requests
import sys

from kuwtg import Notification
from kuwtg.ui import ListScroller


NOTIFICATIONS_ENDPOINT = 'https://api.github.com/notifications'

def get_notifications(access_token):
    response = requests.get(
        NOTIFICATIONS_ENDPOINT,
        headers={
            "authorization": "token {}".format(access_token),
            "user-agent": "femnad/kuwtg"
        })
    raw_notifications = response.json()
    notifications = [Notification(
        notification['id'],
        notification['subject']['title'],
        notification['subject']['url'],
        notification['subject']['latest_comment_url'],
        notification['subject']['type'],

    ) for notification in raw_notifications]
    return notifications

def main():
    arguments = sys.argv
    if len(arguments) == 2:
        access_token = arguments[1]
        titles = get_notifications(access_token)
        list_scroller = ListScroller(titles)
        list_scroller.initialize_list()
        list_scroller.loop()
        exit(0)
    else:
        print("Usage ./kuwtg <access-token>")
