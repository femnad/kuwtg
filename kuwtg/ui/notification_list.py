# Package kuwtg.ui.notifications
from enum import Enum

from kuwtg.api.consumer.github_api_consumer import GithubAPIConsumer
from kuwtg.config.configuration import Configuration
from kuwtg.ui.drawables import Drawable
from kuwtg.ui.drawable_container import DrawableContainer
from kuwtg.ui.notification_detail import NotificationDetail


class NotificationList(DrawableContainer):

    class Modes(Enum):
        list_view = 1
        detail_view = 2

    def __init__(self, list_contents):
        super(NotificationList, self).__init__()
        self._mode = self.Modes.list_view
        self._configuration = Configuration()
        self.logger = self._set_logger(__name__)
        for content in list_contents:
            self._add_to_content(Drawable(content.title,
                                          embedded_object=content))

    def _get_current_item(self):
        return self._content[self._cursor - 1]  # Venerable off by one error

    def draw(self):
        self._render()
        while True:
            keep_going = self._process_key(self.screen.getch())
            if not keep_going:
                break

    def _show_current_notification(self):
        self._mode = self.Modes.detail_view
        current_coords = self._get_current_coordinates()
        self._last_y_coordinate = current_coords.y
        current_item = self._get_current_item()
        github_consumer = GithubAPIConsumer(self._configuration.access_token)
        notification_object = current_item.embedded_object
        starter, comments = github_consumer.get_notification_body(
            notification_object.url)
        notification_detail = NotificationDetail(
            notification_object, starter, comments)
        notification_detail.draw()
        self._show_all_notifications()

    def _show_all_notifications(self):
        self._mode = self.Modes.list_view
        self._render()

    def _process_key(self, key):
        if key == ord('q'):
            self.cleanup()
            return False
        if self._mode == self.Modes.list_view:
            if key == ord('j'):
                self._move_cursor(1)
            elif key == ord('k'):
                self._move_cursor(-1)
            elif key == ord('l'):
                self._show_current_notification()
        return True
