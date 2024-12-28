from enum import Enum

import typer
from typing_extensions import Annotated

from demilich.output import write_csv, write_table


class OutputFormat(str, Enum):
    csv = "csv"
    table = "table"


app = typer.Typer(no_args_is_help=True)


@app.command()
def play_booster(
    format: Annotated[
        OutputFormat, typer.Argument()
    ] = OutputFormat.csv,
):
    """
    Generate a standard play booster skeleton.
    """
    from demilich.examples.play_booster_2024 import pb2024
    if format == OutputFormat.csv:
        write_csv(pb2024(), ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats'])

    elif format == OutputFormat.table:
        write_table(pb2024(), ['id', 'name', 'cost', 'typeline', 'stats', 'text'])

    else:
        raise NotImplementedError(format)


@app.command()
def dev():
    """
    Generate a partial skeleton, exercising a few features.
    """
    from demilich.examples.dev import dev_skeleton
    dev_skeleton()
