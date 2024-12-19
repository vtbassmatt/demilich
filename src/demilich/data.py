from dataclasses import dataclass


_COMMON_CREATURE_COUNTS = [
    # W U  B  R  G
    11, 8, 9, 9, 10
]

_UNCOMMON_CREATURE_COUNTS = [
    # W U    B    R    G
    10, 6.5, 7.5, 7.5, 9
]

_UNCOMMON_SLOTS_PER_COLOR = 14

_COMMON_KEYWORDS = {
    #                 W    U    B     R    G
    "flying":        [3,   3,   2,    0,   0],
    "vigilance":     [2,   1.5, 0,    0,   1.5],
    "lifelink":      [1,   0,   1,    0,   0],
    "first strike":  [.25, 0,   0,    .25, 0],
    "double strike": [.2,  0,   0,    .2,  0],
    "ward N":        [0,   .5,  0,    0,   .5],
    "defender":      [0,   .5,  0,    0,   0],
    "flash":         [0,   .5,  0,    0,   0],
    "menace":        [0,   0,   1.5,  1.5, 0],
    "deathtouch":    [0,   0,   1.25, 0,   1],
    "trample":       [0,   0,   0,    1.5, 1.5],
    "haste":         [0,   0,   0,    1.5, .2],
    "reach":         [0,   0,   0,    1,   1.5],
}
_KEYWORD_BOOSTS = {
    'flying': (-1, -1),
    'trample': (1, 0),
    'defender': (-3, 0),
    'double strike': (-1, 0),
}

_COMMON_CREATURE_MV = {
    'W': [1, 2, 2, 2, 3, 3, 3, 4, 4, 5.5, 6.5],
    'U': [2, 2, 3, 3, 3, 4, 5.5, 6.5],
    'B': [1.5, 2, 2, 3, 3, 4, 4.5, 5.5, 6.5],
    'R': [1.5, 2, 2, 3, 3, 3.5, 4.5, 5, 6],
    'G': [1.5, 2, 2, 3, 3, 3.5, 4.5, 5, 6, 6.5],
}

_COMMON_CREATURE_SIZES = {
    'W': [(1, 1), (2, 2), (1, 2), (2, 2), (3, 3), (3, 3), (3, 3), (4, 4), (4, 4), (5, 6), (6, 6)],
    'U': [(2, 2), (2, 2), (3, 3), (3, 3), (3, 3), (4, 4), (5, 5), (5, 6)],
    'B': [(1, 1), (2, 1), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4), (5, 5), (6, 6)],
    'R': [(2, 1), (2, 2), (2, 2), (3, 3), (3, 3), (4, 3), (4, 4), (5, 5), (6, 6)],
    'G': [(1, 1), (2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 5), (5, 5), (6, 6), (6, 6)],
}

_WUBRG_RACES = ['Dinosaur', 'Dog', 'Spirit']
_COMMON_RACES = {
    'W': ['Human', 'Cat', 'Bird'] + _WUBRG_RACES,
    'U': ['Merfolk', 'Otter', 'Bird'] + _WUBRG_RACES,
    'B': ['Vampire', 'Zombie', 'Bat', 'Horror', 'Skeleton'] + _WUBRG_RACES,
    'R': ['Goblin', 'Devil', 'Ogre'] + _WUBRG_RACES,
    'G': ['Elf', 'Bear', 'Beast', 'Spider', 'Treefolk'] + _WUBRG_RACES,
}
_FLYING_RACES = ['Spirit', 'Bird', 'Dinosaur', 'Vampire']

_COMMON_CLASSES = {
    'W': ['Cleric', 'Knight', 'Monk', 'Mystic', 'Soldier', 'Nomad', 'Samurai', 'Scout'],
    'U': ['Wizard', 'Ninja', 'Pirate', 'Advisor', 'Rogue', 'Artificer'],
    'B': ['Warlock', 'Assassin', 'Knight', 'Minion', 'Rogue'],
    'R': ['Shaman', 'Artificer', 'Barbarian', 'Bard', 'Berserker', 'Pirate', 'Samurai', 'Warrior'],
    'G': ['Druid', 'Archer', 'Bard', 'Monk', 'Mystic', 'Ranger', 'Scout', 'Warrior'],
}

_UNCOMMON_RACES = _COMMON_RACES
_UNCOMMON_CLASSES = _COMMON_CLASSES

_ADJECTIVES = [
    'Ancient', 'Anointed', 'Brazen', 'Desperate', 'Frenzied', 'Gilded',
    'Looming', 'Prosperous', 'Apprentice', 'Shining', 'Territorial',
    'Ambush', 'Armored', 'Doomed', 'Elder', 'Feral', 'Grizzled',
    'Makeshift', 'Night', 'Day', 'One-Eyed', 'Selfless', 'Selfish',
    'Tormented', 'Unruly', 'Interloping', 'Village', 'Woodland',
    'Undead', 'Bellowing', 'Brave', 'Frilled', 'Intrepid', 'Rough',
    'Thieving', 'Guarded', 'Assistant', 'Tragic', 'Conscripted',
]

