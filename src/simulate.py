from typing import List

from character import Character
from src.roll.dice import D4
from src.roll.dice_pool import RollXDX


def turn():
    characters: List[Character]

if __name__ == '__main__':
    rdx = RollXDX(x=20, dx=D4)
    print(rdx.roll())
