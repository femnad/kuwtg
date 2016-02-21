# Package: kuwtg.obj

class GithubNotification(object):

    def __init__(self, notification_id, notification_type, title, url):
        self._notification_id = notification_id
        self._notification_type = notification_type
        self._title = title
        self._url = url

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
