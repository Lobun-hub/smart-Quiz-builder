import pytest

from theme_manager import THEMES


@pytest.mark.parametrize("theme", ["Ocean", "Forest", "Desert"])
@pytest.mark.parametrize("mode", ["light", "dark"])
def test_theme_palette_defines_readable_app_and_button_colors(theme, mode):
    palette = THEMES[theme][mode]

    assert palette["background"].startswith("#")
    assert palette["secondary"].startswith("#")
    assert palette["text"].startswith("#")
    assert palette["primary"].startswith("#")
    assert palette["button_text"].startswith("#")
