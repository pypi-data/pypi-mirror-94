from pathlib import Path


def get_pages():
    from test_pages.entry_page import entry_page
    from test_pages.poweroff_page import poweroff_page
    from test_pages.sampler_page import sampler_page

    _background = str(Path(Path(__file__).parent, "assets/lcars_screen.png"))

    return [entry_page(), sampler_page(_background), poweroff_page()]

