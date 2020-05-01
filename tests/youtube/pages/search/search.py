# coding: utf-8

"""Copyright 2019-2020 Stb-tester.com Ltd <support@stb-tester.com>"""

import networkx
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

    _graph = networkx.compose_all([
        stbt.grid_to_navigation_graph(KEYBOARD_GRID),
        stbt.grid_to_navigation_graph(BOTTOM_GRID),
        stbt.Keyboard.parse_edgelist("""
            5 SPACE KEY_DOWN
            6 SPACE KEY_DOWN
            7 BACKSPACE KEY_DOWN
            8 BACKSPACE KEY_DOWN
            9 CLEAR KEY_DOWN
            0 CLEAR KEY_DOWN
            SPACE 5 KEY_UP
            SPACE 6 KEY_UP
            BACKSPACE 7 KEY_UP
            BACKSPACE 8 KEY_UP
            CLEAR 9 KEY_UP
            CLEAR 0 KEY_UP
        """)])
    _kb = stbt.Keyboard(_graph)

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
        assert False, "Matched selection %r outside of known locations" \
            % (m.region,)

    def enter_text(self, text):
        return Search._kb.enter_text(text.lower(), page=self)

    def clear(self):
        page = self
        page = Search._kb.navigate_to("CLEAR", page)
        stbt.press_and_wait("KEY_OK")  # pylint:disable=stbt-unused-return-value
        return page.refresh()
