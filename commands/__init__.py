import abc


class CommandsRegistry:
    def __init__(self, command_subparsers):
        self.command_subparsers = command_subparsers
        self.commands: dict[str, Command] = {}

    def register(self, command):

        if command.name in self.commands:
            raise ValueError(f"Command '{command.name}' is already registered.")

        parser = self.command_subparsers.add_parser(
            command.name,
            help=command.help,
        )
        command.add_arguments(parser)
        self.commands[command.name] = command

    def get_command(self, name):
        return self.commands.get(name)


class Command(abc.ABC):
    name = ""
    help = ""

    def __init__(self):
        if not self.name:
            raise ValueError("Command name must be set.")
        if not self.help:
            raise ValueError("Command help must be set.")

    @abc.abstractmethod
    def add_arguments(self, parser):
        """Add command-specific arguments to the parser."""
        pass

    @abc.abstractmethod
    def run(self, args):
        """Run the command with the provided arguments."""
        pass
