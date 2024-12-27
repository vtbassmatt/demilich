from dataclasses import dataclass, field
from random import choice, choices, uniform


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
class Reprint:
    name: str
    cost: str
    type_: str
    subtype: list[str]|None
    text: str


@dataclass
class TaggedWord:
    word: str
    tag: str


class Bag:
    def __init__(self, *args: TaggedWord):
        self._bag: list[TaggedWord] = list(args) or []

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

    name_tags = list(bag.words_tagged('name'))
    if name_tags:
        result['name'] = name_tags[0].word

    keyword_tags = bag.words_tagged("keyword")
    # convert to a set to dedupe keywords
    keyword_text = ", ".join(set([w.word for w in keyword_tags]))
    text_tags = bag.words_tagged("text")
    text = " // ".join([t.word for t in text_tags])
    result['text'] = keyword_text
    if keyword_text and text:
        result['text'] += " // "
    if text:
        result['text'] += text

    mv_tags = list(bag.words_tagged("manavalue"))
    instruction_tags = list(bag.words_tagged("instruction"))
    if mv_tags:
        result['instruction'] = f"{mv_tags[0].word} MV"
    elif instruction_tags:
        result['instruction'] = f"{instruction_tags[0].word}"
    else:
        result['instruction'] = ""
    
    cost_tags = list(bag.words_tagged("cost"))
    if cost_tags:
        result['cost'] = cost_tags[0].word
    
    pow_tags = list(bag.words_tagged("power"))
    tou_tags = list(bag.words_tagged("toughness"))
    if pow_tags and tou_tags:
        result['stats'] = f"{pow_tags[0].word}/{tou_tags[0].word}"
    
    type_tags = list(bag.words_tagged("type"))
    type_ = " ".join([t.word for t in type_tags])
    subtypes = (
        list([s.word for s in bag.words_tagged('subtype')]) +
        list([r.word for r in bag.words_tagged('race')]) +
        list([c.word for c in bag.words_tagged('class')])
    )
    if subtypes:
        result['typeline'] = f"{type_.title()} — {" ".join([s.title() for s in subtypes])}"
    else:
        result['typeline'] = type_.title()

    return result


def _clean_keyword(raw: str):
    return raw.replace('_', ' ')


def _make_cost(mv: int|tuple[int], frame: str):
    if frame in 'WUBRGZ':
        if isinstance(mv, int):
            generic = mv-1
        else:
            generic = choice(mv) - 1
        
        color = 'H' if frame == 'Z' else frame
        if generic:
            return f"{{{generic}}}{{{color}}}"
        return f"{{{color}}}"

    else:
        if isinstance(mv, int):
            return f"{{{mv}}}"
        return f"{{{choice(mv)}}}"


def _infinite_shuffle(list_of_items):
    local_copy = list(list_of_items)
    try:
        while True:
            shuffle(local_copy)
            for element in local_copy:
                yield element
    finally:
        return

class SlotMaker:
    def __init__(self, rarity: str, frame: str, creatures: int, spells: int):
        self._rarity = rarity
        self._frame = frame
        if frame == 'A':
            self._creatures = [Bag(TaggedWord('artifact', 'type'), TaggedWord('creature', 'type')) for _ in range(creatures)]
            self._spells = [Bag(TaggedWord('artifact', 'type')) for _ in range(spells)]
        else:
            self._creatures = [Bag(TaggedWord('creature', 'type')) for _ in range(creatures)]
            self._spells = [Bag() for _ in range(spells)]
        # internal bookkeeping
        self._index = -1
        self._next_spell = 0

    def __iter__(self):
        self._index += 1
        for bag in self._creatures:
            yield Slot(
                self._rarity, self._frame, self._index + 1,
                **_get_bag_parts(bag),
            )
            self._index += 1
        for bag in self._spells:
            yield Slot(
                self._rarity, self._frame, self._index + 1,
                **_get_bag_parts(bag),
            )
            self._index += 1

    def keywords(self, **kwargs: dict[str,float]):
        creatures = _infinite_shuffle(self._creatures)
        for keyword, count in kwargs.items():
            keyword = _clean_keyword(keyword)
            while count > 1:
                tag = TaggedWord(keyword, "keyword")
                bag = next(creatures)
                bag.add(tag)
                count -= 1
            if uniform(0.0, 1.0) < count:
                tag = TaggedWord(keyword, "keyword")
                bag = next(creatures)
                bag.add(tag)
        creatures.close()

    def mana_values(self, *args: int|tuple[int]):
        if len(args) != len(self._creatures):
            raise ValueError("incorrect number of mana values passed: "
                             f"expected {len(self._creatures)} "
                             f"but got {len(args)}")
        for mv, bag in zip(args, self._creatures):
            cost = _make_cost(mv, self._frame)
            if isinstance(mv, int):
                mv = str(mv)
            else:
                mv = "/".join([str(x) for x in mv])
            bag.add(TaggedWord(mv, "manavalue"))
            bag.add(TaggedWord(cost, "cost"))

    def powers(self, *args: int|tuple[int]):
        self._pt_tag('power', *args)

    def toughnesses(self, *args: int|tuple[int]):
        self._pt_tag('toughness', *args)

    def _pt_tag(self, _tag_word: str, *args: int|tuple[int]):
        if len(args) != len(self._creatures):
            raise ValueError(f"incorrect number of {_tag_word} passed: "
                             f"expected {len(self._creatures)} "
                             f"but got {len(args)}")
        for pt, bag in zip(args, self._creatures):
            if isinstance(pt, int):
                pt = str(pt)
            else:
                pt = str(choice(pt))
            tag = TaggedWord(pt, _tag_word)
            bag.add(tag)

    def races(self, **kwargs: dict[str,float]):
        self._choose_and_tag('race', **kwargs)

    def classes(self, **kwargs: dict[str,float]):
        self._choose_and_tag('class', **kwargs)

    def _choose_and_tag(self, _tag_word: str, **kwargs: dict[str,float]):
        if len(kwargs) == 0:
            raise ValueError(f"need at least one {_tag_word} passed in")

        distribution = choices(
            list(kwargs.keys()),
            weights=list(kwargs.values()),
            k=len(self._creatures)
        )
        for ch, bag in zip(distribution, self._creatures):
            if ch != "nothing":
                tag = TaggedWord(ch, _tag_word)
                bag.add(tag)

    def add_spell(self, instruction: str, *possibilities: Reprint):
        """Given a list of roughly equivalent reprints, choose one
        for the next spell slot."""
        try:
            bag = self._spells[self._next_spell]
        except IndexError:
            raise IndexError("too many spells; increase the number of spell slots")
        self._next_spell += 1

        bag.add(TaggedWord(instruction, 'instruction'))
        if len(possibilities) > 0:
            spell = choice(possibilities)
            bag.add(TaggedWord(spell.name, 'name'))
            bag.add(TaggedWord(spell.cost, 'cost'))
            bag.add(TaggedWord(spell.type_, 'type'))
            for subtype in spell.subtype or []:
                bag.add(TaggedWord(subtype, 'subtype'))
            bag.add(TaggedWord(spell.text, 'text'))
