from dataclasses import dataclass
from random import uniform, sample, choice, choices

from demilich.data import ADJECTIVES, KEYWORD_BOOSTS
from demilich.restrictions import Restriction


@dataclass
class Creature:
    name: list[str]
    type_: list[str]
    subtype: list[str]
    text: list[str]
    stats: str


def creature_generator(
        mana_values: list,
        sizes: list,
        keywords: dict,
        races: dict,
        classes: dict,
        restrictions: dict[str,list],
    ):
    if len(mana_values) == 0 or len(sizes) == 0:
        return

    musts, maybes = _compute_keywords(keywords)
    keywords_batch = _generate_keywords(mana_values, musts, maybes)

    types_batch = _generate_types(keywords_batch, races, classes, restrictions)
    names_batch = _generate_names(types_batch, ADJECTIVES)
    stats_batch = _generate_stats(keywords_batch, sizes)
    
    for kw_text, types, name, stats in zip(keywords_batch, types_batch, names_batch, stats_batch, strict=True):
        yield Creature(
            name=name,
            type_=('Creature',),
            subtype=types,
            text=kw_text,
            stats=f"{stats[0]}/{stats[1]}"
        )


def _pick_stats(keywords, default_size):
    size = list(default_size)
    for keyword in keywords:
        if keyword in KEYWORD_BOOSTS:
            size[0] = max(0, size[0] + KEYWORD_BOOSTS[keyword][0])
            size[1] = max(1, size[1] + KEYWORD_BOOSTS[keyword][1])
    return tuple(size)


def _generate_stats(keywords_batch, sizes):
    stats_batch = [
        _pick_stats(keywords, default_size)
        for keywords, default_size in zip(keywords_batch, sizes)
    ]
    return stats_batch


def _generate_names(types_batch, adjectives):
    options = [
        choice([x for x in t if x != ""])
        for t in types_batch
    ]
    names = [
        (choice(adjectives), o)
        for t, o in zip(types_batch, options)
    ]
    return names


def _generate_types(keywords_batch, races: dict, classes: dict, restrictions: dict[str,list[Restriction]]):
    races_batch = [(r,) for r in choices(list(races.keys()), weights=list(races.values()), k=len(keywords_batch))]

    # handle keyword restrictions
    for index in range(len(keywords_batch)):
        for keyword, rstrs in restrictions['keyword'].items():
            if keyword in keywords_batch[index]:
                for restriction in rstrs:
                    if not restriction.passes(races_batch[index]):
                        # print(f"** {index=} violated KEYWORD restriction: {keywords_batch[index]=} {races_batch[index]=}")
                        races_batch[index] = restriction.fix(races_batch[index])
                        # print(f"-- fixed: {keywords_batch[index]=} {races_batch[index]=}")
        for race, rstrs in restrictions['race'].items():
            if race in races_batch[index]:
                for restriction in rstrs:
                    if not restriction.passes(keywords_batch[index]):
                        # print(f"** {index=} violated RACE restriction: {keywords_batch[index]=} {races_batch[index]=}")
                        keywords_batch[index] = restriction.fix(keywords_batch[index])
                        # print(f"-- fixed: {keywords_batch[index]=} {races_batch[index]=}")

    # TODO: sometimes, don't generate a class
    classes_batch = choices(list(classes.keys()), weights=list(classes.values()), k=len(keywords_batch))
    types_batch = [
        (*race, class_)
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