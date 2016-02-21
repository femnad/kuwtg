# Package kuwtg.ui.notifications
from kuwtg.api.consumer import GithubAPIConsumer
from kuwtg.ui import ListScroller

class NotificationsList(ListScroller):

    def __init__(self, list_contents, log_file=None):
        super(NotificationsList, self).__init__(list_contents, log_file)

    def initialize_list(self):
        max_y, max_x = self._get_max_coordinates()
        self._display_multiple_items(
            [item.title
             for item in self._list_contents[:max_y]], max_x-1)
        current_y, current_x = self._get_current_coordinates()
        self._list_cursor = max_y - 1
        self.screen.refresh()
        self.log("Initialization complete")

    def _move_cursor_vertically(self, y_diff):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        self.log("y: {y}, x: {x}", dict(x=current_x, y=current_y))
        new_y = current_y + y_diff
        self.log("new_y: {y}, list cursor: {c}",
                 {"c": self._list_cursor, "y": new_y})
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
        self._last_cursor_position = self._list_cursor
        current_y, current_x = self._get_current_coordinates()
        self._last_y_coordinate = current_y
        self.screen.clear()
        current_item = self._get_current_item()
        self.log("Getting body for {url}", dict(url=current_item.url))
        github_consumer = GithubAPIConsumer()
        body, links = github_consumer.get_notification_body(current_item.url)
        self._display_multiple_items(
            [current_item.notification_type,
            body,]
        )
        if links is not None:
            comments_link = links['comments']['href']
            comments = github_consumer.get_notification_body(comments_link)
            for comment in comments:
                self._display_multiple_items([comment['user'], comment['comment']])
        self.screen.move(0, 0)

    def _show_all_notifications(self):
        self.screen.clear()
        redraw_start = self._list_cursor - self._last_y_coordinate
        if redraw_start < 0:
            redraw_start = 0
        max_y, max_x = self._get_max_coordinates()
        count = 0
        for item in self._list_contents[redraw_start:max_y-2]:
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
