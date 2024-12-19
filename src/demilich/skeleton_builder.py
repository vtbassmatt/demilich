import csv
from dataclasses import dataclass, asdict, field
from itertools import cycle
from math import ceil
from random import choice, uniform
import sys

from demilich.data import (
    COMMON, UNCOMMON, UNCOMMON_MULTICOLOR,
    COMMON_ARTIFACT, UNCOMMON_ARTIFACT, UNCOMMON_LANDS,
    ARTIFACT_RACES, ARTIFACT_NONRACES, RARE_COLORED,
    RARE_ARTIFACTS, MYTHIC_COUNT,
)
from demilich.creature_gen import creatures


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


def _generate_commons(writer, color):
    commons = creatures(
            COMMON[color].creature_mana_values,
            COMMON[color].creature_races,
            COMMON[color].creature_classes,
            COMMON[color].keywords,
            COMMON[color].creature_sizes,
        )
    for index, mv in enumerate(COMMON[color].creature_mana_values):
        card = next(commons)
        slot = Slot(
                rarity='C', color=color, number=index+1,
                instruction=f'{mv} MV' if mv == int(mv) else f"{int(mv-.5)} or {int(mv+.5)} MV",
                name=card.name,
                cost=f"{{{mv-1}}}{{{color}}}" if int(mv) == mv else f"{{{int(mv+choice([-1.5, -.5]))}}}{{{color}}}",
                typeline=card.typeline,
                text=card.text,
                stats=card.stats,
            )
        writer.writerow(asdict(slot))

    spell_index = index + 2
    for index, spell in enumerate(COMMON[color].spells):
        slot = Slot(
                rarity='C', color=color, number=index+spell_index,
                instruction=spell,
            )
        writer.writerow(asdict(slot))

def _generate_uncommons(writer, color):
    creature_remainder = UNCOMMON[color].creature_count - int(UNCOMMON[color].creature_count)
    extra_creature = 1 if uniform(0.0, 1.0) < creature_remainder else 0
    uncommon_creatures = int(UNCOMMON[color].creature_count) + extra_creature

    # we're not going to use the instructions or text, but
    # we'd like the generated names and typelines and we'll
    # generate something like a curve
    uncommons = creatures(
            range(uncommon_creatures),
            UNCOMMON[color].creature_races,
            UNCOMMON[color].creature_classes,
            {},
            ((ceil(x/2)+1, ceil(x/2)+1) for x in range(uncommon_creatures)),
        )

    for index in range(uncommon_creatures):
        card = next(uncommons)
        slot = Slot(
                rarity='U', color=color, number=index+1,
                instruction='Creature',
                name=card.name,
                typeline=card.typeline,
                stats=card.stats,
            )
        writer.writerow(asdict(slot))
        
    for index in range(UNCOMMON[color].total_slots - uncommon_creatures):
        slot = Slot(
                rarity='U', color=color, number=uncommon_creatures+index+1,
                instruction='Spell',
                typeline=choice(['Instant', 'Sorcery', 'Enchantment', 'Enchantment — Aura']),
            )
        writer.writerow(asdict(slot))


def _generate_gold_uncommons(writer):
    cards_per_pair = len(UNCOMMON_MULTICOLOR)
    for offset, (first, second) in enumerate(zip(cycle("WUBRG"), "UBRGWBRGWU")):
        # generate cards to use partial information from
        gold_uncommons = creatures(
            range(10 * cards_per_pair),
            UNCOMMON[first].creature_races + UNCOMMON[second].creature_races,
            UNCOMMON[first].creature_classes + UNCOMMON[second].creature_classes,
            {},
            ((2, 2) for _ in range(10 * cards_per_pair)),
        )

        for index, multicolor_instruction in enumerate(UNCOMMON_MULTICOLOR):
            card = next(gold_uncommons)
            slot = Slot(
                rarity='U', color='Z', number=(offset*cards_per_pair)+index+1,
                instruction=f'{first}{second} creature ({multicolor_instruction})',
                name=card.name,
                typeline=card.typeline,
                stats=card.stats,
                cost=f"{{{first}}}{{{second}}}",
            )
            writer.writerow(asdict(slot))


def _pick_artifact_typeline(is_creature):
    if is_creature:
        typeline = f"Artifact Creature — {choice(ARTIFACT_RACES)}"
    elif uniform(0.0, 1.0) < .33:
        typeline = f"Artifact — {choice(ARTIFACT_NONRACES)}"
    else:
        typeline = "Artifact"
    return typeline


def _generate_artifacts(writer):
    for index, (instruction, is_creature, mv) in enumerate(COMMON_ARTIFACT):
        typeline = _pick_artifact_typeline(is_creature)
        slot = Slot(
            rarity='C', color='A', number=index+1,
            instruction=instruction,
            typeline=typeline,
            cost=f"{{{mv}}}" if mv is not None else "",
        )
        writer.writerow(asdict(slot))
    for index, (instruction, is_creature, mv) in enumerate(UNCOMMON_ARTIFACT):
        typeline = _pick_artifact_typeline(is_creature)
        slot = Slot(
            rarity='U', color='A', number=index+1,
            instruction=instruction,
            typeline=typeline,
            cost=f"{{{mv}}}" if mv is not None else "",
        )
        writer.writerow(asdict(slot))


def _generate_uncommon_lands(writer):
    for index in range(UNCOMMON_LANDS):
        slot = Slot(
            rarity='U', color='L', number=index+1,
            instruction='Utility land',
            typeline='Land',
        )
        writer.writerow(asdict(slot))


def _write_rare_mythic_slots(writer):
    slots = (
        ['W'] * RARE_COLORED +
        ['U'] * RARE_COLORED +
        ['B'] * RARE_COLORED +
        ['R'] * RARE_COLORED +
        ['G'] * RARE_COLORED +
        ['A'] * RARE_ARTIFACTS
    )
    for color in "WUBRG":
        for index in range(RARE_COLORED):
            slot = Slot(
                rarity='R', color=color, number=index+1,
                instruction='Rare',
            )
            writer.writerow(asdict(slot))
    for index in range(RARE_ARTIFACTS):
        slot = Slot(
            rarity='R', color='A', number=index+1,
            instruction='Rare artifact',
        )
        writer.writerow(asdict(slot))
    for index in range(MYTHIC_COUNT):
        slot = Slot(
            rarity='M', color='?', number=index+1,
            instruction='Mythic',
        )
        writer.writerow(asdict(slot))


if __name__ == '__main__':
    fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for color in "WUBRG":
        _generate_commons(writer, color)
        _generate_uncommons(writer, color)

    _generate_gold_uncommons(writer)
    _generate_artifacts(writer)
    _generate_uncommon_lands(writer)

    _write_rare_mythic_slots(writer)
