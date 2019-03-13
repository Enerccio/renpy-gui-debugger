init python:
    import os

    class Buffer(NoRollback):
        def __init__(self, source): # THROWS!
            self.source = source

            if os.path.isabs(source):
                self.file = os.path.abspath(source)
            else:
                self.file = os.path.join(debugger.get_project_dir(), source)

            self.filename = os.path.basename(self.file)

            with open(self.file, "r") as f:
                self.content = [quote(x.rstrip()) for x in f.readlines()]

            self.lined = ""
            for i in xrange(len(self.content)):
                self.lined += "%6s %s\n" % (str(i + 1), self.content[i])

            self.scroll_x = ui.adjustment()
            self.scroll_y = ui.adjustment()

            debugger.tree_state.selected = source



screen buffer(buffer):
    if buffer is not None:
        # TODO breakpoints

        label buffer.filename

        viewport:
            scrollbars "both"
            mousewheel True
            draggable True
            xadjustment buffer.scroll_x
            yadjustment buffer.scroll_y

            text Text(buffer.lined, substitute=False, size=16):
                xpos 16
