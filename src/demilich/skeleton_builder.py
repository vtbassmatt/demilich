from demilich.data import COMMON


for color in "WUBRG":
    for index, mv in enumerate(COMMON[color].mana_values):
        slot = f"C{color}{index+1:02}"
        if mv == int(mv):
            print(f"{slot}. {mv}")
        else:
            mv_range = f"{int(mv-.5)} or {int(mv+.5)}"
            print(f"{slot}. {mv_range}")
