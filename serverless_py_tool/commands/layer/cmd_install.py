import json

import click

from serverless_py_tool.services.layer.install_layers import run


@click.command(help="Install modules from Lambda layers to the site-packages directory.")
@click.option(
    "-c", "--config-file", "config_file",
    default=".spt-config.json", help="Path to the configuration file."
)
def command(config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        click.echo(click.style("[ERROR] Config file not found. Use 'spt init' to create one or use 'spt -c <config_file>' to use specific config file."))
        raise click.Abort()

    if not config.get("lambda_layers_base_directory"):
        click.echo(click.style("[ERROR] 'lambda_layers_base_directory' parameter don't exist in config file."))
        raise click.Abort()

    run(config.get("lambda_layers_base_directory"))
