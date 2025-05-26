import pprint
from app.client.code_repositories.retrieve import (
    retrieve_code_repositories as c_retrieve_code_repositories,
)
from app.client.code_repositories.selection import select_code_repositories
from app.formatter.table_formatter import TableFormatter


def retrieve_code_repositories(
    search=None,
    formatter=TableFormatter,
    columns=[
        "fullName",
        "id",
        "isArchived",
        "isPrivate",
        "isSelected",
        "lastPush",
    ],
):
    response = c_retrieve_code_repositories(
        search=search,
    )
    repositories = response.json().get("repositories", [])
    formatter(columns).print_formatted(repositories)


def select_repositories_by_id(
    source,
    repository_ids,
    formatter=TableFormatter,
    columns=[
        "id",
        "name",
    ],
):
    response = select_code_repositories(
        source=source,
        include_ids=repository_ids,
    )
    response_json = response.json()
    formatter(columns).print_formatted(response_json["addedRepositoriesMetadata"])
