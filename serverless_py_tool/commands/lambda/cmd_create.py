import os
import json

import click

from serverless_py_tool.services.lambdas.create_service.create import run


@click.command(help="Create Lambda function")
@click.argument("names", nargs=-1, type=str, required=True)
@click.option(
    "-c", "--config-file", "config_file",
    default=".spt-config.json", help="Path to the configuration file."
)
def command(names, config_file):
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        click.echo(click.style("[ERROR] Config file not found. Use 'spt init' to create one or use 'spt -c <config_file>' to use specific config file."))
        raise click.Abort()

    if not config.get("lambda_layers_base_directory"):
        click.echo(click.style("[ERROR] 'lambda_layers_base_directory' parameter don't exist in config file.", fg="red"))
        raise click.Abort()

    for name in names:
        run(
            python_runtime = config.get("python_runtime"),
            lambda_name = name,
            lambda_prefix = config.get("lambda_prefix", ""),
            lambda_suffix = config.get("lambda_suffix", ""),
            lambda_package = config.get("lambda_filename"),
            lambda_handler = config.get("lambda_handler"),
            build_strategy = config.get("lambda_build_strategy"),
            lambda_base_path = config.get("lambda_base_directory")
        )