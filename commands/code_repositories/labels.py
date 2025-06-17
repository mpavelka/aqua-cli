import sys
from commands import Command, CommandsRegistry
from app.code_repositories import (
    repositories_delete_label,
)


def register_commands(registry: CommandsRegistry):
    registry.register(RepositoriesDeleteLabelsCommand())


class RepositoriesDeleteLabelsCommand(Command):
    name = "repositories.labels.delete"
    help = "Delete labels from code repositories"

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            "--ids",
            type=str,
            nargs="*",
            help="IDs of repositories to delete label from.",
        )
        parser.add_argument(
            "--ids-stdin",
            action="store_true",
            help="Read repository IDs from standard input.",
        )
        parser.add_argument(
            "-l",
            "--labels",
            type=str,
            nargs="*",
            help="List of labels to delete from the repositories.",
        )
        parser.add_argument(
            "--labels-stdin",
            action="store_true",
            help="Read labels from standard input.",
        )

    def run(self, args):
        if args.ids_stdin and args.labels_stdin:
            print("Error: Cannot read both repository IDs and labels from stdin.")
            sys.exit(1)

        if args.ids_stdin:
            repository_ids = self.get_lines_from_stdin()
        else:
            repository_ids = args.ids   

        if args.labels_stdin:
            label_names = self.get_lines_from_stdin()
        else:
            label_names = args.labels

        if not repository_ids or not label_names:
            print("Error: Both repository IDs and label names must be provided.")
            sys.exit(1)

        print(
            f"Deleting labels {label_names} from repositories {repository_ids}", file=sys.stderr
        )

        for label_name in label_names:
            repositories_delete_label(
                label_name=label_name,
                repository_ids=repository_ids,
                formatter=self.get_formatter(args),
            )

