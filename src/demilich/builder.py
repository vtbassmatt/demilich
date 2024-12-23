from enum import Enum
from typing import Iterable

from demilich.restrictions import Restriction
from demilich.skeleton_builder import Slot


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


class DataTypes(Enum):
    MANA_VALUES = 'mv'
    SIZES = 'sz'
    KEYWORDS = 'kw'
    RACES = 'ra'
    CLASSES = 'cl'
    SPELLS = 'sp'


def make_blank_data():
    return {
        DataTypes.MANA_VALUES: [],
        DataTypes.SIZES: [],
        DataTypes.KEYWORDS: {},
        DataTypes.RACES: {},
        DataTypes.CLASSES: {},
        DataTypes.SPELLS: [],
    }


def slotcode(rarity: Rarity, frame: Frame, number: int):
    return f"{rarity.value}{frame.name}{number:02}"


class ModeError(Exception): pass


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
    
    def _current(self) -> dict:
        if not self._working_frame:
            raise ModeError('no frame is selected')

        match self._working_rarity:
            case Rarity.COMMON:
                return self._common_slots[self._working_frame]
            case _:
                raise NotImplementedError()

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
    def creatures(self):
        self._in_creature_mode = True
        return self

    def _check_creature_length(self, length: int, source: str):
        slots = None

        match self._working_rarity:
            case Rarity.COMMON:
                slots = self._common_slot_counts
            case _:
                raise NotImplementedError()
        
        if length > slots[self._working_frame]:
            raise ValueError(f"error in {self._working_rarity.name} {self._working_frame.value} {source}: more creatures specified than slots available")

    def mana_values(self, *args: list[int|tuple[int, ...]]):
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to define mana values")
        self._check_creature_length(len(args), "mana values")

        # check these are sensible
        for mv in args:
            if isinstance(mv, int):
                continue
            elif isinstance(mv, (tuple, list)):
                for sub_mv in mv:
                    if not isinstance(sub_mv, int):
                        raise ValueError(f"mana values {mv} - everything in the tuple must be an int")
            else:
                raise TypeError(f"mana values expected int or tuple of int, got {type(mv)} for {mv}")

        self._current()[DataTypes.MANA_VALUES] = args
        
        return self

    def sizes(self, *args: list[tuple[int,int]]):
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to define sizes")
        self._check_creature_length(len(args), "sizes")

        # check these are sensible
        for size in args:
            match size:
                case (int(), int()):
                    pass
                case _:
                    raise ValueError(f"sizes {size} must be a tuple of pow/tou values")

        self._current()[DataTypes.SIZES] = args

        return self

    def with_keywords(self, **kwargs: int|float):
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to select keywords")
        
        # check these are sensible
        for keyword, frequency in kwargs.items():
            if keyword not in self._keywords:
                raise ValueError(f"{keyword} is not a known keyword; define it first using .{self.create_keywords.__name__}()")

            match frequency:
                case int() | float():
                    pass
                case _:
                    raise ValueError(f"keywords: {keyword} must specify an int or float frequency")

        self._current()[DataTypes.KEYWORDS] = kwargs

        return self

    def from_races(self, **kwargs: int|float):
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to select races")
        
        # check these are sensible
        for race, frequency in kwargs.items():
            if race not in self._races:
                raise ValueError(f"{race} is not a known race; define it first using .{self.create_races.__name__}()")

            match frequency:
                case int() | float():
                    pass
                case _:
                    raise ValueError(f"races: {race} must specify an int or float frequency")

        self._current()[DataTypes.RACES] = kwargs

        return self

    def from_classes(self, none=int|float, **kwargs: int|float):
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to select classes")
        
        # check these are sensible
        for class_, frequency in kwargs.items():
            if class_ not in self._classes:
                raise ValueError(f"{class_} is not a known class; define it first using .{self.create_classes.__name__}()")

            match frequency:
                case int() | float():
                    pass
                case _:
                    raise ValueError(f"classes: {class_} must specify an int or float frequency")

        self._current()[DataTypes.CLASSES] = kwargs

        return self

    def restrict(self, **kwargs: Restriction):
        raise NotImplementedError()
        if not self._in_creature_mode:
            raise ModeError("must be in creature mode to set up restrictions")
        return self
        
    # configure spell slots
    def spells(self):
        self._in_creature_mode = False
        return self

    def instruction(self, text: str, mana: str|None = None): return self
    def card(self, name: str, text: str, mana: str): return self

    # build a skeleton
    def build(self) -> Iterable[Slot]:
        # TODO: if there are no slots, raise
        # raise ValueError("no slots defined")

        for rarity in (self._common_slots, ):
            for frame in Frame:
                for index in range(self._common_slot_counts[frame]):
                    if index < len(self._common_slots[frame][DataTypes.MANA_VALUES]):
                        yield Slot('C', frame.name, index+1, f'{self._common_slots[frame][DataTypes.MANA_VALUES][index]}')
                    else:
                        yield Slot('C', frame.name, index+1, 'spell')

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
    _common_slots = {
        Frame.W: make_blank_data(),
        Frame.U: make_blank_data(),
        Frame.B: make_blank_data(),
        Frame.R: make_blank_data(),
        Frame.G: make_blank_data(),
        Frame.A: make_blank_data(),
        Frame.Z: make_blank_data(),
    }
    _common_slot_counts = {
        Frame.W: 0,
        Frame.U: 0,
        Frame.B: 0,
        Frame.R: 0,
        Frame.G: 0,
        Frame.A: 0,
        Frame.Z: 0,
    }
    # creature mode enables things like sizes, keywords, races, and classes
    # outside of creature mode (spell mode), these concepts don't make sense
    _in_creature_mode = False
