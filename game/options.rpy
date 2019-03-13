define config.name = _("Ren'Py Interactive Debugger")
define gui.show_name = True
define config.version = "1.0"
define gui.about = _p("""
""")
define build.name = "debugger"
define config.has_sound = False
define config.has_music = False
define config.has_voice = False
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)
default preferences.text_cps = 0
default preferences.afm_time = 15
define config.save_directory = "debugger-1552469895"
define config.window_icon = "gui/window_icon.png"

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**.rpyc', None)
    build.classify('**.pyc', None)
    build.classify('**.pyo', None)
    build.classify('**/.**', None)
    build.classify('.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.documentation('*.html')
    build.documentation('*.txt')

    if config.developer:
        config.quit_action = None
