import typer


app = typer.Typer(no_args_is_help=True)


@app.command()
def play_booster():
    """
    Generate a standard play booster skeleton.
    """
    from demilich.examples.play_booster_2024 import pb2024
    pb2024()


@app.command()
def dev():
    """
    Generate a partial skeleton, exercising a few features.
    """
    from demilich.examples.dev import dev_skeleton
    dev_skeleton()
