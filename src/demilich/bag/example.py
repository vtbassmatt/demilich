import csv
from dataclasses import asdict
import sys

from demilich.bag.slot_maker import SlotMaker


if __name__ == "__main__":
    fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    common_white = SlotMaker('C', 'W', 11, 4)
    common_white.keywords(
        flying=3, vigilance=2, lifelink=1,
        first_strike=.25, double_strike=.2,
    )
    common_white.mana_values(1, 2, 2, 2, 3, 3, 3, 4, 4, (5, 6), (6, 7))
    for slot in common_white:
        writer.writerow(asdict(slot))

    # make sure degenerate cases keep working
    common_blue = SlotMaker('C', 'U', 1, 1)
    for slot in common_blue:
        writer.writerow(asdict(slot))
    common_black = SlotMaker('C', 'B', 1, 1)
    common_black.keywords(flying=2)
    for slot in common_black:
        writer.writerow(asdict(slot))
    common_red = SlotMaker('C', 'R', 0, 1)
    for slot in common_red:
        writer.writerow(asdict(slot))
    common_green = SlotMaker('C', 'G', 1, 0)
    common_green.mana_values(5)
    for slot in common_green:
        writer.writerow(asdict(slot))
