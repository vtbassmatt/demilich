import csv
from dataclasses import dataclass, asdict, field
import sys

from demilich.data import COMMON
from demilich.creature_gen import creatures


@dataclass
class Slot:
    rarity: str
    color: str
    number: int
    instruction: str
    id: str = field(init=False)
    name: str = ''
    typeline: str = ''
    text: str = ''

    def __post_init__(self):
        self.id = f"{self.rarity}{self.color}{self.number:02}"


if __name__ == '__main__':
    fieldnames = ['id', 'instruction', 'typeline', 'text']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for color in "WUBRG":
        c = creatures(
            COMMON[color].creature_mana_values,
            COMMON[color].creature_races,
            COMMON[color].creature_classes,
            COMMON[color].keywords,
        )
        for index, mv in enumerate(COMMON[color].creature_mana_values):
            card = next(c)
            slot = Slot(
                rarity='C', color=color, number=index+1,
                instruction=f'{mv} MV' if mv == int(mv) else f"{int(mv-.5)} or {int(mv+.5)} MV",
                name=card.name,
                typeline=card.typeline,
                text=card.text,
            )
            writer.writerow(asdict(slot))

        # spell_index = index + 2
        # for index, spell in enumerate(COMMON[color].spells):
        #     slot = Slot('C', color, index+spell_index, spell)
        #     writer.writerow(asdict(slot))
