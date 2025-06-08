from dataclasses import field
from typing import List, Literal
from copy import deepcopy

from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")  # Defines the TypeVar


class HeapConfig(BaseModel):
    # Attribute to use to compare characters for heap ops
    heapify_attribute: Literal["hp", "initiative"] = field(default="hp")
    order: Literal["min", "max"] = field(default="min")


class AttributeHeap(Generic[T]):
    """
    Min heap priority queue implementation using attributes from different types
    """

    def __init__(
        self, initial_entries: List[T] = None, *, config: HeapConfig = None, **kwargs
    ):
        self.heap: List[T] = initial_entries or []
        self.config = config or HeapConfig()

        # After setting self's values, if a list was provided, min heapify it
        if initial_entries:
            self.heapify()

    # TODO: Add Tests for max and other attrs
    def _attr(self, entry: T):
        attr_val = getattr(entry, self.config.heapify_attribute)

        # To use a max based ordering, just do the same as min but with negative value
        if self.config.order == "max":
            attr_val = -attr_val

        return attr_val

    def insert(self, entry: T):
        """
        Insert based on characters HP attribute
        """
        self.heap.append(entry)
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
