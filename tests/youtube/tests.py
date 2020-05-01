"""Copyright 2019-2020 Stb-tester.com Ltd <support@stb-tester.com>"""

from .pages.search import Search


def test_youtube_keyboard():
    """Showcases the keyboard navigation APIs used in `youtube.Search`

    Precondition: Already at the YouTube Search page.
    """
    page = Search()
    assert page, "Not at the YouTube Search page"
    page.enter_text("peppa pig")
