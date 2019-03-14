init python hide:
    import collections

    class RG_Tree(object):

        def __init__(self, autoselect=False):
            self.all_items = collections.OrderedDict()
            self.captions = {}
            self.parents = {}
            self.expanded = set()

            self.item_click_action = None
            self.expand_action = None
            self.selected = None
            self.autoselect = autoselect

        def yield_state(self, other):
            for item_id in self.all_items:
                if item_id in other.all_items:
                    if item_id in self.expanded:
                        other.expanded.add(item_id)

            other.expand_action = self.expand_action
            other.item_click_action = self.item_click_action
            other.selected = self.selected
            other.autoselect = self.autoselect

        def add_item(self, item_id, item_caption=None):
            self.all_items[item_id] = None
            self.captions[item_id] = None
            if item_caption is not None:
                self.set_item_caption(item_id, item_caption)

        def remove_item(self, item_id):
            if item_id in self.all_items:
                for child_id in self.get_children(item_id):
                    self.remove_item_parent(child_id)
                    self.set_expanded(child_id, False)
                self.all_items.pop(item_id)
                self.captions.pop(item_id, None)
                if item_id in self.expanded:
                    self.expanded.remove(item_id)

        def set_expanded(self, item_id, expanded=True, recursive=False):
            if expanded and item_id not in self.expanded:
                self.expanded.add(item_id)
            elif not expanded and item_id in self.expanded:
                self.expanded.remove(item_id)

            if recursive:
                for child in self.get_children(item_id):
                    self.set_expanded(child, expanded, recursive)

        def set_item_caption(self, item_id, item_caption):
            if item_id in self.all_items:
                self.captions[item_id] = item_caption

        def set_item_parent(self, item_id, parent_id):
            if item_id in self.all_items and parent_id in self.all_items:
                self.parents[item_id] = parent_id

        def remove_item_parent(self, item_id):
            if item_id in self.all_items:
                self.parents.pop(item_id, None)

        def get_roots(self):
            for item_id in self.all_items:
                if item_id not in self.parents:
                    yield item_id

        def get_item_caption(self, item_id):
            return self.captions[item_id]

        def get_item_click_action(self, item_id):
            if item_id in self.click_actions:
                return self.click_actions[item_id]

        def has_children(self, item_id):
            return item_id in self.parents.values()

        def get_children(self, item_id):
            all_children = set()
            for child_id in self.parents:
                if self.parents[child_id] == item_id:
                    all_children.add(child_id)

            for item_id in self.all_items:
                if item_id in all_children:
                    yield item_id

        def remove_children(self, item_id):
            for child in list(self.get_children(item_id)):
                self._remove_child(child)

        def _remove_child(self, child):
            for subchild in list(self.get_children(child)):
                self._remove_child(subchild)

            self.remove_item(child)

        def get_parent(self, item_id):
            return self.parents[item_id]

        def is_expanded(self, item_id):
            return item_id in self.expanded

        def _get_expanded_tree(self):
            items = collections.deque()
            roots = self.get_roots()

            items.extend([(x, 0) for x in roots])

            while len(items) > 0:
                item_id, level = items.popleft()

                if level > 0:
                    parent_id = self.get_parent(item_id)
                    if parent_id not in self.expanded:
                        continue

                children = self.get_children(item_id)
                items.extendleft([(x, level+1) for x in reversed(list(children))])

                yield item_id, level

        def set_selected(self, item_id, expand=False):
            if item_id in self.all_items:
                self.selected = item_id
                parent = item_id
                while parent in self.parents:
                    parent = self.parents[parent]
                    self.set_expanded(parent, expanded=True)

        # item click event
        def set_item_click_action(self, action=lambda tree, item_id: None):
            self.item_click_action = action

        def remove_item_click_action(self):
            self.item_click_action = None

        def _item_clicked(self, item_id):
            if self.autoselect:
                self.selected = item_id

            self.item_click_action(self, item_id)

        def set_expand_action(self, action=lambda tree, item_id, expanded: None):
            self.expand_action = action

        def remove_expand_action(self):
            self.expand_action = None

        def _expand_event(self, item_id, expand):
            self.expand_action(self, item_id, expand)

    store.RG_Tree = RG_Tree


screen rg_tree(renpy_tree):
    vbox:
        for item_id, level in renpy_tree._get_expanded_tree():
            hbox:
                spacing 2

                # offset
                null width (level*32)

                # tree expand/unexpand
                if renpy_tree.has_children(item_id) or renpy_tree.expand_action is not None:
                    imagebutton:
                        if renpy_tree.expand_action is None:
                            if renpy_tree.is_expanded(item_id):
                                idle "_components/icons/tree-down.png"
                                action Function(renpy_tree.set_expanded, item_id, False)
                            else:
                                idle "_components/icons/tree-right.png"
                                action Function(renpy_tree.set_expanded, item_id, True)
                        else:
                            if renpy_tree.is_expanded(item_id):
                                idle "_components/icons/tree-down.png"
                                action Function(renpy_tree._expand_event, item_id, False)
                            else:
                                idle "_components/icons/tree-right.png"
                                action Function(renpy_tree._expand_event, item_id, True)
                else:
                    imagebutton:
                        idle "_components/icons/tree-right-unavailable.png"

                # tree item
                python:
                    txt = renpy_tree.get_item_caption(item_id)
                    if renpy_tree.selected == item_id:
                        txt = "{color=#00ff00}" + txt + "{/color}"
                textbutton txt:
                    action Function(renpy_tree._item_clicked, item_id)
                    sensitive renpy_tree.item_click_action is not None
