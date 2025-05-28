from . import Command, CommandsRegistry


def register_commands(registry: CommandsRegistry):
    registry.register(SomeCommand())


class SomeCommand(Command):
    name = "test"
    help = "help"

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--arg",
            type=str,
            help="An example argument for the command.",
        )

    def run(self, args):
        print(args)
