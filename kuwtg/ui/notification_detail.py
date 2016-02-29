from kuwtg.ui import Attributes, Colors, Coordinates, CursesObject
from kuwtg.ui.drawables import Drawable, DrawableList, HorizontalSpace
from kuwtg.utils import break_lines, render_lines


class NotificationDetail(CursesObject):

    def __init__(self, notification_item, notification_starter, comments):
        super(NotificationDetail, self).__init__()
        self._notification_item = notification_item
        self._notification_starter = notification_starter
        self._comments = comments
        self._content = []
        self._cursor = 0
        self._set_logger(__name__)

    def _add_to_content(self, drawable):
        if isinstance(drawable, list):
            self._content.extend(drawable)
        else:
            self._content.append(drawable)

    def _draw_line(self, line):
        current_coordinates = self._get_current_coordinates()
        max_coordinates = self._get_max_coordinates()
        if isinstance(line, Drawable):
            self.screen.addstr(line.content, line.attribute)
        elif isinstance(line, DrawableList):
            for drawable in line.drawables:
                self.screen.addstr(drawable.content, drawable.attribute)
        if current_coordinates.y < max_coordinates.y - 1:
            self.screen.move(current_coordinates.y+1, 0)
        else:
            self.screen.move(current_coordinates.y, 0)

    def _can_draw_more(self):
        current_coordinates = self._get_current_coordinates()
        max_coordinates = self._get_max_coordinates()
        return current_coordinates.y < max_coordinates.y - 1

    def _get_rendered_lines(self, comment_body):
        max_coordinates = self._get_max_coordinates()
        rendered_lines = render_lines(comment_body)
        broken_lines = break_lines(rendered_lines, max_coordinates.x)
        return [Drawable(line) for line in broken_lines]

    def draw(self):
        self.screen.clear()
        self.screen.refresh()
        self._add_to_content(Drawable(
            self._notification_item.repo_name,
            attribute=self._get_color(Colors.red)))
        self._add_to_content(DrawableList(
            Drawable(self._notification_item.notification_type,
                     self._get_color(Colors.green)),
            Drawable(": "),
            Drawable(self._notification_item.title,
                     self._get_attribute(Attributes.underlined))))
        self._add_to_content(DrawableList(
            Drawable(self._notification_starter.user,
                     self._get_color(Colors.blue)),
            HorizontalSpace(length=5),
            Drawable(self._notification_starter.created_at,
                     self._get_color(Colors.yellow))))

        lines = self._get_rendered_lines(self._notification_starter.body)
        self._add_to_content(lines)

        if self._comments is not None:
            for comment in self._comments:
                comment_drawable = DrawableList(
                    Drawable(comment.user, self._get_color(Colors.blue)),
                    HorizontalSpace(length=5),
                    Drawable(comment.created_at, self._get_color(Colors.yellow)))
                self._add_to_content(comment_drawable)
                rendered_comment = self._get_rendered_lines(comment.body)
                self._add_to_content(rendered_comment)

        for index, content in enumerate(self._content):
            if self._can_draw_more():
                self._draw_line(content)
            else:
                self._draw_line(content)
                self._cursor = index + 1
                break

        while True:
            key = self.screen.getch()
            if key in [ord('q'), ord('h')]:
                self.screen.clear()
                self.screen.refresh()
                break
            elif key == ord('j'):
                self._move_cursor(1)
            elif key == ord('k'):
                self._move_cursor(-1)
            elif key == ord('d'):
                self._debug()

    def _is_movable(self, direction):
        if direction < 0:
            return self._cursor > 1
        elif direction > 0:
            return self._cursor < len(self._content)

    def _get_next_coordinates(self, direction, scroll):
        current_coordinates = self._get_current_coordinates()
        if scroll:
            return current_coordinates
        return Coordinates(current_coordinates.y + direction, 0)

    def _should_scroll(self, direction):
        current_coordinates = self._get_current_coordinates()
        max_coordinates = self._get_max_coordinates()
        if direction > 0:
            return current_coordinates.y == max_coordinates.y - 1
        elif direction < 0:
            return current_coordinates.y == 0 and self._cursor > 0

    def _get_next_line(self, direction):
        return self._content[self._cursor+direction-1]

    def _move_cursor(self, direction):
        if self._is_movable(direction):
            should_scroll = self._should_scroll(direction)
            next_coordinates = self._get_next_coordinates(
                direction, should_scroll)
            if should_scroll:
                self.screen.scroll(direction)
                next_line = self._get_next_line(direction)
                self._draw_line(next_line)
            self._cursor += direction
            self.screen.move(next_coordinates.y, next_coordinates.x)
