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
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
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
        max_y, max_x = self._get_max_coordinates()
        if current_y < max_y - 1:
            self.screen.move(current_y+1, 0)
        else:
            self.screen.move(current_y, 0)

    def _display_single_item(self, item, limit_length=True, new_line=True,
                             attribute=None, start_coordinates=None):
        display = self.screen.addnstr \
                  if limit_length else self.screen.addstr
        display_args = []
        if start_coordinates is not None:
            display_args.extend(start_coordinates)
        display_args.append(item)
        if limit_length:
            max_y, max_x = self._get_max_coordinates()
            display_args.append(max_x - 1)
        if attribute is not None:
            display_args.append(attribute)
        display(*display_args)
        if new_line:
            self._new_line()

    def _redraw_line(self, item, attribute=None):
        current_y, current_x = self._get_current_coordinates()
        self._display_single_item(item,
                                  start_coordinates=(current_y, 0),
                                  attribute=attribute,
                                  new_line=False)

    def _display_multiple_items(self, items, limit_length=True, new_line=True,
                                attributes=None):
        for item in items:
            self._display_single_item(item, limit_length, new_line, attributes)

    def _display_multiline_item(self, item, attribute=None):
        max_y, max_x = self._get_max_coordinates()
        if len(item) < max_x:
            self._display_single_item(item, attribute=attribute)
        else:
            head, tail = item[:max_x], item[max_x:]
            self._display_single_item(head, attribute=attribute)
            self._display_multiline_item(tail, attribute=attribute)

    def _get_max_coordinates(self):
        return self.screen.getmaxyx()

    def _get_current_coordinates(self):
        return self.screen.getyx()

    def _get_current_item(self):
        return self._list_contents[self._list_cursor]

    def move_up(self):
        self._move_cursor_vertically(-1)

    def move_down(self):
        self._move_cursor_vertically(1)

    def move_to_top(self):
        current_y, current_x = self._get_current_coordinates()
        self.screen.move(0, current_x)
        self._list_cursor -= current_y

    def move_to_bottom(self):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        self.screen.move(max_y - 1, current_x)
        self._list_cursor += (max_y - current_y - 1)

    def debug(self):
        current_y, current_x = self._get_current_coordinates()
        self.log("x: {x}, y: {y}, cursor: {c}",
                 {"y": current_y, "x": current_x, "c": self._list_cursor})
        max_y, max_x = self._get_max_coordinates()
        self.log("max x: {x}, max y {y}, last_y {last}",
                 {"x": max_x, "y": max_y, "last": self._last_y_coordinate})
