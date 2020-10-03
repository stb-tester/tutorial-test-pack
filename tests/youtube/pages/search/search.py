# coding: utf-8

"""Copyright 2019-2020 Stb-tester.com Ltd <support@stb-tester.com>"""

import stbt


top_grid = stbt.Grid(region=stbt.Region(x=145, y=125, right=410, bottom=160),
                     data=[["abc", "ABC", "#+-"]])
bottom_grid = stbt.Grid(region=stbt.Region(x=125, y=480, right=425, bottom=520),
                        data=[[" ", "DELETE", "CLEAR"]])
middle_region = stbt.Region(x=125, y=175, right=425, bottom=475)
middle_grids = {
    "lowercase": stbt.Grid(region=middle_region,
                           data=["abcdef",
                                 "ghijkl",
                                 "mnopqr",
                                 "stuvwx",
                                 "yz1234",
                                 "567890"]),
    "uppercase": stbt.Grid(region=middle_region,
                           data=["ABCDEF",
                                 "GHIJKL",
                                 "MNOPQR",
                                 "STUVWX",
                                 "YZ1234",
                                 "567890"]),
    "symbols": stbt.Grid(region=middle_region,
                         data=["!@#$%&",
                               "~*\\/?^",
                               "_`;:|=",
                               "éñ[]{}",
                               "çü.,+-",
                               "<>()'\""]),
}
KEYBOARD_REGION = stbt.Region(x=125, y=125, right=425, bottom=520)

def define_keyboard():
    kb = stbt.Keyboard()  # pylint:disable=redefined-outer-name
    for mode in ["lowercase", "uppercase", "symbols"]:
        kb.add_grid(top_grid, mode=mode)
        kb.add_grid(bottom_grid, mode=mode)
        g = middle_grids[mode]
        kb.add_grid(g, mode=mode)

        # Transitions between grids:
        #
        # abc ABC #+-  (top grid)
        # ↕ ↕ ↕ ↕ ↕ ↕
        # a b c d e f  (first row of middle grid)
        kb.add_transition(g[0, 0].data, "abc", "KEY_UP", mode=mode)
        kb.add_transition(g[1, 0].data, "abc", "KEY_UP", mode=mode)
        kb.add_transition(g[2, 0].data, "ABC", "KEY_UP", mode=mode)
        kb.add_transition(g[3, 0].data, "ABC", "KEY_UP", mode=mode)
        kb.add_transition(g[4, 0].data, "#+-", "KEY_UP", mode=mode)
        kb.add_transition(g[5, 0].data, "#+-", "KEY_UP", mode=mode)

        # 5 6 7 8 9 0  (last row of middle grid)
        # ↕ ↕ ↕ ↕ ↕ ↕
        # SPC DEL CLR  (bottom grid)
        kb.add_transition(g[0, 5].data, " ", "KEY_DOWN", mode=mode)
        kb.add_transition(g[1, 5].data, " ", "KEY_DOWN", mode=mode)
        kb.add_transition(g[2, 5].data, "DELETE", "KEY_DOWN", mode=mode)
        kb.add_transition(g[3, 5].data, "DELETE", "KEY_DOWN", mode=mode)
        kb.add_transition(g[4, 5].data, "CLEAR", "KEY_DOWN", mode=mode)
        kb.add_transition(g[5, 5].data, "CLEAR", "KEY_DOWN", mode=mode)

    # Transitions between modes:
    for source_mode in ["lowercase", "uppercase", "symbols"]:
        for name, target_mode in [("abc", "lowercase"),
                                  ("ABC", "uppercase"),
                                  ("#+-", "symbols")]:
            kb.add_transition(kb.find_key(name=name, mode=source_mode),
                              kb.find_key(name=name, mode=target_mode),
                              "KEY_OK")

    # Pressing KEY_PLAY cycles between the modes
    for source_mode, target_mode in [
            ("lowercase", "uppercase"),
            ("symbols", "lowercase"),
            # Pressing KEY_PLAY from "uppercase" goes to "lowercase" if you
            # have already typed an uppercase letter since entering uppercase
            # mode; if you haven't, it goes to "symbols". We don't keep track
            # of this past state in our model, so we model it as a
            # non-deterministic state machine -- that is, pressing KEY_PLAY
            # from "uppercase" might go to "symbols" or to "lowercase", we just
            # have to press it and then look at the screen to find out where we
            # landed.
            ("uppercase", "symbols"),
            ("uppercase", "lowercase")]:
        for key in kb.find_keys(mode=source_mode):
            target = kb.find_key(region=key.region, mode=target_mode)
            kb.add_transition(key, target, "KEY_PLAY")

    return kb


kb = define_keyboard()


class Search(stbt.FrameObject):
    """The "Search" page of the YouTube app.

    This is a *Page Object* because it inherits from `stbt.FrameObject`.
    For more information about Page Objects see
    <https://stb-tester.com/manual/object-repository>.
    """

    @property
    def is_visible(self):
        """Are we on YouTube's Search page?

        Note: An instance of this class is truthy if ``is_visible`` returns
        True, thanks to `stbt.FrameObject` magic.
        """
        return bool(self.selection)

    @property
    def selection(self):
        """The selected key of the on-screen keyboard."""
        for mode in ["lowercase", "uppercase", "symbols"]:
            match = stbt.find_selection_from_background(
                mode + ".png",
                max_size=(115, 70),
                frame=self._frame,
                mask=KEYBOARD_REGION)
            if match:
                return kb.find_key(region=match.region, mode=mode)

        return None

    def enter_text(self, text):
        return kb.enter_text(text, page=self)

    def clear(self):
        page = self
        page = kb.navigate_to("CLEAR", page)
        stbt.press_and_wait("KEY_OK")  # pylint:disable=stbt-unused-return-value
        return page.refresh()
