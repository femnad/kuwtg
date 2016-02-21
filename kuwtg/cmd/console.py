# Package kuwtg.cmd.console
import requests
import sys

from kuwtg.api.consumer import GithubAPIConsumer
from kuwtg.obj import GithubNotification
from kuwtg.ui.notifications import NotificationsList

def main():
    arguments = sys.argv
    if len(arguments) == 2:
        access_token = arguments[1]
        api_consumer = GithubAPIConsumer()
        notifications = api_consumer.get_notifications(access_token)
        notifications_list = [GithubNotification(
            notification['id'], notification['subject']['type'],
            notification['subject']['title'], notification['subject']['url'])
                              for notification in notifications]
        notification_lister = NotificationsList(notifications_list)
        notification_lister.display_list()
        notification_lister.loop()
        exit(0)
    else:
        print("Usage ./kuwtg <access-token>")
