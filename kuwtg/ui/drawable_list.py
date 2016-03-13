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
