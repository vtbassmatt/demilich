from dataclasses import dataclass, field
from random import choice, uniform


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


def _get_bag_parts(bag: Bag):
    result = {}

    text_tags = bag.words_tagged("keyword")
    # convert to a set to dedupe keywords
    text = ", ".join(set([w.word for w in text_tags]))
    result['text'] = text

    mv_tags = list(bag.words_tagged("manavalue"))
    if mv_tags:
        result['instruction'] = f"{mv_tags[0].word} MV"
    else:
        result['instruction'] = ""

    return result


def _clean_keyword(raw: str):
    return raw.replace('_', ' ')


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
        for bag in self._creatures:
            yield Slot(
                self._rarity, self._frame, self._index + 1,
                **_get_bag_parts(bag),
            )
            self._index += 1
        for _ in self._spells:
            yield Slot(self._rarity, self._frame, self._index + 1, "Spell")
            self._index += 1

    def keywords(self, **kwargs: dict[str,float]):
        for keyword, count in kwargs.items():
            keyword = _clean_keyword(keyword)
            while count > 1:
                tag = TaggedWord(keyword, "keyword")
                bag = choice(self._creatures)
                bag.add(tag)
                count -= 1
            if uniform(0.0, 1.0) < count:
                tag = TaggedWord(keyword, "keyword")
                bag = choice(self._creatures)
                bag.add(tag)

    def mana_values(self, *args: int|tuple[int]):
        if len(args) != len(self._creatures):
            raise ValueError("incorrect number of mana values passed: "
                             f"expected {len(self._creatures)} "
                             f"but got {len(args)}")
        for mv, bag in zip(args, self._creatures):
            if isinstance(mv, int):
                mv = str(mv)
            else:
                mv = "/".join([str(x) for x in mv])
            tag = TaggedWord(mv, "manavalue")
            bag.add(tag)
