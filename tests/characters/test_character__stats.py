import pytest

from src.characters.character import Character
from tests.characters.utils import _character_json


# Stats #
@pytest.mark.parametrize(
    "strength,expected_modifier",
    [
        pytest.param(1, -5, id="1"),
        pytest.param(2, -4, id="2"),
        pytest.param(3, -4, id="3"),
        pytest.param(4, -3, id="4"),
        pytest.param(5, -3, id="5"),
        pytest.param(6, -2, id="6"),
        pytest.param(7, -2, id="7"),
        pytest.param(8, -1, id="8"),
        pytest.param(9, -1, id="9"),
        pytest.param(10, 0, id="10"),
        pytest.param(11, 0, id="11"),
        pytest.param(12, 1, id="12"),
        pytest.param(13, 1, id="13"),
        pytest.param(14, 2, id="14"),
        pytest.param(15, 2, id="15"),
        pytest.param(16, 3, id="16"),
        pytest.param(17, 3, id="17"),
        pytest.param(18, 4, id="18"),
        pytest.param(19, 4, id="19"),
        pytest.param(20, 5, id="20"),
        pytest.param(21, 5, id="21"),
        pytest.param(22, 6, id="22"),
        pytest.param(23, 6, id="23"),
        pytest.param(24, 7, id="24"),
        pytest.param(25, 7, id="25"),
        pytest.param(26, 8, id="26"),
        pytest.param(27, 8, id="27"),
        pytest.param(28, 9, id="28"),
        pytest.param(29, 9, id="29"),
        pytest.param(30, 10, id="30"),
    ],
)
def test_stat_modifier(strength, expected_modifier):
    c = Character.from_json(_character_json(strength=strength))
    assert c.stats.str_modifier == expected_modifier
