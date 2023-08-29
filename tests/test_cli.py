from click.testing import CliRunner

from serverlesspytool.cli import cli


def test_cli_base_execution():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
