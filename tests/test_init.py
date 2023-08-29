import os
import json

from click.testing import CliRunner

from serverless_py_tool.commands.cmd_init import command

config = {
    "py_venv_manager": "venv",
    "aws_region": "us-east-1",
    "lambda_base_directory": "lambdas",
    "lambda_prefix": "prefix",
    "lambda_suffix": "suffix",
    "lambda_build_strategy": "reference",
    "lambda_layers_base_directory": "common",
    "lambda_layers_prefix": "layer_prefix",
    "lambda_layers_suffix": "layer_suffix",
    "iac_technology": "terraform"
}


def test_init_command():
    runner = CliRunner()
    result = runner.invoke(
        command,
        [
            '--py-venv-manager', 'venv',
            '--aws-region', 'us-east-1',
            '--lambda-base-directory', 'lambdas',
            '--lambda-prefix', 'prefix',
            '--lambda-suffix', 'suffix',
            '--lambda-build-strategy', 'reference',
            '--lambda-layers-base-directory', 'common',
            '--lambda-layers-prefix', 'layer_prefix',
            '--lambda-layers-suffix', 'layer_suffix',
            '--iac-technology', 'terraform',
            '--config-filename', '.spt-config.test.json'
        ]
    )

    assert result.exit_code == 0
    with open(".spt-config.test.json", "r") as f:
        json_result = json.load(f)
    for key, value in config.items():
        assert json_result.get(key) == value
    os.remove(".spt-config.test.json")
