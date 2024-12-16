from dataclasses import dataclass


_COMMON_CREATURE_COUNTS = [
    # W U  B  R  G
    11, 8, 9, 9, 10
]

_UNCOMMON_CREATURE_COUNTS = [
    # W U    B    R    G
    10, 6.5, 7.5, 7.5, 9
]

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

_COMMON_CREATURE_MV = {
    'W': [1, 2, 2, 2, 3, 3, 3, 4, 4, 5.5, 6.5],
    'U': [2, 2, 3, 3, 3, 4, 5.5, 6.5],
    'B': [1.5, 2, 2, 3, 3, 4, 4.5, 5.5, 6.5],
    'R': [1.5, 2, 2, 3, 3, 3.5, 4.5, 5, 6],
    'G': [1.5, 2, 2, 3, 3, 3.5, 4.5, 5, 6, 6.5],
}


@dataclass
class ColorData:
    keywords: dict[str, float]
    mana_values: list[float]


COMMON = {
    color: ColorData({
            kw: values[index]
            for kw, values in _COMMON_KEYWORDS.items()
            if values[index] > 0
        },
        _COMMON_CREATURE_MV[color],
    ) for index, color in enumerate('WUBRG')
}


class DesignSkeletonConfigError(ValueError): pass

def _validate_commons_data(creature_counts, keywords, creature_mv):
    if len(creature_counts) != 5:
        raise DesignSkeletonConfigError(f"[common] {len(creature_counts)=}")
    if len(creature_mv.keys()) != 5:
        raise DesignSkeletonConfigError(f"[common] {len(creature_mv.keys())=}")
    for index, color in enumerate("WUBRG"):
        if color not in creature_mv.keys():
            raise DesignSkeletonConfigError(f"[common] expected {color} common creature MV list")
        if len(creature_mv[color]) != creature_counts[index]:
            raise DesignSkeletonConfigError(f"[common] {color} creature count expected to be {creature_counts[index]} but was {len(creature_mv[color])}")
    for keyword, counts in keywords.items():
        if len(counts) != 5:
            raise DesignSkeletonConfigError(f"[common] {keyword} has {len(counts)} entries")


if __name__ == '__main__':
    _validate_commons_data(_COMMON_CREATURE_COUNTS, _COMMON_KEYWORDS, _COMMON_CREATURE_MV)
