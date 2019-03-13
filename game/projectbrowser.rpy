init python:
    import os

    def build_project_tree(debugger):
        old_state = debugger.tree_state
        tree = RG_Tree()

        for root, subdirs, files in os.walk(debugger.get_project_dir()):
            for folder in sorted(subdirs):
                item_id = os.path.join(root, folder)
                tree.add_item(item_id, folder)
                tree.set_item_parent(item_id, root)

            for source in sorted(files):
                if source.endswith(".rpy") or source.endswith(".py") or source.endswith(".rpym"):
                    item_id = os.path.join(root, source)
                    tree.add_item(os.path.join(root, source), source)
                    tree.set_item_parent(item_id, root)


        if old_state is not None:
            old_state.yield_state(tree)

        tree.set_item_click_action(debugger.on_buffer_select)
        return tree


screen projectbrowser():
    if debugger.has_project() and debugger.tree_state is not None:
        use rg_tree(debugger.tree_state)
