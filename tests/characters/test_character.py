from src.characters.character import Character
from tests.characters.utils import _character_json


# Hit #
def test_from_json_method():
    c = Character.from_json(_character_json())

    assert c.ac == 18
    assert c.target_priority == "most_healthy"
