# Package: kuwtg.ui
import curses
import logging
import os
import os.path

class CursesObject(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.clear()
        self.screen.scrollok(1)

    def cleanup(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

class ListScroller(CursesObject):

    DEFAULT_LOG_FILE = '~/.local/share/kuwtg/logs/kuwtg.log'

    def __init__(self, list_contents, log_file=None):
        super(ListScroller, self).__init__()
        self._list_contents = list_contents
        self._list_length = len(self._list_contents)
        self._list_cursor = 0
        self._last_cursor_position = None
        self._last_y_coordinate = None
        self.logger = self._get_logger(log_file)

    def _get_logger(self, file_name):
        if file_name is None:
            file_name = os.path.expanduser(self.DEFAULT_LOG_FILE)
            log_dir = os.path.dirname(file_name)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(file_name)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        return logger

    def log(self, message, variables=None):
        if variables is None:
            variables = {}
        formatted_message = message.format(**variables)
        self.logger.debug(formatted_message)

    def _new_line(self):
        current_y, current_x = self._get_current_coordinates()
        self.screen.move(current_y+1, 0)

    def _display_single_item(self, item, max_chars=None, new_line=True):
        if max_chars is None:
            self.screen.addstr(item)
        else:
            self.screen.addnstr(item, max_chars)
        if new_line:
            self._new_line()

    def _display_multiple_items(self, *items, max_chars=None, new_line=True):
        for item in items:
            self._display_single_item(item)

    def _get_max_coordinates(self):
        return self.screen.getmaxyx()

    def _get_current_coordinates(self):
        return self.screen.getyx()

    def _get_current_item(self):
        return self._list_contents[self._list_cursor]

    def initialize_list(self):
        max_y, max_x = self._get_max_coordinates()
        while self._list_cursor < max_y - 1 and self._list_cursor < self._list_length:
            current_item = self._list_contents[self._list_cursor]
            self._display_single_item(current_item.title, max_x-2)
            self._list_cursor += 1
        current_y, current_x = self._get_current_coordinates()
        self.screen.move(current_y - 1, 0)
        self._list_cursor -= 1
        self.screen.refresh()
        self.log("Initialization complete")

    def _move_cursor_vertically(self, y_diff):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        self.log("y: {y}, x: {x}", dict(x=current_x, y=current_y))
        new_y = current_y + y_diff
        self.log("new_y: {y}, list cursor: {c}",
                 {"c": self._list_cursor, "y": new_y})
        if 0 <= self._list_cursor + y_diff < self._list_length:
            current_item = self._list_contents[self._list_cursor]
            moved_cursor = False
            if 0 <= new_y < max_y:
                self.screen.move(current_y + y_diff, current_x)
                moved_cursor = True
            elif new_y >= max_y:
                self._display_single_item(current_item.title)
                self.screen.move(current_y, 0)
                self.screen.scroll(y_diff)
                moved_cursor = True
            elif new_y < 0:
                self.screen.scroll(y_diff)
                self._display_single_item(current_item.title)
                current_y, current_x = self._get_current_coordinates()
                self.screen.move(current_y, 0)
                moved_cursor = True
            if moved_cursor:
                self._list_cursor += y_diff
        self.screen.refresh()

    def move_up(self):
        self._move_cursor_vertically(-1)

    def move_down(self):
        self._move_cursor_vertically(1)

    def move_to_top(self):
        current_y, current_x = self._get_current_coordinates()
        self.screen.move(0, current_x)

    def move_to_bottom(self):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        self.screen.move(max_y - 1, current_x)

    def debug(self):
        current_y, current_x = self._get_current_coordinates()
        self.log("x: {x}, y: {y}, cursor: {c}",
                 {"y": current_y, "x": current_x, "c": self._list_cursor})

    def _show_current_notification(self):
        self._last_cursor_position = self._list_cursor
        current_y, current_x = self._get_current_coordinates()
        self._last_y_coordinate = current_y
        self.screen.clear()
        current_item = self._get_current_item()
        self._display_multiple_items(
            current_item.url, current_item.latest_comment_url,
            current_item.notification_type)
        self.screen.move(0, 0)

    def _show_all_notifications(self):
        self.screen.clear()
        redraw_start = self._list_cursor - self._last_y_coordinate
        if redraw_start < 0:
            redraw_start = 0
        max_y, max_x = self._get_max_coordinates()
        count = 0
        for item in self._list_contents[redraw_start:max_y-2]:
            self.log("redraw count: {c}", {"c": count})
            self._display_single_item(item.title)
            count += 1
        self.screen.move(self._last_y_coordinate, 0)

    def _process_key(self, key):
        if key == ord('q'):
            self.cleanup()
            return False
        elif key == ord('j'):
            self.move_down()
        elif key == ord('k'):
            self.move_up()
        elif key == ord('d'):
            self.debug()
        elif key == ord('g'):
            self.move_to_top()
        elif key == ord('G'):
            self.move_to_bottom()
        elif key == ord('l'):
            self._show_current_notification()
        elif key == ord('h'):
            self._show_all_notifications()
        return True

    def loop(self):
        while True:
            keep_going = self._process_key(self.screen.getch())
            if not keep_going:
                break
