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

            self.blocked = []
            cline = ""
            for i in xrange(len(self.content)):
                cline += "%6s %s\n" % (str(i + 1), self.content[i])
                if len(cline) > 20000:
                    self.blocked.append(cline)
                    cline = ""
            if cline != "":
                self.blocked.append(cline)

            self.scroll_x = ui.adjustment()
            self.scroll_y = ui.adjustment()

            debugger.tree_state.selected = source

        def on_click(self, vx, vy, cx, cy, event, st):
            print cx, cy



screen buffer(buffer, cbuffer_size):
    if buffer is not None:
        # TODO breakpoints

        label buffer.filename

        clickarea:
            scrollbars "both"
            mousewheel True
            draggable True
            xadjustment buffer.scroll_x
            yadjustment buffer.scroll_y

            click buffer.on_click

            vbox:
                xpos 16
                for block in buffer.blocked:
                    text Text(block, substitute=False, size=16)
