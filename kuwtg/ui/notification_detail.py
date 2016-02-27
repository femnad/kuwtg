from kuwtg.ui import Attributes, Colors, CursesObject
from kuwtg.ui.drawables import Drawable, DrawableList, HorizontalSpace
from kuwtg.utils import break_lines, render_lines


class NotificationDetail(CursesObject):

    def __init__(self, notification_item, notification_starter, comments):
        super(NotificationDetail, self).__init__()
        self._notification_item = notification_item
        self._notification_starter = notification_starter
        self._comments = comments
        self._visible_content = []
        self._set_logger(__name__)

    def _add_to_visible_content(self, drawable):
        if isinstance(drawable, list):
            self._visible_content.extend(drawable)
        else:
            self._visible_content.append(drawable)

    def _draw_line(self, line):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        if isinstance(line, Drawable):
            self.screen.addstr(line.content, line.attribute)
        elif isinstance(line, DrawableList):
            for drawable in line.drawables:
                self.screen.addstr(drawable.content, drawable.attribute)
        if current_y < max_y - 1:
            self.screen.move(current_y+1, 0)
        else:
            self.screen.move(current_y, 0)

    def _can_draw_more(self):
        current_y, current_x = self._get_current_coordinates()
        max_y, max_x = self._get_max_coordinates()
        return current_y < max_y - 1

    def _get_rendered_lines(self, comment_body):
        max_y, max_x = self._get_max_coordinates()
        rendered_lines = render_lines(comment_body)
        broken_lines = break_lines(rendered_lines, max_x)
        return [Drawable(line) for line in broken_lines]

    def draw(self):
        self.screen.clear()
        self.screen.refresh()
        self._add_to_visible_content(Drawable(
            self._notification_item.repo_name,
            attribute=self._get_color(Colors.red)))
        self._add_to_visible_content(DrawableList(
            Drawable(self._notification_item.notification_type,
                     self._get_color(Colors.green)),
            Drawable(": "),
            Drawable(self._notification_item.title,
                     self._get_attribute(Attributes.underlined))))
        self._add_to_visible_content(DrawableList(
            Drawable(self._notification_starter.user,
                     self._get_color(Colors.blue)),
            HorizontalSpace(length=5),
            Drawable(self._notification_starter.created_at,
                     self._get_color(Colors.yellow))))

        lines = self._get_rendered_lines(self._notification_starter.body)
        self._add_to_visible_content(lines)

        for comment in self._comments:
            comment_drawable = DrawableList(
                Drawable(comment.user, self._get_color(Colors.yellow)),
                HorizontalSpace(length=5),
                Drawable(comment.created_at, self._get_color(Colors.yellow)))
            self._add_to_visible_content(comment_drawable)
            rendered_comment = self._get_rendered_lines(comment.body)
            self._add_to_visible_content(rendered_comment)

        last_cursor = 0
        for index, content in enumerate(self._visible_content):
            if self._can_draw_more():
                self._draw_line(content)
            else:
                self._draw_line(content)  # Off by one error (or two?)
                last_cursor = index + 1
                break

        while True:
            key = self.screen.getch()
            if key in [ord('q'), ord('h')]:
                self.screen.clear()
                self.screen.refresh()
                break
            elif key == ord('j'):
                last_cursor = self._scroll(last_cursor, 1)
            elif key == ord('k'):
                last_cursor = self._scroll(last_cursor, -1)

    def _scroll(self, last_cursor, direction):
        max_y, max_x = self._get_max_coordinates()
        if direction > 0 and last_cursor < len(self._visible_content):
            self.screen.scroll(direction)
            self.screen.move(max_y-1, 0)
            self._draw_line(self._visible_content[last_cursor])
        elif direction < 0 and last_cursor - max_y > 0:
            self.screen.scroll(direction)
            self.screen.move(0, 0)
            self._draw_line(self._visible_content[last_cursor - max_y - 1])
        last_cursor += direction
        current_y, current_x = self._get_current_coordinates()
        self.screen.move(current_y, 0)
        return last_cursor
