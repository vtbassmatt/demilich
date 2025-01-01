# Demilich - the MTG skeleton wizard

A tool for quickly scaffolding a custom MTG set.

For designers of custom Magic: the Gathering sets, the designers of canon Magic suggest starting from a [design skeleton](https://magic.wizards.com/en/news/making-magic/nuts-and-bolts-16-play-boosters).
This is a set of "slots" which have some standard creatures, keywords, and spells to make the limited game work, at least at a base level.
I've found that the act of mechanically filling out a design skeleton (15 commons per color, 14 uncommons per color, plus artifacts and signposts) is draining.
In fact, I've never successfully completed a design skeleton by hand.

Enter `demilich`.
Demilich encodes the suggested distributions of things and generates a randomized set of initial slots.
This takes the drudgery and thinking out of the process and makes it a simple, mechanical starting point.
From there, you can start assigning your own mechanics and creative to your new set!

## Installation

The fastest way to simply generate a basic skeleton is to run `demilich` using `pipx`.
1. Install [`pipx`](https://pipx.pypa.io/latest/)
2. Run `demilich`: `pipx run demilich play-booster > skeleton.csv`

If you intend to use more of its features (like [generating a skeleton programmatically](#programmatically-building-a-skeleton)), you can also install the package.

```shell
# first make a virtualenv however you normally do
% python -m venv env
% . env/bin/activate
# then install demilich
% pip install demilich
```

## Basic use

```shell
% demilich play-booster > skeleton.csv
```

Then open `skeleton.csv` in the editor of your choice.

## Custom skeleton

You can use `demilich` with your custom skeleton definition.
I recommend you copy [pb2024.toml](src/demilich/data/pb2024.toml) to use as a starting point.
Once you have your `my-custom-skeleton.toml` ready to go, run:

```shell
% demilich custom-skeleton my-custom-skeleton.toml
```

## Output formats

By default, `demilich` generates a CSV.
You can ask for a pretty-printed table instead with the `--format` option.

```shell
% demilich play-booster --format=table
# or
% demilich custom-skeleton my-custom-skeleton.toml --format=table
```

## Choosing fields

CSV mode includes all fields by default.
Table mode omits the "instruction" field by default.
But you have full control about which fields appear and in what order.

```shell
% demilich play-booster --format=table --fields=id,name,stats,text
```

This will generate a 4-column output (regardless of format) which only includes ID, name, stats, and card text fields.

The valid fields are:
- `id`
- `instruction`
- `name`
- `cost`
- `typeline`
- `stats`
- `text`

## Limiting to certain chunks of the skeleton

By default, `demilich` will generate every skeleton chunk in the definition file.
But for a particular run, you may want to only generate a subset of rarities and/or a subset of frames.
There are options for this:

```shell
# produce only the white commons
% demilich play-booster --rarities C --frames W

# produce artifact uncommons and rares
% demilich play-booster --rarities UR --frames A

# produce blue and black rares
% demilich play-booster --rarities R --frames UB

# produce red and green commons and uncommons
% demilich play-booster --rarities CU --frames RG
```

When you specify both `--rarities` and `--frames`, you'll get output which includes every combination.
There isn't a way to ask for "blue commons and red uncommons"; just split that into two separate invocations (`demilich play-booster --rarities C --frames U` and `demilich play-booster --rarities U --frames R`).

## Programmatically building a skeleton

The API for `SkeletonGenerator` is documented in docstrings so you can generate skeletons programmatically.
See the examples in `examples/` for ideas on how to do it.

Each `SkeletonGenerator` is only responsible for a single section of a full skeleton.
It keeps a fixed rarity and frame code, which simplifies the implementation quite a bit.
If you need something much fancier, like redistributing keywords that didn't make it into one rarity into another rarity, you can probably achieve that using the programmatic interface.

## Fan content policy

`demilich` is unofficial Fan Content permitted under the [Fan Content Policy][fan-content].
Not approved/endorsed by Wizards.
Portions of the materials used are property of Wizards of the Coast.
©Wizards of the Coast LLC.

[fan-content]: https://company.wizards.com/en/legal/fancontentpolicy
