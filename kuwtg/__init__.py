# Package: kutwg

class Notification(object):

    def __init__(self, notification_id=None, title=None, url=None,
                 latest_comment_url=None, notification_type=None):
        self._id = notification_id
        self._title = title
        self._notification_type = notification_type
        self._url = url
        self._latest_comment_url = latest_comment_url

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def notification_type(self):
        return self._notification_type

    @property
    def url(self):
        return self._url

    @property
    def latest_comment_url(self):
        return self._latest_comment_url
