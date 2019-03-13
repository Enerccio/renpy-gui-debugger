
init python hide:
    import os
    import platform

    class RG_FolderBrowser(object):
        def __init__(self, path=None):
            self.set_path(path)

        def set_path(self, new_path):
            if new_path is not None:
                if not os.path.isdir(new_path):
                    raise ValueError("path <%s> does not exist or is not folder" % new_path)

            self.path = new_path

        def has_path(self):
            return self.path is not None

        def get_path(self):
            return self.path

        def _mk_tree(self):
            tree = RG_Tree()

            system = platform.system()
            roots = ["/"]

            if system == "Windows":
                for drive in range(ord('A'), ord('Z')):
                    if exists(chr(drive) + ':'):
                        roots.append(chr(drive))

            for root in roots:
                tree.add_item(root, root)

            def clickaction(tree, item_id):
                self.set_path(item_id)

            def expandaction(tree, item_id, expand):
                print tree, item_id, expand
                if not expand:
                    tree.remove_children(item_id)
                    tree.set_expanded(item_id, False, True)
                else:
                    tree.set_expanded(item_id)

                    subdirs = [name for name in os.listdir(item_id) if os.path.isdir(os.path.join(item_id, name))]

                    for subdir in sorted(subdirs):
                        subdir_id = os.path.join(item_id, subdir)

                        try:
                            os.listdir(subdir_id)
                        except Exception:
                            continue  # no rights

                        tree.add_item(subdir_id, subdir)
                        tree.set_item_parent(subdir_id, item_id)

            tree.set_item_click_action(clickaction)
            tree.set_expand_action(expandaction)

            return tree

        def open(self, label, on_ok):
            renpy.show_screen("_rg_folderbrowser_open", self, self._mk_tree(), label, on_ok)


    store.RG_FolderBrowser = RG_FolderBrowser


screen _rg_folderbrowser_open(folderbrowser, tree, label, on_ok):
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 500

        vbox:
            spacing 2

            if label is not None:
                hbox:
                    xfill True

                    label label:
                        xalign 0.5

            hbox:
                spacing 5
                ysize 30

                text _("Current directory:")
                text ("" if folderbrowser.get_path() is None else folderbrowser.get_path())

            viewport:
                ysize 350
                scrollbars "vertical"
                mousewheel "vertical"
                use rg_tree(tree)


screen rg_folderbrowser(folderbrowser, maxwidth, label=None, on_ok=None):
    hbox:
        spacing 5
        xmaximum maxwidth

        hbox:
            xsize maxwidth - (32+2)
            text ("" if folderbrowser.get_path() is None else folderbrowser.get_path())

        imagebutton:
            idle "components/icons/folder-tree.png"
            action Function(folderbrowser.open, label, on_ok)
