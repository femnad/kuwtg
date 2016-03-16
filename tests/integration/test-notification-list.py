#!/usr/bin/env python3
import json

from kuwtg.obj import GithubNotification
from kuwtg.ui.notification_list import NotificationList

if __name__ == "__main__":
    with open('test-notifications.json') as notification_list_file:
        raw_notifications = notification_list_file.read()
        notifications = json.loads(raw_notifications)
        notification_objects = [GithubNotification(notification)
                                for notification in notifications]
        notification_list = NotificationList(notification_objects)
        notification_list.draw()
