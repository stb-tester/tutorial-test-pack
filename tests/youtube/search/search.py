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
        region=stbt.Region(x=125, y=165, right=430, bottom=470),
        data=[
            "abcdef",
            "ghijkl",
            "mnopqr",
            "stuvwx",
            "yz1234",
            "567890"])
    BOTTOM_GRID = stbt.Grid(
        region=stbt.Region(x=125, y=470, right=430, bottom=525),
        data=[[" ", "DELETE", "CLEAR"]])

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
