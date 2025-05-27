#!/usr/bin/env python3
import argparse
import os
import sys
from app.client.auth import authenticate
from app.client.client import AquaClient
from app.code_repositories import (
    repositories_add_labels,
    retrieve_code_repositories,
    search_code_repositories,
    select_repositories_by_id,
    repositories_retrieve_selected,
    repositories_retrieve_selected_by_names,
)
from app.formatter.csv_formatter import CSVFormatter, CSVNoHeaderFormatter
from app.formatter.table_formatter import TableFormatter


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool for interacting with the Aqua API."
    )
    parser.add_argument("--version", action="version", version="Aqua CLI 1.0.0")
    parser.add_argument(
        "--token-file",
        type=str,
        default=".aqua_token",
        help="Path to the file where the authentication token will be stored.",
    )
    parser.add_argument(
        "--ca-cert",
        type=str,
        default="",
        help="Path to the CA certificate file for secure connections.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Output results in CSV format instead of the default table format.",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Do not print the header in the formatted output.",
    )
    parser.add_argument(
        "--keys",
        "-k",
        type=str,
        nargs="*",
        default=[],
        help="List of keys to include in the output. If not provided, default keys will be included.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Authenticate
    subparsers.add_parser("authenticate", help="Authenticate with the Aqua API.")

    # Repositories: Retrieve code repositories
    repositories = subparsers.add_parser(
        "repositories",
        help="Retrieve code repositories from the Aqua API.",
    )
    repositories.add_argument(
        "-s",
        "--search",
        type=str,
        help="Optional search term to filter the repositories.",
    )
    # Repositories: Search code repositories
    repositories_search = subparsers.add_parser(
        "repositories-search",
        help="Retrieve code repositories from the Aqua API.",
    )
    repositories_search.add_argument(
        "search",
        type=str,
        nargs="*",
        help="Search terms to filter the repositories. Supports multiple terms.",
    )
    repositories_search.add_argument(
        "-i",
        "--stdin",
        action="store_true",
        help="Read search terms from standard input instead of command line. Suports multiple lines of input.",
    )
    # Repositories: Select repositories
    select_repositories = subparsers.add_parser(
        "select-repositories",
        help="Add code repositories to Aqua by their IDs.",
    )
    select_repositories.add_argument(
        "--stdin",
        action="store_true",
        help="Read repository IDs from standard input if not provided as arguments.",
    )
    select_repositories.add_argument(
        "--source",
        type=str,
        default=None,
        help="Source from which to select repositories (default: gitlab_server).",
    )
    select_repositories.add_argument(
        "repository_ids",
        type=str,
        nargs="*",
        help="List of repository IDs to add to Aqua.",
    )
    # Repositories: Retrieve selected code repositories
    repositories_retrieve_selected = subparsers.add_parser(
        "repositories-retrieve-selected",
        help="Retrieve repositories that have been previously selected.",
    )
    repositories_retrieve_selected.add_argument(
        "-i",
        "--ids",
        type=str,
        nargs="*",
        help="IDs of repositories to retrieve.",
    )
    repositories_retrieve_selected.add_argument(
        "-n",
        "--name",
        type=str,
        help="Name of the repository to retrieve.",
    )
    repositories_retrieve_selected.add_argument(
        "--stdin",
        action="store_true",
        help="Read IDs from stdin.",
    )
    repositories_retrieve_selected.add_argument(
        "--names",
        type=str,
        nargs="*",
        help="Names of repositories to filter. If provided, all other search parameters are ignored.",
    )
    repositories_retrieve_selected.add_argument(
        "--names-stdin",
        action="store_true",
        help="Read names from stdin. If provided, all other search parameters are ignored.",
    )
    # Repositories: Add labels
    repositories_add_label = subparsers.add_parser(
        "repositories-add-labels",
        help="Add labels to code repositories.",
    )
    repositories_add_label.add_argument(
        "-i",
        "--ids",
        type=str,
        nargs="*",
        help="IDs of repositories to add the labels to.",
    )
    repositories_add_label.add_argument(
        "--ids-stdin",
        action="store_true",
        help="Read repository IDs from standard input.",
    )
    repositories_add_label.add_argument(
        "-l",
        "--labels",
        type=str,
        nargs="*",
        help="List of labels to add to the repositories.",
    )
    repositories_add_label.add_argument(
        "--labels-stdin",
        action="store_true",
        help="Read labels from standard input.",
    )

    args = parser.parse_args()

    # Set up AquaClient
    if args.ca_cert:
        AquaClient.verify = args.ca_cert
    AquaClient.set_token_file_path(args.token_file)

    # Commands
    if args.command == "authenticate":
        _cmd_authenticate(args)

    elif args.command == "repositories":
        retrieve_code_repositories(
            search=args.search,
            formatter=_get_formatter(args),
        )

    elif args.command == "repositories-search":
        _cmd_search_code_repositories(args)

    elif args.command == "select-repositories":
        _cmd_select_repositories(args)

    elif args.command == "repositories-retrieve-selected":
        _cmd_repositories_retrieve_selected(args)
    
    elif args.command == "repositories-add-labels":
        _cmd_repositories_add_labels(args)

    else:
        parser.print_help()
        return 1


def _get_formatter(args):
    if args.csv and args.no_header:
        return CSVNoHeaderFormatter
    elif args.csv:
        return CSVFormatter
    else:
        return TableFormatter


def _cmd_authenticate(args):
    # Read API_KEY from envvars
    api_key = os.getenv("AQUA_API_KEY")
    api_secret = os.getenv("AQUA_API_SECRET")

    # Prompt user for the api_key or api_secret if not set
    if not api_key:
        api_key = input("Enter your API Key: ")
    if not api_secret:
        api_secret = input("Enter your API Secret: ")

    authenticate(
        api_key,
        api_secret,
        args.token_file,
        args.ca_cert,
    )


def _cmd_search_code_repositories(args):
    if args.stdin:
        search_terms = _get_lines_from_stdin()
        args.search = search_terms

    search_code_repositories(
        search=args.search,
        formatter=_get_formatter(args),
        keys=args.keys,
    )


def _cmd_select_repositories(args):
    if args.stdin:
        repository_ids = _get_lines_from_stdin()
    else:
        repository_ids = args.repository_ids

    select_repositories_by_id(
        source=args.source,
        repository_ids=repository_ids,
        formatter=_get_formatter(args),
        keys=args.keys,
    )


def _cmd_repositories_retrieve_selected(args):
    if args.names_stdin:
        repositories_retrieve_selected_by_names(
            names=_get_lines_from_stdin(),
            formatter=_get_formatter(args),
            keys=args.keys,
        )
    elif args.names:
        repositories_retrieve_selected_by_names(
            names=args.names,
            formatter=_get_formatter(args),
            keys=args.keys,
        )
    else:
        if args.stdin:
            args.ids = _get_lines_from_stdin()
        repositories_retrieve_selected(
            ids=args.ids,
            name=args.name,
            formatter=_get_formatter(args),
            keys=args.keys,
        )

def _cmd_repositories_add_labels(args):
    if args.ids_stdin and args.labels_stdin:
        print("Error: Cannot read both repository IDs and labels from stdin.")
        sys.exit(1)

    if args.ids_stdin:
        repository_ids = _get_lines_from_stdin()
    else:
        repository_ids = args.ids

    if args.labels_stdin:
        label_names = _get_lines_from_stdin()
    else:
        label_names = args.labels

    if not repository_ids or not label_names:
        print("Error: Both repository IDs and label names must be provided.")
        sys.exit(1)
    
    repositories_add_labels(
        label_names=label_names,
        repository_ids=repository_ids,
        formatter=_get_formatter(args),
        keys=args.keys,
    )

def _get_lines_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    return lines


if __name__ == "__main__":
    main()
