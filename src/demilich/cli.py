from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated

from demilich.reader import (
    generate_skeleton,
    load_from_resources,
    load_from_file,
)
from demilich.output import write_csv, write_table


ALL_FIELDS = ['id', 'instruction', 'name', 'cost', 'typeline', 'stats', 'text']
FIELDS_HELP = f"Comma-separated fields to include in the output from among: {','.join(ALL_FIELDS)}"

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
        str, typer.Option(help=FIELDS_HELP, metavar="field_list")
    ] = "",
):
    """
    Generate a standard play booster skeleton.
    """
    fields = _get_fields(fields, format)
    data = load_from_resources('pb2024.toml')
    _generate(data, format, fields)


@app.command()
def custom_skeleton(
    filename: Annotated[
        Path, typer.Argument()
    ],
    format: Annotated[
        OutputFormat, typer.Option()
    ] = OutputFormat.csv,
    fields: Annotated[
        str, typer.Option(help=FIELDS_HELP, metavar="field_list")
    ] = "",
):
    """
    Generate a skeleton from a TOML file.
    """
    fields = _get_fields(fields, format)
    data = load_from_file(filename)
    _generate(data, format, fields)


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


def _generate(data, format, fields):
    if format == OutputFormat.csv:
        write_csv(generate_skeleton(data), fields)

    elif format == OutputFormat.table:
        write_table(generate_skeleton(data), fields)

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
