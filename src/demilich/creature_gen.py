from dataclasses import dataclass
from random import uniform, sample, choice

from demilich.data import FLYING_RACES, ADJECTIVES


@dataclass
class Creature:
    name: str
    typeline: str
    text: str


def creatures(mana_values, races, classes, keywords):
    musts, maybes = _compute_keywords(keywords)

    keywords_batch = _generate_keywords(mana_values, musts, maybes)
    types_batch = _generate_typelines(keywords_batch, races, classes)
    names_batch = _generate_names(types_batch, ADJECTIVES)
    
    for kw_text, types, name in zip(keywords_batch, types_batch, names_batch, strict=True):
        yield Creature(
            name=f"{name[0]} {name[1]}",
            typeline=" ".join(["Creature", "—", "{0} {1}".format(types[0], types[1]).strip()]),
            text=", ".join(kw_text),
        )


def _generate_names(types_batch, adjectives):
    options = [
        choice([0, 1]) if t[1] is not "" else 0
        for t in types_batch
    ]
    names = [
        (choice(adjectives), t[o])
        for t, o in zip(types_batch, options)
    ]
    return names


def _choose_race(races, keywords):
    if 'flying' in keywords:
        return choice(list(races & FLYING_RACES))
    # awkwardly hardcode Bird as an obligate flyer
    return choice(list(races - {'Bird'}))


def _generate_typelines(keywords_batch, races, classes):
    races_set = set(races)
    races_batch = [
        _choose_race(races_set, kw)
        for kw in keywords_batch
    ]
    classes_batch = [
        choice(classes) if uniform(0.0, 1.0) < .75 else ""
        for _ in keywords_batch
    ]
    types_batch = [
        (race, class_)
        for race, class_ in zip(races_batch, classes_batch)
    ]
    return types_batch


def _generate_keywords(mana_values, musts, maybes):
    keywords_batch = [[] for _ in mana_values]
    must_targets = sample(keywords_batch, len(musts))
    for target in must_targets:
        keyword = musts.pop()
        target.append(keyword)
    
    selected_maybes = [
        m[0] for m in maybes if uniform(0.0, 1.0) < m[1]
    ]
    maybe_targets = sample(keywords_batch, len(selected_maybes))
    for target in maybe_targets:
        # note: this could assign incompatible keywords (trample +
        # deathtouch), or non-optimal placement (trample on a 1/1).
        # since we're only generating a starter skeleton, we'll live
        # with that for now.
        keyword = selected_maybes.pop()
        # however, we do want to avoid doubling keywords
        if keyword not in target:
            target.append(keyword)
    return keywords_batch


def _compute_keywords(keywords):
    musts = []
    maybes = []
    for keyword, quantity in keywords.items():
        while quantity >= 1:
            musts.append(keyword)
            quantity -= 1
        if quantity > 0:
            maybes.append((keyword, quantity))
    return musts, maybes