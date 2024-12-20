from enum import Enum

from demilich.restrictions import Restriction


class Rarity(Enum):
    COMMON = 'C'
    UNCOMMON = 'U'
    RARE = 'R'
    MYTHIC = 'M'


class Frame(Enum):
    W = 'white'
    U = 'blue'
    B = 'black'
    R = 'red'
    G = 'green'
    A = 'artifact'
    Z = 'multicolor'


def slotcode(rarity: Rarity, frame: Frame, number: int):
    return f"{rarity.value}{frame.name}{number:02}"


class SkeletonBuilder():
    # general skeleton setup
    def create_keywords(self, **kwargs: str):
        self._keywords.update(kwargs)
        return self
    
    def create_races(self, **kwargs: str):
        self._races.update(kwargs)
        return self

    def create_classes(self, **kwargs: str):
        self._classes.update(kwargs)
        return self

    # work on a particular rarity
    def common(self):
        self._working_rarity = Rarity.COMMON
        return self

    def uncommon(self):
        self._working_rarity = Rarity.UNCOMMON
        return self

    def rare(self):
        self._working_rarity = Rarity.RARE
        return self

    def mythic(self):
        self._working_rarity = Rarity.MYTHIC
        return self

    # work on a particular color/frame
    def _set_color_and_slots(self, slots: int, frame: Frame):
        self._working_frame = frame

        match self._working_rarity:
            case Rarity.COMMON:
                self._common_slot_counts[frame] = slots
            case _:
                raise NotImplementedError()

        return self

    def white(self, slots: int):
        return self._set_color_and_slots(slots, Frame.W)
    def blue(self, slots: int):
        return self._set_color_and_slots(slots, Frame.U)
    def black(self, slots: int):
        return self._set_color_and_slots(slots, Frame.B)
    def red(self, slots: int):
        return self._set_color_and_slots(slots, Frame.R)
    def green(self, slots: int):
        return self._set_color_and_slots(slots, Frame.G)
    def artifact(self, slots: int):
        return self._set_color_and_slots(slots, Frame.A)
    def multicolor(self, slots: int):
        return self._set_color_and_slots(slots, Frame.Z)

    # configure creature slots
    def creatures(self): return self
    def mana_values(self, *args: list[int|tuple[int, ...]]): return self
    def sizes(self, *args: list[tuple[int,int]]): return self
    def with_keywords(self, **kwargs: int|float): return self
    def from_races(self, **kwargs: int|float): return self
    def from_classes(self, none=int|float, **kwargs: int|float): return self
    def restrict(self, **kwargs: Restriction): return self

    # configure spell slots
    def spells(self): return self
    def instruction(self, text: str, mana: str|None = None): return self
    def card(self, name: str, text: str, mana: str): return self

    # inspection helpers
    def __str__(self):
        return f"""--------------------------
Skeleton Builder internals
--------------------------
Keywords: {[v for v in self._keywords.values()]}
Races: {[v for v in self._races.values()]}
Classes: {[v for v in self._classes.values()]}

Common slots:
  W: {self._common_slot_counts[Frame.W]}
  U: {self._common_slot_counts[Frame.U]}
  B: {self._common_slot_counts[Frame.B]}
  R: {self._common_slot_counts[Frame.R]}
  G: {self._common_slot_counts[Frame.G]}
  A: {self._common_slot_counts[Frame.A]}
  Z: {self._common_slot_counts[Frame.Z]}
Total: {sum(self._common_slot_counts.values())}
"""

    _keywords = {}
    _races = {}
    _classes = {}
    # default to common so we don't have to handle the None case everywhere
    _working_rarity: Rarity = Rarity.COMMON
    # it's not clear what a default frame would mean, so we'll handle
    _working_frame: Frame|None = None
    _common_slots = {}
    _common_slot_counts = {
        Frame.W: 0,
        Frame.U: 0,
        Frame.B: 0,
        Frame.R: 0,
        Frame.G: 0,
        Frame.A: 0,
        Frame.Z: 0,
    }
