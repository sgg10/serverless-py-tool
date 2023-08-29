from pathlib import Path

import click

def run(module_name: str, layer_path: str):
    base_path: Path = Path(layer_path).joinpath("python").resolve()
    module_path = base_path.joinpath(f"{module_name}").resolve()

    if module_path.exists():
        click.echo(click.style(f"[WARNING] '{module_path}' already exists!", fg="yellow"))
        raise click.Abort()

    module_path.mkdir(parents=True)

    init_file = module_path.joinpath("__init__.py").resolve()

    init_file.touch(mode=0o776)

    click.echo(click.style(f"[CREATED] '{module_name}' was created!", fg="green"))
