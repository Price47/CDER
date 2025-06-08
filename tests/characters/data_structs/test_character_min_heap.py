from typing import List

from src.characters.character import Character
from src.characters.data_structs.character_min_heap import CharacterHeap

default_config = {
    "hit_modifier": 2,
    "morale": 1,
    "behavior": {
        "target_priority": "most_healthy",
    },
}


def _characters() -> (List[Character], Character):
    min_char = Character(**{"hp": 1, "ac": 18, "config": default_config})
    return [
        Character(**{"hp": 30, "ac": 18, "config": default_config}),
        Character(**{"hp": 10, "ac": 18, "config": default_config}),
        Character(**{"hp": 35, "ac": 18, "config": default_config}),
        min_char,
    ], min_char


def test_character_min_heap():
    c_heap = CharacterHeap()
    [char_1, char_2, char_3, char_4], _ = _characters()

    c_heap.insert(char_1)
    assert c_heap.heap[0] == char_1

    c_heap.insert(char_2)
    # new char is lowest health, should be top of stack
    assert c_heap.heap[0] == char_2

    c_heap.insert(char_3)
    # should remain unchanged
    assert c_heap.heap[0] == char_2

    c_heap.insert(char_4)
    # new lowest health is char 4
    assert c_heap.heap[0] == char_4


def test_min_heapify():
    chars, min_char = _characters()
    c_heap = CharacterHeap(chars)

    # Last characters in the list should be smallest (top of queue)
    assert c_heap.heap[0] == min_char


def test_pop():
    chars, min_char = _characters()
    c_heap = CharacterHeap(chars)

    second_lowest_char = sorted(chars, key=lambda x: x.hp)[1]

    assert c_heap.pop() == min_char
    assert c_heap.heap[0] == second_lowest_char
    assert c_heap.pop() == second_lowest_char
