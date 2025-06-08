from src.characters.character import Character
from src.characters.data_structs.attribute_heap import AttributeHeap


class CharacterHeap(AttributeHeap[Character]):
    """
    Min heap priority queue implementation for characters, using one of
    its attributes like AC or HP
    """

    def _attr(self, c: Character):
        attr_val = getattr(c, self.config.heapify_attribute)

        # To use a max based ordering, just do the same as min but with negative value
        if self.config.order == "max":
            attr_val = -attr_val

        return attr_val
