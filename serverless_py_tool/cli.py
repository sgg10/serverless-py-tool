import os
from typing import Any, List, MutableMapping, Optional, Sequence

import click
from click.core import Command, Context
from click.formatting import HelpFormatter

commands_type = MutableMapping[str, Command] or Sequence[Command]


class CLIGroup(click.Group):

    def __init__(
        self,
        name: Optional[str] = None,
        commands: Optional[commands_type] = None,
        **attrs: Any
    ) -> None:
        super().__init__(name, commands, **attrs)
        self.commands_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "commands")
        )

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        formatter.write_usage(
            ctx.command_path,
            "<command> [<subcommand>] [OPTIONS] [ARGS]"
        )

    def _get_command_list(self, base_path: str) -> List[str]:
        return [
            filename.replace("cmd_", "").replace(".py", "")
            for filename in os.listdir(base_path)
            if filename.startswith("cmd_") and filename.endswith(".py")
        ]

    def list_commands(self, ctx: Context) -> List[str]:
        commands = self._get_command_list(self.commands_directory)
        groups = [
            d for d in os.listdir(self.commands_directory)
            if os.path.isdir(os.path.join(self.commands_directory, d))
            and not d.startswith("__") and not d.endswith("__")
        ]
        return sorted(commands) + sorted(groups)

    def get_command(self, ctx: Context, name: str) -> Command or None:
        if os.path.isdir(os.path.join(self.commands_directory, name)):
            group_path = os.path.join(
                os.path.dirname(__file__),
                "commands",
                name
            )
            commands = self._get_command_list(group_path)

            @click.group(
                name=name,
                help=f"Commands Group for {name.capitalize()} resource"
            )
            def group():
                f"""{name.capitalize()} resource commands"""
                pass

            for cmd_name in commands:
                try:
                    mod = __import__(
                        f"serverless_py_tool.commands.{name}.cmd_{cmd_name}",
                        None,
                        None,
                        ["command"]
                    )
                    group.add_command(mod.command, name=cmd_name)
                except ImportError as e:
                    print(e)
                    continue

            return group
        else:
            try:
                mod = __import__(
                    f"serverless_py_tool.commands.cmd_{name}",
                    None,
                    None,
                    ["command"]
                )
            except ImportError as e:
                print(e)
                return
            return mod.command


@click.group(cls=CLIGroup)
def cli():
    pass


if __name__ == "__main__":
    cli()
