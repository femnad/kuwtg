# Package kuwtg.ui.notifications
import curses
from enum import Enum

from kuwtg.api.consumer.github_api_consumer import GithubAPIConsumer
from kuwtg.ui import ListScroller


class NotificationsList(ListScroller):

    class Modes(Enum):
        list_view = 1
        detail_view = 2

    def __init__(self, list_contents, log_file=None):
        super(NotificationsList, self).__init__(list_contents, log_file)
        self._mode = self.Modes.list_view
        self._last_y_coordinate = None

    def _get_current_line(self):
        return self._list_contents[self._list_cursor]

    def _draw_line(self, highlight=False):
        current_line = self._get_current_line()
        if highlight:
            self._redraw_line(current_line.title,
                              attribute=curses.color_pair(3))
        else:
            self._redraw_line(current_line.title,
                              attribute=curses.A_NORMAL)

    def _highlight_line(self):
        self._draw_line(True)

    def _unhighlight_line(self):
        self._draw_line(False)

    def display_list(self, start_from=0, highlight_y_coordinate=None):
        self.screen.clear()
        self.screen.refresh()
        self.screen.move(0, 0)
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        draw_until = min(max_y + start_from, self._list_length)
        for item in self._list_contents[start_from:draw_until-1]:
            self._display_single_item(item.title)
        self._redraw_line(self._list_contents[draw_until-1].title)
        # List cursor is on the last item which was drawn, so substract 1 from
        # `draw_until`
        self._list_cursor = draw_until - 1
        if highlight_y_coordinate is not None:
            self.screen.move(highlight_y_coordinate, 0)
        self.screen.clear()
        self.screen.refresh()
        self._highlight_line()

    def _move_cursor_vertically(self, y_diff):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        new_y = current_y + y_diff
        self._unhighlight_line()
        new_cursor_position = self._list_cursor + y_diff
        if 0 <= new_cursor_position < self._list_length:
            if 0 <= new_y < max_y:  # Moving the cursor is enough
                self.screen.move(current_y + y_diff, current_x)
            else:  # We have to scroll
                self.screen.scroll(y_diff)
                self.screen.move(current_y, 0)
            self._list_cursor += y_diff
        self._highlight_line()
        self.screen.refresh()

    def _render_lines(self, comment_body):
        return [line for line in comment_body.split('\r\n') if len(line) > 0]

    def _show_current_notification(self):
        self._unhighlight_line()
        self._mode = self.Modes.detail_view
        current_y, current_x = self._get_current_coordinates()
        self._last_y_coordinate = current_y
        current_item = self._get_current_item()
        github_consumer = GithubAPIConsumer()
        body, links = github_consumer.get_notification_body(current_item.url)
        self.screen.clear()
        self._display_single_item(
            current_item.repo_name, attribute=curses.color_pair(1))
        self._display_single_item(
            "{}: ".format(current_item.notification_type),
            attribute=curses.color_pair(2), new_line=False)
        self._display_single_item(
            current_item.title, attribute=curses.A_UNDERLINE)
        lines = self._render_lines(body)
        for line in lines:
            self._display_multiline_item(line)
        self.screen.move(0, 0)

    def _show_all_notifications(self):
        self._mode = self.Modes.list_view
        self.screen.clear()
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
        self.display_list(redraw_start, self._last_y_coordinate)

    def _process_key(self, key):
        if key == ord('q'):
            self.cleanup()
            return False
        elif key == ord('d'):
            self.debug()
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
        elif self._mode == self.Modes.detail_view:
            if key == ord('h'):
                self._show_all_notifications()
        return True

    def loop(self):
        while True:
            keep_going = self._process_key(self.screen.getch())
            if not keep_going:
                break
