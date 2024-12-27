import csv
from dataclasses import asdict
import sys

from demilich.bag.slot_maker import SlotMaker


if __name__ == "__main__":
    fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for slot in SlotMaker('C', 'W', 11, 4):
        writer.writerow(asdict(slot))
