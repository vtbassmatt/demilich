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
    for slot in common_white:
        writer.writerow(asdict(slot))
