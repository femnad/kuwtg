# Package: kuwtg.api.consumer
import requests

from kuwtg.api.consumer.exceptions import ResponseNotOkException
from kuwtg.obj import GithubComment


class GithubAPIConsumer(object):

    NOTIFICATIONS_ENDPOINT = 'https://api.github.com/notifications'

    def _get_json_response(self, url, headers=None):
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        else:
            raise ResponseNotOkException(response.text)

    def get_notifications(self, access_token):
        return self._get_json_response(
            self.NOTIFICATIONS_ENDPOINT, headers={
                "authorization": "token {}".format(access_token),
                "user-agent": "femnad/kuwtg"
            })

    def _get_comments(self, url):
        raw_comments = self._get_json_response(url)
        comments = [GithubComment(comment) for comment in raw_comments]
        return comments

    def get_notification_body(self, url):
        notification = self._get_json_response(url)
        starter_comment = GithubComment(notification)
        comments_url = notification['comments_url']
        comments = self._get_comments(comments_url)
        return starter_comment, comments
