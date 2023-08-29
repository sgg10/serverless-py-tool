import json
from enum import Enum
from pathlib import Path
from typing import Optional

import click


class PyVenvManager(str, Enum):
    VENV = "venv"
    PIPENV = "pipenv"


class BuildStrategies(str, Enum):
    ZIP = "zip"
    DOCKER = "docker"
    REFERENCE = "reference"


class IaCTechnologies(str, Enum):
    SAM = "sam"
    CLOUDFORMATION = "cloudformation"
    TERRAFORM = "terraform"


def create_config_file(
    py_venv_manager: PyVenvManager = "venv",
    aws_region: Optional[str] = None,
    lambda_base_directory: Optional[str] = None,
    lambda_prefix: Optional[str] = None,
    lambda_suffix: Optional[str] = None,
    lambda_build_strategy: BuildStrategies = "reference",
    lambda_layers_base_directory: Optional[str] = None,
    lambda_layers_prefix: Optional[str] = None,
    lambda_layers_suffix: Optional[str] = None,
    iac_technology: Optional[IaCTechnologies] = None,
    config_filename: Optional[str] = ".spt-config.json"
):
    """
    Creates and saves a configuration file based on the provided parameters.

    This function generates a configuration file for serverless projects,
    allowing users to specify various settings related to their AWS Lambda
    functions and infrastructure as code (IaC) setup.

    Parameters:
        - py_venv_manager ({"venv", "pipenv"}): Specifies the Python virtual environment manager. Default is "venv".
        - aws_region (str, optional): AWS region to be used for the Lambda functions.
        - lambda_base_directory (str, optional): Base directory for Lambda functions.
        - lambda_prefix (str, optional): Prefix for Lambda function names.
        - lambda_suffix (str, optional): Suffix for Lambda function names.
        - lambda_build_strategy ({"zip", "docker", "reference"}): Strategy to build Lambda functions. Default is "reference".
        - lambda_layers_base_directory (str, optional): Base directory for Lambda layers.
        - lambda_layers_prefix (str, optional): Prefix for Lambda layer names.
        - lambda_layers_suffix (str, optional): Suffix for Lambda layer names.
        - iac_technology ({"sam", "cloudformation", "terraform"}, optional): Infrastructure as Code technology to be used.

    The function will create the specified directories if they don't exist.
    The resulting configuration is saved in a '.spt-config.json' file. If this file
    already exists, the user will be prompted to confirm overwriting it.

    Returns:
    None. The function provides feedback to the user via console messages and saves the configuration to a file.

    Raises:
        - PermissionError: If there's a permission issue when creating directories or writing to the file.
        - IsADirectoryError: If there's an issue related to directory paths.
        - json.JSONDecodeError: If there's an issue encoding the configuration to JSON.
    """
    config = {
        param: value
        for param, value in locals().items()
        if value
    }

    for directory in (lambda_base_directory, lambda_layers_base_directory):
        if not directory:
            continue

        path = Path(directory).resolve()

        try:
            if not path.exists():
                path.mkdir(parents=True)
        except (PermissionError, IsADirectoryError) as e:
            click.echo(click.style(f"Error creating directory {path}: {str(e)}", fg="red"))
            raise click.Abort()

    config_file = Path(config_filename)

    if config_file.exists():
        if not click.confirm(click.style(f"{config_file} already exists. Do you want to overwrite it?", fg="yellow")):
            click.echo(click.style("Configuration not saved. Exiting.", fg="yellow"))
            raise click.Abort()

    try:
        with config_file.open("w") as f:
            json.dump(config, f, indent=4)
    except (PermissionError, json.JSONDecodeError) as e:
        click.echo(click.style(f"Error writing to {config_file}: {str(e)}", fg="red"))
        raise click.Abort()

    click.echo(click.style("Configuration resume:", bg="green"))
    for param, key in config.items():
        click.echo(click.style(f"\t{param}={key}", fg="green"))
    click.echo(click.style(f"Saved on: {config_file}", fg="green"))
