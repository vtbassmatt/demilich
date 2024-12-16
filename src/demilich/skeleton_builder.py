from dataclasses import dataclass

from demilich.data import COMMON


@dataclass
class Slot:
    rarity: str
    color: str
    number: int
    instruction: str

    @property
    def name(self) -> str:
        return f"{self.rarity}{self.color}{self.number:02}"


if __name__ == '__main__':
    for color in "WUBRG":
        for index, mv in enumerate(COMMON[color].creature_mana_values):
            slot = Slot('C', color, index+1, str(mv) if mv == int(mv) else f"{int(mv-.5)} or {int(mv+.5)}")
            print(f"{slot.name}. {slot.instruction}")

        spell_index = index + 2
        for index, spell in enumerate(COMMON[color].spells):
            slot = Slot('C', color, index+spell_index, spell)
            print(f"{slot.name}. {slot.instruction}")