_COMMON_SPELLS = {
    'W': [
        "Combat-related removal",
        "Banishing Light",
        "Combat trick",
        "Disenchant/removal",
    ],
    'U': [
        "Protective instant",
        "Counterspell",
        "Cantrip",
        "Draw 2 or 3",
        "Witness Protection (aura)",
        "Top or bottom spell",
        "Modal spell",
    ],
    'B': [
        "Small conditional removal",
        "Combat trick",
        "Card draw at a cost",
        "Coercion+",
        "Unconditional removal",
        "Slightly overcosted removal",
    ],
    'R': [
        "Direct damage for 2",
        "Combat trick",
        "Rummage/impulse draw",
        "Modal Shatter",
        "Direct damage for 4 (efficient)",
        "Direct damage (5 mana, 6 damage)",
    ],
    'G': [
        "Fight spell",
        "Bite spell",
        "Combat trick (power pump)",
        "Mana acceleration",
        "Dig for lands and/or creatures",
    ],
}


@dataclass
class CommonsData:
    keywords: dict[str, float]
    creature_mana_values: list[float]
    creature_races: list[str]
    creature_classes: list[str]
    creature_sizes: list[tuple[int,int]]
    spells: list[str]


@dataclass
class UncommonsData:
    creature_count: float | int
    creature_races: list[str]
    creature_classes: list[str]
    total_slots: int


COMMON = {
    color: CommonsData({
            kw: values[index]
            for kw, values in _COMMON_KEYWORDS.items()
            if values[index] > 0
        },
        _COMMON_CREATURE_MV[color],
        _COMMON_RACES[color],
        _COMMON_CLASSES[color],
        _COMMON_CREATURE_SIZES[color],
        _COMMON_SPELLS[color],
    ) for index, color in enumerate('WUBRG')
}
UNCOMMON = {
    color: UncommonsData(
        _UNCOMMON_CREATURE_COUNTS[index],
        _UNCOMMON_RACES[color],
        _UNCOMMON_CLASSES[color],
        _UNCOMMON_SLOTS_PER_COLOR,
    ) for index, color in enumerate('WUBRG')
}
UNCOMMON_MULTICOLOR = ["enabler", "payoff"]
COMMON_ARTIFACT = [
    ('Two-mana creature (variance buster)', True, 2),
    ('Three-mana creature', True, 3),
    ('Four-mana creature', True, 4),
    ('Removal', False, None),
    ('Manalith+ ability', False, None),
    ('Land fixing', False, None),
]
UNCOMMON_ARTIFACT = (
    [('Creature', True, None)] * 4 + 
    [('Artifact', False, None)] * 3 + 
    [('Land', False, None)] * 3
)
UNCOMMON_LANDS = 3
ARTIFACT_RACES = ["Construct", "Toy", "Gnome", "Golem", "Gargoyle"]
ARTIFACT_NONRACES = ["Equipment", "Vehicle"]

FLYING_RACES = set(_FLYING_RACES)
ADJECTIVES = _ADJECTIVES
KEYWORD_BOOSTS = _KEYWORD_BOOSTS


class DesignSkeletonConfigError(ValueError): pass

def _validate_commons_data(
        creature_counts,
        keywords,
        creature_mv,
        creature_sizes,
        races,
        classes,
        spells,
):
    if len(creature_counts) != 5:
        raise DesignSkeletonConfigError(f"[common] {len(creature_counts)=}")
    if len(creature_mv.keys()) != 5:
        raise DesignSkeletonConfigError(f"[common] {len(creature_mv.keys())=}")
    
    color_count = {}

    for index, color in enumerate("WUBRG"):
        if color not in creature_mv.keys():
            raise DesignSkeletonConfigError(f"[common] expected {color} common creature MV list")
        if len(creature_mv[color]) != creature_counts[index]:
            raise DesignSkeletonConfigError(f"[common] {color} creature MV count expected to be {creature_counts[index]} but was {len(creature_mv[color])}")

        if color not in creature_sizes.keys():
            raise DesignSkeletonConfigError(f"[common] expected {color} common creature sizes list")
        if len(creature_sizes[color]) != creature_counts[index]:
            raise DesignSkeletonConfigError(f"[common] {color} creature sizes count expected to be {creature_counts[index]} but was {len(creature_mv[color])}")

        if color not in races.keys():
            raise DesignSkeletonConfigError(f"[common] expected {color} races list")
        if color not in classes.keys():
            raise DesignSkeletonConfigError(f"[common] expected {color} classes list")
        
        color_count[color] = len(creature_mv[color]) + len(spells[color])

    if not (color_count['W'] == color_count['U'] == color_count['B'] == color_count['R'] == color_count['G']):
        raise DesignSkeletonConfigError(f"[common] color counts are uneven: {color_count=}")

    for keyword, counts in keywords.items():
        if len(counts) != 5:
            raise DesignSkeletonConfigError(f"[common] {keyword} has {len(counts)} entries")


if __name__ == '__main__':
    _validate_commons_data(
        _COMMON_CREATURE_COUNTS,
        _COMMON_KEYWORDS,
        _COMMON_CREATURE_MV,
        _COMMON_CREATURE_SIZES,
        _COMMON_RACES,
        _COMMON_CLASSES,
        _COMMON_SPELLS,
    )
