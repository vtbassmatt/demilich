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

## Advanced use

`TODO`: Eventually, this will sprout an ability to read skeleton definitions from custom TOML files.
(For now, you can hack up `data/pb2024.toml` if you want.)

`TODO`: Also eventually, the API for `SkeletonGenerator` will be documented so you can generate skeletons programmatically.
For now, see the examples in `examples/` for how to do it.
