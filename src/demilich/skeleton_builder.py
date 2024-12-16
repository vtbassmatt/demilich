import csv
from dataclasses import dataclass, asdict, field
import sys

from demilich.data import COMMON


@dataclass
class Slot:
    rarity: str
    color: str
    number: int
    instruction: str
    id: str = field(init=False)

    def __post_init__(self):
        self.id = f"{self.rarity}{self.color}{self.number:02}"


if __name__ == '__main__':
    fieldnames = ['id', 'instruction']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for color in "WUBRG":
        for index, mv in enumerate(COMMON[color].creature_mana_values):
            slot = Slot('C', color, index+1, f'{mv} MV' if mv == int(mv) else f"{int(mv-.5)} or {int(mv+.5)} MV")
            writer.writerow(asdict(slot))

        spell_index = index + 2
        for index, spell in enumerate(COMMON[color].spells):
            slot = Slot('C', color, index+spell_index, spell)
            writer.writerow(asdict(slot))
