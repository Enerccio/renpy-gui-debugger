
python early hide:
    import weakref
    import pygame_sdl2 as pygame

    class TextInput(renpy.display.behavior.Input):
        _displayable_groups = {}

        def add_to_group(self):
            group = self.group

            if group not in TextInput._displayable_groups:
                TextInput._displayable_groups = weakref.WeakSet()
            TextInput._displayable_groups[group].add(self)

        def set_active(self):
            for ti in TextInput._displayable_groups[self.group]:
                ti.value.default = False
            self.value.default = True

        def __init__(self,
                 default="",
                 length=None,
                 style='input',
                 allow=None,
                 exclude=None,
                 prefix="",
                 suffix="",
                 changed=None,
                 button=None,
                 replaces=None,
                 editable=True,
                 pixel_width=None,
                 value=None,
                 copypaste=False,
                 **properties):

            super(TextInput, self).__init__(default, length, style, allow, exclude, prefix, suffix, changed, button, replaces, editable, pixel_width, value, copypaste, **properties)

            grp = properties["group"]
            self.group = grp if isinstance(grp, str) else grp[0]
            self.value.default = False if isinstance(grp, str) else grp[1]

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and x >= self.x and x <= self.x+self.w and y >= self.y and y <= self.y+self.h:
                self.set_active()

            super(self, TextInput).event(ev, x, y, st)

    textinput = renpy.register_sl_displayable("textinput", TextInput, "input")
    textinput.add_property("group")
    # input defaults
    textinput.add_property_group("position")
    textinput.add_property_group("text")
    textinput.add_property("value")
    textinput.add_property("default")
    textinput.add_property("length")
    textinput.add_property("pixel_width")
    textinput.add_property("allow")
    textinput.add_property("exclude")
    textinput.add_property("copypaste")
    textinput.add_property("prefix")
    textinput.add_property("suffix")
    textinput.add_property("changed")
