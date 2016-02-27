import curses


class Drawable(object):

    def __init__(self, content, attribute=curses.A_NORMAL):
        self._content = content
        self._attribute = attribute

    @property
    def content(self):
        return self._content

    @property
    def attribute(self):
        return self._attribute


class DrawableList(object):

    def __init__(self, *drawables):
        self._drawables = drawables

    @property
    def drawables(self):
        return self._drawables


class HorizontalSpace(Drawable):

    def __init__(self, length=1, character=" "):
        super(HorizontalSpace, self).__init__(length*character)
