import os
import yaml
import shutil
from pathlib import Path

import click

from serverless_py_tool.utils.enums import IaCTechnologies
from serverless_py_tool.services.generators.sam import SAMGenerator
from serverless_py_tool.services.analyzer.layers import analyze_lambda_layers
from serverless_py_tool.services.analyzer.lambdas import analyze_lambda_fucntion

IAC_CONFIG = {
    IaCTechnologies.SAM.value: { "generator": SAMGenerator, "filetype": "yaml" },
}


def empty_directory(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.unlink(file_path)
            except Exception as e:
                continue

def run(
    lambdas_path: str,
    lambda_layers_path: str,
    iac_technology: str,
    python_runtime: str,
    lambda_packege: str,
    lambda_handler: str
):
    layers = analyze_lambda_layers(lambda_layers_path)
    lambdas = analyze_lambda_fucntion(lambdas_path, layers)

    if not IAC_CONFIG.get(iac_technology):
        click.echo(click.style(f"Unsupported '{iac_technology}' IaC option", "yellow"))
        raise click.Abort()

    filetype = IAC_CONFIG[iac_technology]["filetype"]
    generator = IAC_CONFIG[iac_technology]["generator"](python_runtime, lambda_packege, lambda_handler)

    # Register Lambda Layers
    for layer, content in layers.items():
        generator.add_layer(layer, content["path"])

    # Register Lambda Fucnstions
    for lambda_name, content in lambdas.items():
        generator.add_lambda(lambda_name, content["path"], content["envs"], content["layers"])

    content_file = generator.get_content()
    output_file_path = Path("./spt-build").resolve()
    output_file_path.mkdir(parents=True, exist_ok=True)
    output_file = output_file_path.joinpath(f"template.{filetype}")
    empty_directory(str(output_file_path))
    output_file.touch(0o666)

    with output_file.open("w") as f:
        if filetype == "yaml":
            yaml.dump(content_file, f, default_flow_style=False)

    click.echo(click.style(f"[COMPLETED] Go to {output_file_path.name} to see output result!", fg="green"))
