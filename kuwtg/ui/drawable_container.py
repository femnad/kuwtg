from kuwtg.ui import CursesObject, Coordinates
from kuwtg.ui.drawables import Drawable, DrawableList
from kuwtg.utils import break_lines, render_lines


class DrawableContainer(CursesObject):

    def __init__(self):
        super(DrawableContainer, self).__init__()
        self._content = []
        self._cursor = 0

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
        y_coordinate_increment = 0
        if current_coordinates.y < max_coordinates.y - 1:
            y_coordinate_increment += 1
        self._move(Coordinates(
            current_coordinates.y + y_coordinate_increment, 0))

    def _can_draw_more(self):
        current_coordinates = self._get_current_coordinates()
        max_coordinates = self._get_max_coordinates()
        return current_coordinates.y < max_coordinates.y - 1

    def _get_rendered_lines(self, comment_body):
        max_coordinates = self._get_max_coordinates()
        rendered_lines = render_lines(comment_body)
        broken_lines = break_lines(rendered_lines, max_coordinates.x)
        return [Drawable(line) for line in broken_lines]

    def _render(self):
        self.screen.clear()
        self.screen.refresh()
        for index, content in enumerate(self._content):
            if self._can_draw_more():
                self._draw_line(content)
            else:
                self._draw_line(content)
                self._cursor = index + 1
                break

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
