# Package: kuwtg.api.consumer
import requests


class GithubAPIConsumer(object):

    NOTIFICATIONS_ENDPOINT = 'https://api.github.com/notifications'

    def _get_json_response(self, url, headers=None):
        response = requests.get(url, headers=headers)
        return response.json()

    def get_notifications(self, access_token):
        return self._get_json_response(
            self.NOTIFICATIONS_ENDPOINT, headers={
                "authorization": "token {}".format(access_token),
                "user-agent": "femnad/kuwtg"
            })

    def get_notification_body(self, url):
        notification = self._get_json_response(url)
        body = notification['body']
        if '_links' in notification:
            links = notification['_links']
        else:
            links = None
        return body, links

    def get_comments(self, url):
        raw_comments = self._get_json_response(url)
        comments = [{"user": comment['user']['login'],
                     "comment": comment['body']} for comment in raw_comments]
        return comments
