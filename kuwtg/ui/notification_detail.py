from kuwtg.ui import Attributes, Colors
from kuwtg.ui.drawables import Drawable, DrawableList, HorizontalSpace
from kuwtg.ui.drawable_container import DrawableContainer


class NotificationDetail(DrawableContainer):

    def __init__(self, notification_item, notification_starter, comments):
        super(NotificationDetail, self).__init__()
        self._notification_item = notification_item
        self._notification_starter = notification_starter
        self._comments = comments
        self._content = []
        self._cursor = 0
        self._set_logger(__name__)

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
                    Drawable(comment.created_at,
                             self._get_color(Colors.yellow)))
                self._add_to_content(comment_drawable)
                rendered_comment = self._get_rendered_lines(comment.body)
                self._add_to_content(rendered_comment)

        self._render()

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
