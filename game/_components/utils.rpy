init python:
    def quote(string):
        return string.replace("{", "{{").replace("\ufeff", "")


screen rg_wrap_max(xmax=None):
    viewport:
        if xmax is not None:
            xsize xmax
        mousewheel False
        draggable False
        xinitial 1.0
        scrollbars None

        hbox:
            transclude
