from kuwtg.ui import Attributes


class Drawable(object):

    def __init__(self, content, attribute=None, embedded_object=None):
        self._content = content
        if attribute is None:
            attribute = Attributes.normal.value
        self._attribute = attribute
        self._embedded_object = embedded_object

    @property
    def content(self):
        return self._content

    @property
    def attribute(self):
        return self._attribute

    @property
    def embedded_object(self):
        return self._embedded_object


class DrawableList(object):

    def __init__(self, *drawables):
        self._drawables = drawables

    @property
    def drawables(self):
        return self._drawables


class HorizontalSpace(Drawable):

    def __init__(self, length=1, character=" "):
        super(HorizontalSpace, self).__init__(length*character)
