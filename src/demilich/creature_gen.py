from dataclasses import dataclass
from random import uniform, sample


@dataclass
class Creature:
    name: str
    typeline: str
    text: str


def creatures(mana_values, types, keywords):
    musts, maybes = _compute_keywords(keywords)

    keywords_batch = _generate_keywords(mana_values, musts, maybes)
    
    for slot_keywords in keywords_batch:
        yield Creature(
            name='TODO',
            typeline='TODO',
            text=", ".join(slot_keywords),
        )


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