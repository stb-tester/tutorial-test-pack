# coding: utf-8
"""Copyright 2019 Stb-tester.com Ltd <support@stb-tester.com>"""

import stbt


class Search(stbt.FrameObject):
    """The "Search" page of the YouTube app.

    This is a *Page Object* because it inherits from `stbt.FrameObject`.
    For more information about Page Objects see
    <https://stb-tester.com/manual/object-repository>.
    """

    KEYBOARD_GRID = stbt.Grid(
        region=stbt.Region(x=125, y=140, right=430, bottom=445),
        data=[
            "abcdef",
            "ghijkl",
            "mnopqr",
            "stuvwx",
            "yz1234",
            "567890"])
    BOTTOM_GRID = stbt.Grid(
        region=stbt.Region(x=125, y=445, right=430, bottom=500),
        data=[[" ", "DELETE", "CLEAR"]])

    _kb = stbt.Keyboard("""
        a b KEY_RIGHT
        a g KEY_DOWN
        b a KEY_LEFT
        b c KEY_RIGHT
        b h KEY_DOWN
        c b KEY_LEFT
        c d KEY_RIGHT
        c i KEY_DOWN
        d c KEY_LEFT
        d e KEY_RIGHT
        d j KEY_DOWN
        e d KEY_LEFT
        e f KEY_RIGHT
        e k KEY_DOWN
        f e KEY_LEFT
        f l KEY_DOWN
        g a KEY_UP
        g h KEY_RIGHT
        g m KEY_DOWN
        h b KEY_UP
        h g KEY_LEFT
        h i KEY_RIGHT
        h n KEY_DOWN
        i c KEY_UP
        i h KEY_LEFT
        i j KEY_RIGHT
        i o KEY_DOWN
        j d KEY_UP
        j i KEY_LEFT
        j k KEY_RIGHT
        j p KEY_DOWN
        k e KEY_UP
        k j KEY_LEFT
        k l KEY_RIGHT
        k q KEY_DOWN
        l f KEY_UP
        l k KEY_LEFT
        l r KEY_DOWN
        m g KEY_UP
        m n KEY_RIGHT
        m s KEY_DOWN
        n h KEY_UP
        n m KEY_LEFT
        n o KEY_RIGHT
        n t KEY_DOWN
        o i KEY_UP
        o n KEY_LEFT
        o p KEY_RIGHT
        o u KEY_DOWN
        p j KEY_UP
        p o KEY_LEFT
        p q KEY_RIGHT
        p v KEY_DOWN
        q k KEY_UP
        q p KEY_LEFT
        q r KEY_RIGHT
        q w KEY_DOWN
        r l KEY_UP
        r q KEY_LEFT
        r x KEY_DOWN
        s m KEY_UP
        s t KEY_RIGHT
        s y KEY_DOWN
        t n KEY_UP
        t s KEY_LEFT
        t u KEY_RIGHT
        t z KEY_DOWN
        u o KEY_UP
        u t KEY_LEFT
        u v KEY_RIGHT
        u 1 KEY_DOWN
        v p KEY_UP
        v u KEY_LEFT
        v w KEY_RIGHT
        v 2 KEY_DOWN
        w q KEY_UP
        w v KEY_LEFT
        w x KEY_RIGHT
        w 3 KEY_DOWN
        x r KEY_UP
        x w KEY_LEFT
        x 4 KEY_DOWN
        y s KEY_UP
        y z KEY_RIGHT
        y 5 KEY_DOWN
        z t KEY_UP
        z y KEY_LEFT
        z 1 KEY_RIGHT
        z 6 KEY_DOWN
        1 u KEY_UP
        1 z KEY_LEFT
        1 2 KEY_RIGHT
        1 7 KEY_DOWN
        2 v KEY_UP
        2 1 KEY_LEFT
        2 3 KEY_RIGHT
        2 8 KEY_DOWN
        3 w KEY_UP
        3 2 KEY_LEFT
        3 4 KEY_RIGHT
        3 9 KEY_DOWN
        4 x KEY_UP
        4 3 KEY_LEFT
        4 0 KEY_DOWN
        5 y KEY_UP
        5 6 KEY_RIGHT
        5 SPACE KEY_DOWN
        6 z KEY_UP
        6 5 KEY_LEFT
        6 7 KEY_RIGHT
        6 SPACE KEY_DOWN
        7 1 KEY_UP
        7 6 KEY_LEFT
        7 8 KEY_RIGHT
        7 BACKSPACE KEY_DOWN
        8 2 KEY_UP
        8 7 KEY_LEFT
        8 9 KEY_RIGHT
        8 BACKSPACE KEY_DOWN
        9 3 KEY_UP
        9 8 KEY_LEFT
        9 0 KEY_RIGHT
        9 CLEAR KEY_DOWN
        0 4 KEY_UP
        0 9 KEY_LEFT
        0 CLEAR KEY_DOWN
        SPACE 5 KEY_UP
        SPACE 6 KEY_UP
        BACKSPACE 7 KEY_UP
        BACKSPACE 8 KEY_UP
        CLEAR 9 KEY_UP
        CLEAR 0 KEY_UP
    """)

    @property
    def is_visible(self):
        """Are we on YouTube's Search page?

        Note: An instance of this class is truthy if ``is_visible`` returns
        True, thanks to `stbt.FrameObject` magic.
        """
        return stbt.match("Search.png", frame=self._frame)

    @property
    def selection(self):
        """The name of the selected button on the on-screen keyboard.

        For example 'g' or 'CLEAR'.
        """
        m = stbt.match("selection.png", frame=self._frame,
                       region=stbt.Region.bounding_box(
                           Search.KEYBOARD_GRID.region,
                           Search.BOTTOM_GRID.region))
        for grid in [Search.KEYBOARD_GRID, Search.BOTTOM_GRID]:
            try:
                text = grid.get(region=m.region).data
                return text
            except IndexError:
                pass
        assert False, "Matched selection %r outside of known locations" % (m.region,)

    def enter_text(self, text):
        return Search._kb.enter_text(text.lower(), page=self)

    def clear(self):
        page = self
        page = Search._kb.navigate_to("CLEAR", page)
        stbt.press_and_wait("KEY_OK")
        return page.refresh()
