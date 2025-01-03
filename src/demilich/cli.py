from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from demilich.reader import (
    generate_skeleton,
    load_from_resources,
    load_from_file,
    FRAMES,
    RARITIES,
)
from demilich.output import write_csv, write_table


ALL_FIELDS = ['id', 'instruction', 'name', 'cost', 'typeline', 'stats', 'text']
FIELDS_HELP = f"Comma-separated fields to include in the output from among: {','.join(ALL_FIELDS)}"
FIELDS_METAVAR = "field_list"
RARITIES_HELP = "Which rarities to include in output (C, U, R, M)"
RARITIES_METAVAR = "rarities"
FRAMES_HELP = "Which frames to include in output (W, U, B, R, G, A, Z, L)"
FRAMES_METAVAR = "frames"

class OutputFormat(str, Enum):
    csv = "csv"
    table = "table"


app = typer.Typer(no_args_is_help=True)


@app.command()
def play_booster(
    format: Annotated[
        OutputFormat, typer.Option()
    ] = OutputFormat.csv,
    fields: Annotated[
        str, typer.Option(help=FIELDS_HELP, metavar=FIELDS_METAVAR)
    ] = "",
    rarities: Annotated[
        str, typer.Option(help=RARITIES_HELP, metavar=RARITIES_METAVAR)
    ] = "CURM",
    frames: Annotated[
        str, typer.Option(help=FRAMES_HELP, metavar=FRAMES_METAVAR)
    ] = "WUBRGAZL",
):
    """
    Generate a standard play booster skeleton.
    """
    data_loader = lambda: load_from_resources('pb2024.toml')
    _generate(data_loader, format, fields, rarities, frames)


@app.command()
def custom_skeleton(
    filename: Annotated[
        Path, typer.Argument()
    ],
    format: Annotated[
        OutputFormat, typer.Option()
    ] = OutputFormat.csv,
    fields: Annotated[
        str, typer.Option(help=FIELDS_HELP, metavar=FIELDS_METAVAR)
    ] = "",
    rarities: Annotated[
        str, typer.Option(help=RARITIES_HELP, metavar=RARITIES_METAVAR)
    ] = "CURM",
    frames: Annotated[
        str, typer.Option(help=FRAMES_HELP, metavar=FRAMES_METAVAR)
    ] = "WUBRGAZL",
):
    """
    Generate a skeleton from a TOML file.
    """
    data_loader = lambda: load_from_file(filename)
    _generate(data_loader, format, fields, rarities, frames)


def _clean_rarities_and_frames(rarities, frames):
    rarities = rarities.upper().replace(',', '')
    set_rarities = set([x[0] for x in RARITIES])
    for r in rarities:
        if r not in set_rarities:
            raise ValueError(f"unknown rarity {r} requested; "
                             f"valid options are {[x[0] for x in RARITIES]}")
    
    frames = frames.upper().replace(',', '')
    set_frames = set([x[0] for x in FRAMES])
    for f in frames:
        if f not in set_frames:
            raise ValueError(f"unknown frame {f} requested; "
                             f"valid options are {[x[0] for x in FRAMES]}")

    return rarities, frames


def _get_fields(field_str: str|None, format: OutputFormat):
    if not field_str:
        if format == OutputFormat.table:
            return [f for f in ALL_FIELDS if f != 'instruction']
        return ALL_FIELDS

    requested_fields = [f.lower() for f in field_str.split(',')]
    shown_fields = []
    for field in requested_fields:
        if field in ALL_FIELDS:
            shown_fields.append(field)
        else:
            raise ValueError(f"unknown field {field} requested; "
                             f"valid options are {ALL_FIELDS}")
    return shown_fields


def _generate(data_loader, format, fields, rarities, frames):
    rarities, frames = _clean_rarities_and_frames(rarities.upper(), frames.upper())
    fields = _get_fields(fields, format)
    data = data_loader()

    if format == OutputFormat.csv:
        write_csv(generate_skeleton(data, rarities, frames), fields)

    elif format == OutputFormat.table:
        write_table(generate_skeleton(data, rarities, frames), fields)

    else:
        raise NotImplementedError(format)


# Left for demonstration purposes - this exercises the example
# in examples/dev.py
# @app.command()
# def dev():
#     """
#     Generate a partial skeleton, exercising a few features.
#     """
#     from demilich.examples.dev import dev_skeleton
#     write_csv(dev_skeleton(), ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats'])
