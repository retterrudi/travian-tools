from dataclasses import dataclass
from typing import KeysView


@dataclass
class Resources:
    lumber: int = 0
    clay: int = 0
    iron: int = 0
    crop: int = 0

    def __add__(self, other: 'Resources'):
        if isinstance(other, Resources):
            return Resources(
                self.lumber + other.lumber,
                self.clay + other.clay,
                self.iron + other.iron,
                self.crop + other.crop
            )
        else:
            raise TypeError("Can only add Resources objects to each other")

    def __sub__(self, other: 'Resources'):
        if isinstance(other, Resources):
            return Resources(
                self.lumber - other.lumber,
                self.clay - other.clay,
                self.iron - other.iron,
                self.crop - other.crop
            )
        else:
            raise TypeError("Can only subtract Resources objects from each other")

    def __mul__(self, other: int):
        if isinstance(other, int):
            return Resources(
                self.lumber * other,
                self.clay * other,
                self.iron * other,
                self.crop * other
            )
        else:
            return NotImplemented

    def __rmul__(self, other: int):
        return self.__mul__(other)

    def __getitem__(self, key: str) -> int:
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise KeyError(f"Resource '{key}' not found")

    def keys(self) -> KeysView:
        """Return a view object that displays a list of all the keys."""
        return self.__dict__.keys()

    def sum(self) -> int:
        return self.lumber + self.clay + self.iron + self.crop

    def has_negative_resources(self) -> bool:
        return any([self.lumber < 0, self.clay < 0, self.iron < 0, self.crop < 0])
