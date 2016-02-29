# Package kuwtg.ui.notifications
from enum import Enum

from kuwtg.api.consumer.github_api_consumer import GithubAPIConsumer
from kuwtg.config.configuration import Configuration
from kuwtg.ui import Attributes, Colors, CursesObject
from kuwtg.ui.notification_detail import NotificationDetail


class NotificationsList(CursesObject):

    class Modes(Enum):
        list_view = 1
        detail_view = 2

    def __init__(self, list_contents):
        super(NotificationsList, self).__init__()
        self._list_contents = list_contents
        self._list_length = len(self._list_contents)
        self._list_cursor = 0
        self._mode = self.Modes.list_view
        self._last_y_coordinate = None
        self._configuration = Configuration()
        self.logger = self._set_logger(__name__)

    def _get_current_line(self):
        return self._list_contents[self._list_cursor]

    def _draw_line(self, highlight=False):
        current_line = self._get_current_line()
        if highlight:
            self._redraw_line(
                current_line.title, attribute=self._get_color(
                    Colors.black_on_magenta))
        else:
            self._redraw_line(current_line.title,
                              attribute=self._get_attribute(Attributes.normal))

    def _highlight_line(self):
        self._draw_line(True)

    def _unhighlight_line(self):
        self._draw_line(False)

    def display_list(self, start_from=0):
        self.screen.clear()
        self.screen.refresh()
        self.screen.move(0, 0)
        max_coords = self._get_max_coordinates()
        draw_until = min(max_coords.y + start_from, self._list_length)
        for item in self._list_contents[start_from:draw_until-1]:
            self._display_single_item(item.title)
        self._draw_line(highlight=True)
        # List cursor is on the last item which was drawn, so substract 1 from
        # `draw_until`
        self._list_cursor = draw_until - 1
        self._highlight_line()

    def _move_cursor_vertically(self, y_diff):
        current_coords = self._get_current_coordinates()
        max_coords = self._get_max_coordinates()
        new_y = current_coords.y + y_diff
        self._unhighlight_line()
        new_cursor_position = self._list_cursor + y_diff
        if 0 <= new_cursor_position < self._list_length:
            if 0 <= new_y < max_coords.y:  # Moving the cursor is enough
                self.screen.move(current_coords.y + y_diff, current_coords.x)
            else:  # We have to scroll
                self.screen.scroll(y_diff)
                self.screen.move(current_coords.y, 0)
            self._list_cursor += y_diff
        self._highlight_line()
        self.screen.refresh()

    def move_up(self):
        self._move_cursor_vertically(-1)

    def move_down(self):
        self._move_cursor_vertically(1)

    def move_to_top(self):
        current_coords = self._get_current_coordinates()
        self.screen.move(0, current_coords.x)
        self._list_cursor -= current_coords.y

    def move_to_bottom(self):
        current_coords = self._get_current_coordinates()
        max_coords = self._get_max_coordinates()
        self.screen.move(max_coords.y - 1, current_coords.x)
        self._list_cursor += (max_coords.y - current_coords.y - 1)

    def _show_current_notification(self):
        self._unhighlight_line()
        self._mode = self.Modes.detail_view
        current_coords = self._get_current_coordinates()
        self._last_y_coordinate = current_coords.y
        current_item = self._get_current_item()
        github_consumer = GithubAPIConsumer(self._configuration.access_token)
        starter, comments = github_consumer.get_notification_body(
            current_item.url)
        notification_detail = NotificationDetail(
            current_item, starter, comments)
        notification_detail.draw()
        self._show_all_notifications()

    def _show_all_notifications(self):
        self._mode = self.Modes.list_view
        self.screen.clear()
        self.screen.refresh()
        """
        Find out where we have start redrawing. For a screen of 5 height,
        assume we were at y = 2 (0-indexed) previously and the list contained
        10 items, where the y cursor was on the 2th item (zero based).

        .
        .
        . y = 2, c = 5
        .
        .

        So in order to show the same list state on redraw, we have to start
        drawing from 3th item in the list and move to y cursor to its original
        position

        . y = 0, c = 3
        .
        . y = 2
        .
        .

        """
        redraw_start = self._list_cursor - self._last_y_coordinate
        if redraw_start < 0:
            redraw_start = 0
        self.display_list(redraw_start)

    def _process_key(self, key):
        if key == ord('q'):
            self.cleanup()
            return False
        if self._mode == self.Modes.list_view:
            if key == ord('j'):
                self.move_down()
            elif key == ord('k'):
                self.move_up()
            elif key == ord('g'):
                self.move_to_top()
            elif key == ord('G'):
                self.move_to_bottom()
            elif key == ord('l'):
                self._show_current_notification()
        return True

    def loop(self):
        while True:
            keep_going = self._process_key(self.screen.getch())
            if not keep_going:
                break
