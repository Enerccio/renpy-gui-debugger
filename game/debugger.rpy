
screen debugger():

    if persistent.project_dir is not None:
        pass


label main_menu:
    python:
        _skipping = False
        _rollback = False

        fb = RG_FolderBrowser()

        renpy.call_screen("rg_folderbrowser", fb, 300, label="TEST")

    $ renpy.quit()
