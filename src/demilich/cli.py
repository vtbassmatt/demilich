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
    include_instruction: Annotated[
        bool|None, typer.Option(help="Include skeleton instruction")
    ] = None,
    include_text: Annotated[
        bool|None, typer.Option(help="Include card text")
    ] = None,
):
    """
    Generate a standard play booster skeleton.
    """
    from demilich.examples.play_booster_2024 import pb2024

    all_fields = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
    fields = {field: True for field in all_fields}

    if format == OutputFormat.csv:
        fields['instruction'] = False if include_instruction is False else True
        fields['text'] = False if include_text is False else True
        write_csv(pb2024(), [key for key, value in fields.items() if value])

    elif format == OutputFormat.table:
        fields['instruction'] = True if include_instruction is True else False
        fields['text'] = False if include_text is False else True
        write_table(pb2024(), [key for key, value in fields.items() if value])

    else:
        raise NotImplementedError(format)


@app.command()
def dev():
    """
    Generate a partial skeleton, exercising a few features.
    """
    from demilich.examples.dev import dev_skeleton
    dev_skeleton()
