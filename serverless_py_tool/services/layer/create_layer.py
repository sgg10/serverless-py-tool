from pathlib import Path

import click


def run(lambda_layer_name: str, base_path: str, prefix: str, suffix: str):
    base_path: Path = Path(base_path).resolve()
    layer_path = base_path.joinpath(f"{prefix}{lambda_layer_name}{suffix}", "python").resolve()

    if layer_path.exists():
        click.echo(click.style(f"[WARNING] '{prefix}{lambda_layer_name}{suffix}' already exists!", fg="yellow"))
        raise click.Abort()

    layer_path.mkdir(parents=True)
    click.echo(click.style(f"[CREATED] '{prefix}{lambda_layer_name}{suffix}' was created", fg="green"))
