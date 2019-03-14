
python early hide:
    import pygame_sdl2 as pygame

    class RG_ClickArea(renpy.display.viewport.Viewport):
        def __init__(self, *args, **kwargs):
            super(RG_ClickArea, self).__init__(*args, **kwargs)

            self.click_callback = None
            if "click" in kwargs:
                self.click_callback = kwargs["click"]

        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self.click_callback is not None and self.offsets is not None:
                if x>=0 and x<self.width and y>=0 and y<=self.height:  # event for us
                    print self.offsets
                    child_x = -self.offsets[0][0] + x
                    child_y = -self.offsets[0][1] + y
                    self.click_callback(x, y, child_x, child_y, ev, st)

            super(RG_ClickArea, self).event(ev, x, y, st)


    store.RG_ClickArea = RG_ClickArea

    _rg_clickarea =  renpy.ui.Wrapper(RG_ClickArea, one=True, replaces=True, style='viewport')

    def rg_clickarea_sl2(context=None, **kwargs):
        """
        This converts the output of renpy.ui.viewport into something that
        sl.displayable can use.
        """

        d = renpy.ui.detached()

        if context is not None:
            renpy.ui.stack[-1].style_prefix = context.style_prefix

        vp = renpy.ui.viewport_common(_rg_clickarea, True, **kwargs)

        renpy.ui.stack.pop()

        rv = d.child

        if vp is not rv:
            rv._main = vp

        rv._composite_parts = list(rv.children)

        return rv

    clickarea = renpy.register_sl_displayable("clickarea", rg_clickarea_sl2, "viewport", nchildren=1)
    clickarea.add_property("click")
    # viewport defaults
    clickarea.add_property_group("position")
    clickarea.add_property("child_size")
    clickarea.add_property("mousewheel")
    clickarea.add_property("draggable")
    clickarea.add_property("edgescroll")
    clickarea.add_property("xadjustment")
    clickarea.add_property("yadjustment")
    clickarea.add_property("xinitial")
    clickarea.add_property("yinitial")
    clickarea.add_property("scrollbars")
    clickarea.add_property("arrowkeys")
    clickarea.add_property("pagekeys")
