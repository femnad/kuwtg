# Package: kuwtg.obj


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

    def __init__(self, comment):
        user = comment['user']['login']
        body = comment['body']
        self._user = user
        self._body = body

    @property
    def user(self):
        return self._user

    @property
    def body(self):
        return self._body
