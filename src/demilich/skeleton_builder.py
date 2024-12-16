from demilich.data import COMMON


for color in "WUBRG":
    for index, mv in enumerate(COMMON[color].creature_mana_values):
        slot = f"C{color}{index+1:02}"
        if mv == int(mv):
            print(f"{slot}. {mv}")
        else:
            mv_range = f"{int(mv-.5)} or {int(mv+.5)}"
            print(f"{slot}. {mv_range}")
    spell_index = index + 1
    for index, spell in enumerate(COMMON[color].spells):
        slot = f"C{color}{index+spell_index+1:02}"
        print(f"{slot}. {spell}")