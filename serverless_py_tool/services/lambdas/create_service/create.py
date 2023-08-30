import os
from pathlib import Path
from string import Template

import click

from serverless_py_tool.utils.enums import BuildStrategies
from serverless_py_tool.services.lambdas.create_service.templates import (
    DOCKER_TEMPLATE,
    LAMBDA_FUNCTION_TEMPLATE
)


def create_docker_file(python_runtime: str, lambda_package: str, lambda_handler: str) -> str:
    return Template(DOCKER_TEMPLATE).substitute(
        python_runtime=python_runtime,
        lambda_package=lambda_package,
        lambda_handler=lambda_handler
    )

def create_lambda_function_file(lambda_handler: str):
    return Template(LAMBDA_FUNCTION_TEMPLATE).substitute(
        lambda_handler=lambda_handler
    )

def run(
    python_runtime: str,
    lambda_name: str,
    lambda_prefix: str,
    lambda_suffix: str,
    lambda_package: str,
    lambda_handler: str,
    build_strategy: str,
    lambda_base_path: str,
):
    base_path = Path(lambda_base_path).resolve()
    lambda_path = base_path.joinpath(f"{lambda_prefix}{lambda_name}{lambda_suffix}").resolve()

    if lambda_path.exists():
        click.echo(click.style(f"[ERROR] '{lambda_path.name}' lambda already exists!"))
        raise click.Abort()

    lambda_path.mkdir(parents=True)

    lambda_file = lambda_path.joinpath(f"{lambda_package}.py").resolve()
    lambda_file.touch(mode=0o776)
    with lambda_file.open("w") as f:
        f.write(create_lambda_function_file(lambda_handler))
        click.echo(click.style(f"[CREATED] {lambda_path.name}/{lambda_file.name} was created!", fg="green"))

    if build_strategy == BuildStrategies.DOCKER:
        docker_file = lambda_path.joinpath("Dockerfile").resolve()
        docker_file.touch(mode=0o776)
        with docker_file.open("w") as f:
            f.write(create_docker_file(python_runtime, lambda_package, lambda_handler))
            click.echo(click.style(f"[CREATED] {lambda_path.name}/{docker_file.name} was created!", fg="green"))

    if click.confirm("Do you need a 'requirements.txt' for this lambda function?", default=False):
        requirements_file = lambda_path.joinpath("requirements.txt").resolve()
        requirements_file.touch(mode=0o776)
        click.echo(click.style(f"[CREATED] {lambda_path.name}/{requirements_file.name} was created!", fg="green"))
