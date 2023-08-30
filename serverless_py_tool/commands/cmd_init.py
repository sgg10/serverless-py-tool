from typing import List, Optional

import click

from serverless_py_tool.services.create_project import run
from serverless_py_tool.utils.enums import (
    BuildStrategies,
    IaCTechnologies,
    PyVenvManager,
    PythonRuntime
)

venv_opts = [opt.value for opt in PyVenvManager]
build_opts = [opt.value for opt in BuildStrategies]
iac_opts = [opt.value for opt in IaCTechnologies]
runtimes_opts = [opt.value for opt in PythonRuntime]


def prompt_for_choice_if_none(
    value: Optional[str],
    prompt_text: str,
    choices: List[str],
    default_choice: Optional[str],
    confirm: bool = True
) -> str:
    """Prompt the user for a choice if the value is None.

    Parameters:
        - value: The current value of the option.
        - prompt_text: The text to display in the prompt.
        - choices: A list of valid choices.
        - default_choice: The default choice.
        - confirm: Whether to confirm before prompting.

    Returns:
        - The chosen value.
    """
    if not value:
        if not confirm or click.confirm(f"Do you want to select {prompt_text}?"):
            return click.prompt(
                f"Select your {prompt_text}: ",
                type=click.Choice(choices, case_sensitive=True),
                default=default_choice
            )
    return value

@click.command(help="This command initializes a new project with the given parameters.")
@click.option(
    "--py-venv-manager",
    type=click.Choice(venv_opts),
    default=None,
    required=False,
    help="Python virtual environment manager to use."
)
@click.option(
    "--python-runtime",
    type = click.Choice(runtimes_opts),
    default = None,
    required = False,
    help = "Python runtime for lambda creation"
)
@click.option("--aws-region", prompt=True, default="", help="AWS region for deployment.")
@click.option("--lambda-base-directory", default="lambdas", prompt=True, help="Base directory for Lambda functions.")
@click.option("--lambda-prefix", prompt=True, default="", help="Prefix for Lambda function names.")
@click.option("--lambda-suffix", prompt=True, default="", help="Suffix for Lambda function names.")
@click.option("--lambda-filename", prompt=True, default="handler", help="File name for each Lambda to be created")
@click.option("--lambda-handler", prompt=True, default="lambda_handler", help="Handler for each Lambda to be created")
@click.option(
    "--lambda-build-strategy",
    type=click.Choice(build_opts),
    default=None,
    required=False,
    help="Build strategy for Lambda functions."
)
@click.option("--lambda-layers-base-directory", default="common", prompt=True, help="Base directory for Lambda layers.")
@click.option("--lambda-layers-prefix", prompt=True, default="", help="Prefix for Lambda layer names.")
@click.option("--lambda-layers-suffix", prompt=True, default="", help="Suffix for Lambda layer names.")
@click.option(
    "--iac-technology",
    type=click.Choice(iac_opts),
    default=None,
    required=False,
    help="Infrastructure as Code technology to use."
)
@click.option("--config-filename", default=".spt-config.json", help="SPT config file name")
def command(
    py_venv_manager: Optional[str],
    python_runtime: Optional[str],
    aws_region: Optional[str],
    lambda_base_directory: str,
    lambda_prefix: Optional[str],
    lambda_suffix: Optional[str],
    lambda_filename: Optional[str],
    lambda_handler: Optional[str],
    lambda_build_strategy: Optional[str],
    lambda_layers_base_directory: str,
    lambda_layers_prefix: Optional[str],
    lambda_layers_suffix: Optional[str],
    iac_technology: Optional[str],
    config_filename: str
):
    py_venv_manager = prompt_for_choice_if_none(
        py_venv_manager,
        "venv manager",
        venv_opts,
        PyVenvManager.VENV.value
    )

    python_runtime = prompt_for_choice_if_none(
        python_runtime,
        "python runtime",
        runtimes_opts,
        PythonRuntime.PY39.value,
        False
    )

    lambda_build_strategy = prompt_for_choice_if_none(
        lambda_build_strategy,
        "build strategy",
        build_opts,
        BuildStrategies.REFERENCE.value,
        False
    )

    iac_technology = prompt_for_choice_if_none(
        iac_technology,
        "IaC technology",
        iac_opts,
        ""
    )

    run(
        py_venv_manager=py_venv_manager,
        python_runtime=python_runtime,
        aws_region=aws_region,
        lambda_base_directory=lambda_base_directory,
        lambda_prefix=lambda_prefix,
        lambda_suffix=lambda_suffix,
        lambda_filename=lambda_filename,
        lambda_handler=lambda_handler,
        lambda_build_strategy=lambda_build_strategy,
        lambda_layers_base_directory=lambda_layers_base_directory,
        lambda_layers_prefix=lambda_layers_prefix,
        lambda_layers_suffix=lambda_layers_suffix,
        iac_technology=iac_technology,
        config_filename=config_filename
    )
