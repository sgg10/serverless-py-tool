import os
import json

import click

from serverless_py_tool.services.layer.create_module import run


@click.command(help="Create module for Lambda layer")
@click.argument("modules", nargs=-1, type=str, required=True)
@click.option("-l", "--layer", "layer", required=False, default=None)
@click.option(
    "-c", "--config-file", "config_file",
    default=".spt-config.json", help="Path to the configuration file."
)
def command(modules, layer, config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        click.echo(click.style("[ERROR] Config file not found. Use 'spt init' to create one or use 'spt -c <config_file>' to use specific config file."))
        raise click.Abort()

    if not config.get("lambda_layers_base_directory"):
        click.echo(click.style("[ERROR] 'lambda_layers_base_directory' parameter don't exist in config file.", fg="red"))
        raise click.Abort()

    layers = [
        layer
        for layer in os.listdir(config.get("lambda_layers_base_directory"))
        if os.path.isdir(os.path.join(config.get("lambda_layers_base_directory"), layer))
        and not layer.startswith("__") and not layer.endswith("__")
    ]

    if layer:
        if layer not in layers:
            click.echo(click.style(f"[ERROR] '{layer}' don't exist.", fg="red"))
            raise click.Abort()
    else:
        layer = click.prompt(
            "Select Lambda layer: ",
            type=click.Choice(choices=layers, case_sensitive=True)
        )

    for module in modules:
        if module not in os.listdir(os.path.join(config.get("lambda_layers_base_directory"), layer, "python")):
            run(module, os.path.join(config.get("lambda_layers_base_directory"), layer))
        else:
            click.echo(click.style(f"[WARNING] '{module}' module already exists.", fg="yellow"))