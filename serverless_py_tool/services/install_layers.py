import os
import sys
from shutil import copytree, rmtree
from typing import Dict, List

import click

def get_site_packages_path() -> str:
    """
    Get the path to the 'site-packages' directory of the current Python environment.

    Returns:
        str: Path to the 'site-packages' directory.
    """
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return os.path.join(sys.prefix, 'lib', f'python{version}', 'site-packages')


def cp_layer(src: str, dest: str, layer_name: str, module_name: str) -> None:
    """
    Copy a module from a Lambda layer to the site-packages directory.

    Args:
        src (str): Source path of the module in the Lambda layer.
        dest (str): Destination path in the site-packages directory.
        layer_name (str): Name of the Lambda layer.
        module_name (str): Name of the module.

    """
    try:
        if os.path.exists(dest):
            rmtree(dest)

        copytree(src, dest)
        click.echo(click.style(f"[INSTALLED] '{module_name}' module from '{layer_name}' layer", fg="green"))
    except Exception as e:
        click.echo(click.style(f"[ERROR] Failed to copy '{module_name}' module from '{layer_name}' layer: {e}", fg="red"))


def run(lambda_layers_base_path: str) -> None:
    """
    Install modules from Lambda layers to the site-packages directory.

    Args:
        lambda_layers_base_path (str): Base path where Lambda layers are stored.
    """
    dest = get_site_packages_path()

    layers = {
        layer: [module for module in os.listdir(os.path.join(lambda_layers_base_path, layer, "python"))]
        for layer in os.listdir(lambda_layers_base_path)
        if os.path.isdir(os.path.join(lambda_layers_base_path, layer))
        and not layer.startswith("__") and not layer.endswith("__")
    }

    for layer, modules in layers.items():
        for module in modules:
            cp_layer(
                os.path.join(lambda_layers_base_path, layer, "python", module),
                os.path.join(dest, module),
                layer,
                module
            )
