# Package: kuwtg.obj
import datetime


class GithubNotification(object):

    def __init__(self, notification):
        subject = notification['subject']
        repository = notification['repository']
        self._notification_id = notification['id']
        self._notification_type = subject['type']
        self._title = subject['title']
        self._url = subject['url']
        self._repo_name = repository['full_name']

    @property
    def notification_id(self):
        return self._notification_id

    @property
    def notification_type(self):
        return self._notification_type

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def repo_name(self):
        return self._repo_name


class GithubComment(object):

    INPUT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
    OUTPUT_DATE_FORMAT = '%F %T'

    def __init__(self, comment):
        if 'user' in comment:
            user_key = 'user'
        else:
            user_key = 'author'
        user = comment[user_key]['login']
        body = comment['body']
        self._user = user
        self._body = body
        created_at = comment['created_at']
        self._created_at = datetime.datetime.strptime(
            created_at, self.INPUT_DATE_FORMAT)

    @property
    def user(self):
        return self._user

    @property
    def body(self):
        return self._body

    @property
    def created_at(self):
        return self._created_at.strftime(self.OUTPUT_DATE_FORMAT)
