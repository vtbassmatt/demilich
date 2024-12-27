import csv
from dataclasses import asdict
import sys

from demilich.bag.slot_maker import SlotMaker, Reprint


if __name__ == "__main__":
    fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    common_white = SlotMaker('C', 'W', 11, 4)
    common_white.keywords(
        flying=3, vigilance=2, lifelink=1,
        first_strike=.25, double_strike=.2,
    )
    common_white.mana_values(
        1, 2, 2, 2, 3, 3,
        3, 4, 4, (5, 6), (6, 7)
    )
    common_white.powers(
        (1, 2), 2, (1, 2, 3), 2, (2, 3), (2, 3),
        3, (3, 4), 4, (4, 5), (4, 5, 6)
    )
    common_white.toughnesses(
        1, 1, (1, 2), (2, 3), 3, 3,
        3, (3, 4), 4, (4, 5), (4, 5)
    )
    common_white.races(
        human=20, bird=5, spirit=5, cat=5, kithkin=2, unicorn=1,
        dog=1, dinosaur=1, avatar=1, loxodon=1, giant=1, nothing=1,
    )
    common_white.classes(
        nothing=2, scout=4, knight=4, soldier=4, monk=2, cleric=2,
        nomad=1, mystic=1, samurai=1,
    )
    common_white.add_spell("Combat-related removal")
    common_white.add_spell(
        "Banishing Light",
        Reprint("Banishing Light", "{2}{W}", "Enchantment", None, "When this enchantment enters, exile target nonland permanent an opponent controls until this enchantment leaves the battlefield."),
        Reprint("Journey to Nowhere", "{1}{W}", "Enchantment", None, "When Journey to Nowhere enters, exile target creature. // When Journey to Nowhere leaves the battlefield, return the exiled card to the battlefield under its owner's control."),
        Reprint("Oblivion Ring", "{2}{W}", "Enchantment", None, "When Oblivion Ring enters, exile another target nonland permanent. //  When Oblivion Ring leaves the battlefield, return the exiled card to the battlefield under its owner's control."),
        Reprint("Chains of Custody", "{2}{W}", "Enchantment", ["Aura"], "Enchant creature you control // When Chains of Custody enters, exile target nonland permanent an opponent controls until Chains of Custody leaves the battlefield. // Enchanted creature has ward {2}."),
    )
    common_white.add_spell("Combat trick")
    common_white.add_spell("Disenchant/removal")
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
    common_artifact = SlotMaker('C', 'A', 1, 1)
    common_artifact.mana_values(3)
    for slot in common_artifact:
        writer.writerow(asdict(slot))
