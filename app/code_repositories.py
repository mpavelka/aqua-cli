import pprint
from app.client.code_repositories.retrieve import (
    retrieve_code_repositories as c_retrieve_code_repositories,
)
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
    if response.status_code == 200:
        repositories = response.json().get("repositories", [])
        formatter(columns).print_formatted(repositories)
    else:
        raise Exception(f"Failed to retrieve code repositories: {response.text}")
