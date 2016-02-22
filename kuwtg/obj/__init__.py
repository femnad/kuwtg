# Package: kuwtg.obj

class GithubNotification(object):

    def __init__(self, notification_id, notification_type, title, url, repo_name):
        self._notification_id = notification_id
        self._notification_type = notification_type
        self._title = title
        self._url = url
        self._repo_name = repo_name

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
