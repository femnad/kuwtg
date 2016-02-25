# Package: kuwtg.ui
import curses
import logging
import os
import os.path

from kuwtg.utils import break_lines


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
        broken_lines = break_lines(item, max_x)
        for line in broken_lines:
            self._display_single_item(line, attribute=attribute)

    def _get_max_coordinates(self):
        return self.screen.getmaxyx()

    def _get_current_coordinates(self):
        return self.screen.getyx()

    def _get_current_item(self):
        return self._list_contents[self._list_cursor]


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

    def debug(self):
        current_y, current_x = self._get_current_coordinates()
        self.log("x: {x}, y: {y}, cursor: {c}",
                 {"y": current_y, "x": current_x, "c": self._list_cursor})
        max_y, max_x = self._get_max_coordinates()
        self.log("max x: {x}, max y {y}, last_y {last}",
                 {"x": max_x, "y": max_y, "last": self._last_y_coordinate})

    def _render_lines(self, comment_body):
        return ' '.join([line
                         for line in comment_body.split('\r\n')
                         if len(line) > 0])


class NotificationDetail(ListScroller):

    def __init__(self, notification_item, notification_starter, comments):
        super(NotificationDetail, self).__init__(comments)
        self._notification_item = notification_item
        self._notification_starter = notification_starter
        self._comments = comments

    def _get_height_of_comment_body(self, comment_body):
        max_y, max_x = self._get_max_coordinates()
        return len(break_lines(comment_body, max_x))

    def _comment_will_fit(self, comment):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        # Assuming user part of a comment is 1
        comment_height = 1 + self._get_height_of_comment_body(comment.body)
        return comment_height < max_y - current_y

    def _display_comment(self, comment):
        self._display_single_item(
            comment.user, attribute=curses.color_pair(4))
        rendered_comment = self._render_lines(comment.body)
        self._display_multiline_item(rendered_comment)

    def draw(self):
        self.screen.clear()
        self.screen.refresh()
        self._display_single_item(
            self._notification_item.repo_name, attribute=curses.color_pair(1))
        self._display_single_item(
            "{}: ".format(self._notification_item.notification_type),
            attribute=curses.color_pair(2), new_line=False)
        self._display_single_item(
            self._notification_item.title, attribute=curses.A_UNDERLINE)
        self._display_single_item(
            self._notification_starter.user, attribute=curses.color_pair(4))
        lines = self._render_lines(self._notification_starter.body)
        self._display_multiline_item(lines)

        for comment in self._comments:
            self._display_comment(comment)

        while True:
            key = self.screen.getch()
            if key in [ord('q'), ord('h')]:
                self.screen.clear()
                self.screen.refresh()
                break
