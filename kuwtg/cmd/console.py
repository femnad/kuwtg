# Package kuwtg.cmd.console
from kuwtg.api.consumer.github_api_consumer import GithubAPIConsumer
from kuwtg.api.consumer.exceptions import ResponseNotOkException
from kuwtg.config.configuration import Configuration
from kuwtg.obj import GithubNotification
from kuwtg.ui.notification_list import NotificationList


def main():
    try:
        configuration = Configuration()
        api_consumer = GithubAPIConsumer(configuration.access_token)
        notifications = api_consumer.get_notifications()
        notifications_list = [GithubNotification(notification)
                              for notification in notifications]
        notification_lister = NotificationList(notifications_list)
        notification_lister.draw()
    except ResponseNotOkException as e:
        print("Unexpected response when accessing Github:")
        print(e)
        exit(1)
