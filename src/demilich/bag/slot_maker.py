from dataclasses import dataclass, field


@dataclass
class Slot:
    rarity: str
    color: str
    number: int
    instruction: str
    id: str = field(init=False)
    name: str = ''
    cost: str = ''
    typeline: str = ''
    text: str = ''
    stats: str | None = None

    def __post_init__(self):
        self.id = f"{self.rarity}{self.color}{self.number:02}"


@dataclass
class TaggedWord:
    word: str
    tag: str


class Bag:
    def __init__(self, *args: list[TaggedWord]):
        self._bag: list[TaggedWord] = args or []

    def add(self, word: TaggedWord):
        self._bag.append(word)

    def words(self):
        yield from self._bag
    
    def words_tagged(self, tag: str):
        for word in self._bag:
            if word.tag == tag:
                yield word


class SlotMaker:
    def __init__(self, rarity: str, frame: str, creatures: int, spells: int):
        self._rarity = rarity
        self._frame = frame
        self._creatures = [Bag() for _ in range(creatures)]
        self._spells = [Bag() for _ in range(spells)]
        # internal bookkeeping
        self._index = -1

    def __iter__(self):
        self._index += 1
        for _ in self._creatures:
            yield Slot(self._rarity, self._frame, self._index + 1, "Creature")
            self._index += 1
        for _ in self._spells:
            yield Slot(self._rarity, self._frame, self._index + 1, "Spell")
            self._index += 1
