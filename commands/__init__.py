import abc
import sys

from app.formatter.csv_formatter import CSVFormatter, CSVNoHeaderFormatter
from app.formatter.table_formatter import TableFormatter


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

    def get_lines_from_stdin(self):
        lines = []
        for line in sys.stdin:
            line = line.strip()
            if line:
                lines.append(line)
        return lines
    
    def get_arg_keys(self, args):
        return args.keys.split(",") if args.keys else []
    
    def get_formatter(self, args):
        if args.csv and args.no_header:
            return CSVNoHeaderFormatter
        elif args.csv:
            return CSVFormatter
        else:
            return TableFormatter
