import csv
from dataclasses import dataclass, asdict, field
from random import choice, uniform
import sys

from demilich.data import COMMON, UNCOMMON
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


if __name__ == '__main__':
    fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for color in "WUBRG":
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

        creature_remainder = UNCOMMON[color].creature_count - int(UNCOMMON[color].creature_count)
        extra_creature = 1 if uniform(0.0, 1.0) < creature_remainder else 0
        uncommon_creatures = int(UNCOMMON[color].creature_count) + extra_creature
        for index in range(uncommon_creatures):
            slot = Slot(
                rarity='U', color=color, number=index+1,
                instruction='Creature',
                typeline='Creature — TODO',
            )
            writer.writerow(asdict(slot))
        
        for index in range(UNCOMMON[color].total_slots - uncommon_creatures):
            slot = Slot(
                rarity='U', color=color, number=uncommon_creatures+index+1,
                instruction='Spell',
                typeline=choice(['Instant', 'Sorcery', 'Enchantment', 'Enchantment — Aura']),
            )
            writer.writerow(asdict(slot))
