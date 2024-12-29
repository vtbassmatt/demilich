# Demilich - the MTG skeleton wizard

A tool for quickly scaffolding a custom MTG set.

## Installation

```shell
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
You can ask for a pretty-printed table by adding "table" to your command.

```shell
% demilich play-booster table
# or
% demilich custom-skeleton my-custom-skeleton.toml table
```

## Suppressing or including big columns

CSV mode includes all columns by default.

Table mode suppresses the "instruction" column by default.
You can bring it back with `--include-instruction`.
(You'll want a pretty wide terminal for this to make sense.)

```shell
% demilich play-booster table --include-instruction
```

You can additionally suppress card text with `--no-include-text`:

```shell
% demilich play-booster table --no-include-text
```

## Programmatically building a skeleton

The API for `SkeletonGenerator` is documented in docstrings so you can generate skeletons programmatically.
See the examples in `examples/` for ideas on how to do it.

Each `SkeletonGenerator` is only responsible for a single section of a full skeleton.
It keeps a fixed rarity and frame code, which simplifies the implementation quite a bit.
If you need something much fancier, like redistribution keywords that didn't make it into one rarity into another rarity, you can probably achieve that using the programmatic interface.
