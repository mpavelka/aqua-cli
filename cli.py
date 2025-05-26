#!/usr/bin/env python3
import argparse
import os
from app.client.auth import authenticate
from app.client.client import AquaClient
from app.code_repositories import retrieve_code_repositories


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
        default=None,
        help="Optional search term to filter the repositories.",
    )

    args = parser.parse_args()

    # Set up AquaClient
    AquaClient.set_token_file_path(args.token_file)

    # Commands
    if args.command == "authenticate":
        return _cmd_authenticate(args)

    elif args.command == "repositories":
        retrieve_code_repositories(search=args.search)

    else:
        parser.print_help()
        return 1


def _cmd_authenticate(args):
    # Read API_KEY from envvars
    api_key = os.getenv("AQUA_API_KEY")
    api_secret = os.getenv("AQUA_API_SECRET")

    # Prompt user for the api_key or api_secret if not set
    if not api_key:
        api_key = input("Enter your API Key: ")
    if not api_secret:
        api_secret = input("Enter your API Secret: ")

    authenticate(api_key, api_secret, args.token_file)


if __name__ == "__main__":
    main()
