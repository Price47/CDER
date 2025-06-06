from typing import List, Literal
from copy import deepcopy

from pydantic import BaseModel

from src.characters.character import Character


class CharacterHeapConfig(BaseModel):
    # Attribute to use to compare characters for heap ops
    heapify_attribute: Literal["hp"]
    order: Literal["min", "max"]


class CharacterHeap:
    """
    Min heap priority queue implementation for characters, using one of
    its attributes like AC or HP
    """

    def __init__(
        self,
        initial_characters: List[Character] = None,
        *,
        config: CharacterHeapConfig = None,
    ):
        self.config = config or CharacterHeapConfig(heapify_attribute="hp", order="min")
        self.heap: List[Character] = initial_characters or []

        # After setting self's values, if a list was provided, min heapify it
        if initial_characters:
            self.heapify()

    # TODO: Add Tests for max and other attrs
    def _attr(self, c: Character):
        attr_val = getattr(c, self.config.heapify_attribute)

        # To use a max based ordering, just do the same as min but with negative value
        if self.config.order == "max":
            attr_val = -attr_val

        return attr_val

    def insert(self, char: Character):
        """
        Insert based on characters HP attribute
        """
        self.heap.append(char)
        idx = len(self.heap) - 1

        # compare to parent node
        while idx > 0 and self._attr(self.heap[(idx - 1) // 2]) > self._attr(
            self.heap[idx]
        ):
            # parent attribute is greater, swap nodes
            self.heap[idx], self.heap[(idx - 1) // 2] = (
                self.heap[(idx - 1) // 2],
                self.heap[idx],
            )
            idx = (idx - 1) // 2

    def _heapify(self, i, n):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self._attr(self.heap[left]) < self._attr(self.heap[smallest]):
            smallest = left

        if right < n and self._attr(self.heap[right]) < self._attr(self.heap[smallest]):
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify(smallest, n)

    def heapify(self):
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify(i, len(self.heap))

    def pop(self):
        root = self.heap[0]
        self.heap = self.heap[1::]
        self.heapify()
        return root

    def peek(self):
        """
        Important note, only peeking at the character reference so this is
        a COPY, not the actual reference
        """
        return deepcopy(self.heap[0])
