from io import BufferedReader
import tomllib

from demilich.slot_maker import SlotMaker, Reprint


def load_from_resources(filename: str):
    from importlib import resources
    from demilich import data
    
    full_filename = resources.files(data) / filename
    return load_from_file(full_filename)


def load_from_file(filename: str):
    with open(filename, 'rb') as f:
        return load_from_stream(f)


def load_from_stream(stream: BufferedReader):
    data = tomllib.load(stream)
    return data


FRAMES = [
    ('W', 'white'),
    ('U', 'blue'),
    ('B', 'black'),
    ('R', 'red'),
    ('G', 'green'),
    ('Z', 'multicolor'),
    ('A', 'artifact'),
]

RARITIES = [
    ('C', 'common'),
    ('U', 'uncommon'),
    ('R', 'rare'),
    ('M', 'mythic'),
]


def _configure_slots(data: dict, slot_maker: SlotMaker):
    for key in ['keywords', 'races', 'classes']:
        if key in data:
            method = slot_maker.__getattribute__(key)
            method(**data[key])

    if 'creature_slots' in data:
        mv, power, toughness = zip(
            *[(x['mv'], x['power'], x['toughness'])
              for x in data['creature_slots']]
        )
        slot_maker.mana_values(*mv)
        slot_maker.powers(*power)
        slot_maker.toughnesses(*toughness)
    
    if 'spell_slots' in data:
        for spell in data['spell_slots']:
            options = [Reprint(**x) for x in spell.get('options', [])]
            slot_maker.add_spell(spell.get('instruction', ''), *options)


def generate_skeleton(data: dict):
    for frame_code, frame_name in FRAMES:
        if frame_name not in data:
            continue

        frame_data = data[frame_name]
        for rarity_code, rarity_name in RARITIES:
            if rarity_name not in frame_data:
                continue

            f_r_data = frame_data[rarity_name]
            creature_count = f_r_data['creatures']
            spell_count = f_r_data['spells']
            slot_maker = SlotMaker(rarity_code, frame_code, creature_count, spell_count)
            _configure_slots(f_r_data, slot_maker)
            yield from slot_maker


if __name__ == '__main__':
    print(load_from_resources('pb2024.toml'))
