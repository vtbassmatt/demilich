from enum import Enum

import typer
from typing_extensions import Annotated


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
        import csv
        from dataclasses import asdict
        import sys

        fieldnames = ['id', 'instruction', 'name', 'cost', 'typeline', 'text', 'stats']
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for slot in pb2024():
            writer.writerow(asdict(slot))

    elif format == OutputFormat.table:
        from dataclasses import asdict
        from rich.console import Console
        from rich.table import Table

        fieldnames = ['name', 'cost', 'typeline', 'stats', 'text']
        table = Table(title="Play Booster skeleton")
        table.add_column("id", no_wrap=True)
        for col in fieldnames:
            table.add_column(col)
        
        for slot in pb2024():
            data = asdict(slot)
            table.add_row(data['id'], *[data[key] for key in fieldnames])
        
        console = Console()
        console.print(table)

    else:
        raise NotImplementedError(format)


@app.command()
def dev():
    """
    Generate a partial skeleton, exercising a few features.
    """
    from demilich.examples.dev import dev_skeleton
    dev_skeleton()
