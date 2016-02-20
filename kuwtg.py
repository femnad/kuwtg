#!/usr/bin/env python3
import curses
import logging
import os
import os.path
import requests
import sys


NOTIFICATIONS_ENDPOINT = 'https://api.github.com/notifications'


def get_notifications(access_token):
    response = requests.get(
        NOTIFICATIONS_ENDPOINT,
        headers={
            "authorization": "token {}".format(access_token),
            "user-agent": "femnad/kuwtg"
        })
    notifications = response.json()
    return notifications

def get_titles(access_token):
    notifications = get_notifications(access_token)
    return [notification['subject']['title'] for notification in notifications]


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

    def _get_max_coordinates(self):
        return self.screen.getmaxyx()

    def _get_current_coordinates(self):
        return self.screen.getyx()

    def initialize_list(self):
        max_y, max_x = self._get_max_coordinates()
        while self._list_cursor < max_y - 1 and self._list_cursor < self._list_length:
            self.screen.addstr(self._list_contents[self._list_cursor])
            self.screen.addch('\n')
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
            moved_cursor = False
            if 0 <= new_y < max_y:
                self.screen.move(current_y + y_diff, current_x)
                moved_cursor = True
            elif new_y >= max_y:
                self.screen.addstr(self._list_contents[self._list_cursor])
                self.screen.move(current_y, 0)
                self.screen.scroll(y_diff)
                moved_cursor = True
            elif new_y < 0:
                self.screen.scroll(y_diff)
                self.screen.addstr(self._list_contents[self._list_cursor - 1])
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
        return True

    def loop(self):
        while True:
            keep_going = self._process_key(self.screen.getch())
            if not keep_going:
                break

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 2:
        access_token = arguments[1]
        titles = get_titles(access_token)
        list_scroller = ListScroller(titles)
        list_scroller.initialize_list()
        list_scroller.loop()
        exit(0)
    else:
        print("Usage ./kuwtg <access-token>")
