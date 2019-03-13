
init python:
    import threading
    import os
    import traceback

    from librpydb.debugger import *
    from librpydb.baseconf import DEBUGGER_PORT


    def set_renpy_dir(fb):
        persistent.renpy_dir = fb.get_path()
        return True


    def set_project_dir(fb):
        persistent.last_project_dir = fb.get_path()
        debugger.set_project_dir(fb.get_path())
        return True


    def reset_renpy_dir():
        fb = RG_FolderBrowser(persistent.renpy_dir)
        renpy.show_screen("rg_folderbrowser_picker", fb, fb._mk_tree(), _("Select Ren'Py SDK location"), set_renpy_dir)


    class RpyDebuggerState(NoRollback):
        def __init__(self):
            self.project_dir = persistent.last_project_dir
            self.debugger = RenpyDebugger("127.0.0.1", DEBUGGER_PORT)

            self.debugger.set_connected_callback(self.connected)
            self.debugger.set_pause_callback(self.paused)
            self.debugger.set_client_error_callback(self.errored)
            self.debugger.set_pause_callback(self.disconnected)

            self.tree_state = None
            self.active_buffer = None

            if self.project_dir is not None:
                self.tree_state = build_project_tree(self)

            self._connected = False
            self._executed_state = None

            self.state_lock = threading.RLock()

        def refresh(self):
            with self.state_lock:

                if self.has_project():
                    self.tree_state = build_project_tree(self)

        def has_project(self):
            with self.state_lock:
                return self.project_dir is not None

        def is_ready(self):
            return self._connected and (self.debugger.get_state() == DebuggerState.CONNECTED or
                self.debugger.get_state() == DebuggerState.EXECUTION_PAUSED)

        def is_paused(self):
            with self.state_lock:
                return self._connected and self.debugger.get_state() == DebuggerState.EXECUTION_PAUSED and self._executed_state is not None

        def connected(self, *args, **kwargs):
            with self.state_lock:
                self._connected = True

        def paused(self, stop_reason, description, exc):
            with self.state_lock:
                self._pause_reason = stop_reason
                self._executed_state = exc

        def errored(self, *args, **kwargs):
            with self.state_lock:
                pass

        def disconnected(self):
            with self.state_lock:
                self._connected = False
                self._execution_state = None

        def set_project_dir(self, pd):
            self.project_dir = pd
            # TODO: full reset, close buffers etc

        def get_project_dir(self):
            return self.project_dir

        def on_buffer_select(self, tree, buffer_source):
            with self.state_lock:
                if not os.path.isdir(buffer_source):
                    self.open_buffer(buffer_source)

        def open_buffer(self, path):
            with self.state_lock:
                try:
                    self.active_buffer = Buffer(path)
                except Exception:
                    traceback.print_exc()
                    renpy.notify("Failed to open buffer %s" % str(path))


screen debugger_set_renpy(fb, action):
    modal True

    frame:
        xalign 0.5
        yalign 0.5

        vbox:
            label _("Ren'Py Debugger Setup") xalign 0.5
            text ""
            text _("Hello and welcome to Ren'Py Interactive Debugger.") xalign 0.5 text_align 0.5
            text _("Please provide path to the Ren'Py SDK.") xalign 0.5 text_align 0.5
            textbutton _("OK"):
                xalign 0.5
                text_align 0.5

                action [Hide("debugger_set_renpy"), Show("rg_folderbrowser_picker", None, fb, fb._mk_tree(), _("Select Ren'Py SDK location"), action)]


screen debugger_project_conf():
    frame:
        xpos 2
        ypos 2
        ysize 42

        hbox:
            spacing 2

            if debugger.is_ready():
                null width 300 height 32
            else:
                imagebutton:
                    idle "icons/settings.png"
                    tooltip _("Set Ren'Py SDK path")
                    action [Function(reset_renpy_dir)]

                use rg_folderbrowser_widget(RG_FolderBrowser(debugger.project_dir), 266, label=_("Select project location"), tooltip=_("Change project path"), on_ok=set_project_dir)


screen debugger_toolbar():
    pass


screen debugger_filebrowser():
    frame:
        xpos 2
        ypos 46
        xsize 311
        ysize 642

        vbox:
            spacing 2
            
            label _("Project sources:")

            if debugger.has_project():
                use projectbrowser()


screen debugger_tooltip_area():
    $ tooltip = GetTooltip()

    frame:
        xpos 2
        ypos 690
        xsize 1276

        text ("" if tooltip is None else tooltip)


screen debugger_content():

    frame:
        xpos 315
        ypos 46
        xsize 1280-320
        ysize 642

        if debugger.has_project():
            vbox:
                use buffer(debugger.active_buffer)


screen debugger():
    timer 0.5 action Function(debugger.refresh) repeat True

    use debugger_project_conf
    use debugger_toolbar
    use debugger_filebrowser
    use debugger_content
    use debugger_tooltip_area



label main_menu:
    return


label start:
    hide window

    python:
        _confirm_quit = config.developer
        _skipping = False
        _rollback = False
        quick_menu = False
        _game_menu_screen = None

        while persistent.renpy_dir is None:
            fb = RG_FolderBrowser()
            renpy.call_screen("debugger_set_renpy", fb, set_renpy_dir)

        # launch_renpy_project("/src/r/renpy-gui-debugger/debuggee", persistent.renpy_dir, "/src/renpyprojects/fgoharem", False)

        debugger = RpyDebuggerState()
        renpy.show_screen("debugger")
        while True:
            ui.interact()

    $ renpy.quit()
