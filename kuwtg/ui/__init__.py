# Package: kuwtg.ui
import curses
from enum import Enum
import logging
import os
import os.path

from kuwtg.config.configuration import Configuration
from kuwtg.utils import break_lines


class Colors(Enum):
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7
    black_on_magenta = 8


class Attributes(Enum):
    normal = curses.A_NORMAL
    underlined = curses.A_UNDERLINE


class Coordinates(object):

    def __init__(self, y=None, x=None):
        self._y = y
        self._x = x

    def __str__(self):
        return "<Coordinates[y={y}, x={y}]>".format(x=self._x, y=self._y)

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x


class CursesObject(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self._initialize_colors()
        self.screen.clear()
        self.screen.scrollok(1)

    def _initialize_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(Colors.red.value, curses.COLOR_RED, -1)
        curses.init_pair(Colors.green.value, curses.COLOR_GREEN, -1)
        curses.init_pair(Colors.yellow.value, curses.COLOR_YELLOW, -1)
        curses.init_pair(Colors.blue.value, curses.COLOR_BLUE, -1)
        curses.init_pair(Colors.black_on_magenta.value, curses.COLOR_BLACK,
                         curses.COLOR_MAGENTA)

    def _get_color(self, color):
        return curses.color_pair(color.value)

    def _get_attribute(self, attribute):
        return attribute.value

    def _set_logger(self, logger_name):
        configuration = Configuration()
        log_file = configuration.log_file
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter
        formatter = logging.Formatter('%(asctime)s %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        self.logger = logger

    def _move(self, coordinates):
        self.screen.move(coordinates.y, coordinates.x)

    def _scroll(self, direction):
        self.screen.scroll(direction)

    def log(self, message, variables=None):
        if variables is None:
            variables = {}
        if isinstance(message, str):
            formatted_message = message.format(**variables)
            self.logger.debug(formatted_message)
        else:
            self.logger.debug(message)

    def cleanup(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def _new_line(self):
        current_coordinates = self._get_current_coordinates()
        max_coords = self._get_max_coordinates()
        if current_coordinates.y < max_coords.y - 1:
            self.screen.move(current_coordinates.y+1, 0)
        else:
            self.screen.move(current_coordinates.y, 0)

    def _display_single_item(self, item, limit_length=True, new_line=True,
                             attribute=None, start_coordinates=None):
        display = self.screen.addnstr \
            if limit_length else self.screen.addstr
        display_args = []
        if start_coordinates is not None:
            display_args.extend(start_coordinates)
        display_args.append(item)
        if limit_length:
            max_coords = self._get_max_coordinates()
            display_args.append(max_coords.x - 1)
        if attribute is not None:
            display_args.append(attribute)
        display(*display_args)
        if new_line:
            self._new_line()

    def _redraw_line(self, item, attribute=None):
        current_coords = self._get_current_coordinates()
        self._display_single_item(item,
                                  start_coordinates=(current_coords.y, 0),
                                  attribute=attribute,
                                  new_line=False)

    def _display_multiple_items(self, items, limit_length=True, new_line=True,
                                attributes=None):
        for item in items:
            self._display_single_item(item, limit_length, new_line, attributes)

    def _display_multiline_item(self, item, attribute=None):
        max_coords = self._get_max_coordinates()
        broken_lines = break_lines(item, max_coords.x)
        for line in broken_lines:
            self._display_single_item(line, attribute=attribute)

    def _get_max_coordinates(self):
        max_y, max_x = self.screen.getmaxyx()
        return Coordinates(y=max_y, x=max_x)

    def _get_current_coordinates(self):
        current_y, current_x = self.screen.getyx()
        return Coordinates(y=current_y, x=current_x)
