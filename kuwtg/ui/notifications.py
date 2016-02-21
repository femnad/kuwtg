# Package kuwtg.ui.notifications
import curses
from enum import Enum

from kuwtg.api.consumer import GithubAPIConsumer
from kuwtg.ui import ListScroller


class NotificationsList(ListScroller):

    class Modes(Enum):
        list_view = 1
        detail_view = 2

    def __init__(self, list_contents, log_file=None):
        super(NotificationsList, self).__init__(list_contents, log_file)
        self._mode = self.Modes.list_view

    def display_list(self, start_from=0, cursor_y_position=None):
        self.screen.clear()
        self.screen.move(0, 0)
        max_y, max_x = self._get_max_coordinates()
        draw_until = min(max_y, self._list_length)
        self._display_multiple_items(
            [item.title
             for item in self._list_contents[start_from:draw_until]], max_x-1)
        # List cursor is on the last item which was drawn, so substract 1 from
        # `draw_until`
        self._list_cursor = draw_until - 1
        if cursor_y_position is not None:
            self.screen.move(cursor_y_position, 0)
            self._list_cursor = cursor_y_position
        self.screen.refresh()

    def _move_cursor_vertically(self, y_diff):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        new_y = current_y + y_diff
        new_cursor_position = self._list_cursor + y_diff
        if 0 <= new_cursor_position < self._list_length:
            if 0 <= new_y < max_y: # Moving the cursor is enough
                self.screen.move(current_y + y_diff, current_x)
                moved_cursor = True
            else: # We have to scroll
                next_item = self._list_contents[new_cursor_position]
                self.screen.scroll(y_diff)
                max_chars = max_x - 1
                self._display_single_item(
                    next_item.title, max_chars=max_chars, new_line=False)
                self.screen.move(current_y, 0)
            self._list_cursor += y_diff
        self.screen.refresh()

    def _show_current_notification(self):
        self._mode = self.Modes.detail_view
        current_y, current_x = self._get_current_coordinates()
        self._last_y_coordinate = current_y
        self.screen.clear()
        current_item = self._get_current_item()
        github_consumer = GithubAPIConsumer()
        body, links = github_consumer.get_notification_body(current_item.url)
        self._display_single_item("{}: ".format(current_item.notification_type),
                                  attribute=curses.color_pair(2), new_line=False)
        self._display_single_item(current_item.title, attribute=curses.A_UNDERLINE)
        self._display_single_item(body)
        if links is not None:
            comments_link = links['comments']['href']
            comments = github_consumer.get_comments(comments_link)
            for comment in comments:
                if comment is not None:
                    self._display_multiple_items(
                        [comment['user'], comment['comment']],
                        new_line_on_last_item=True)
        self.screen.move(1, 0)

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
        redraw_start =  self._list_cursor - self._last_y_coordinate
        if redraw_start < 0:
            redraw_start = 0
        self.display_list(redraw_start,
                          cursor_y_position=self._last_y_coordinate)

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
