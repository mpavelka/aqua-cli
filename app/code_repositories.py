import sys
from app.client.code_repositories.labels import codesec_api_v1_repositories_label
from app.client.code_repositories.retrieve import (
    retrieve_code_repositories as c_retrieve_code_repositories,
    codesec_api_v1_repositories,
)
from app.client.code_repositories.selection import select_code_repositories
from app.formatter.table_formatter import TableFormatter


def retrieve_code_repositories(
    search: str,
    formatter=TableFormatter,
    keys=[
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
    formatter().print_formatted(repositories, keys)


def search_code_repositories(
    search: list[str],
    formatter=TableFormatter,
    keys=[
        "fullName",
        "id",
        "isArchived",
        "isPrivate",
        "isSelected",
        "lastPush",
    ],
):
    results = []
    for term in search:
        print(f"Searching: {term}", file=sys.stderr)
        response = c_retrieve_code_repositories(
            search=term,
        )
        repositories = response.json().get("repositories", [])
        results.extend(repositories)

    formatter().print_formatted(
        results,
        keys,
    )


def select_repositories_by_id(
    source,
    repository_ids,
    formatter=TableFormatter,
    keys=[
        "id",
        "name",
    ],
):
    response = select_code_repositories(
        source=source,
        include_ids=repository_ids,
    )
    response_json = response.json()
    formatter().print_formatted(
        response_json["addedRepositoriesMetadata"],
        keys,
    )


def repositories_retrieve_selected(
    ids: list[str] | None = None,
    name: str | None = None,
    formatter=TableFormatter,
    keys=[],
):
    response = codesec_api_v1_repositories(
        ids=ids,
        name=name,
        disable_pagination=True,
    )
    formatter().print_formatted(
        response.json().get("data", []),
        keys,
    )


def repositories_retrieve_selected_by_names(
    names: list[str],
    formatter=TableFormatter,
    keys=[],
):
    for name in names:
        repositories_retrieve_selected(
            name=name,
            formatter=formatter,
            keys=keys,
        )


def repositories_add_labels(
    label_names: list[str],
    repository_ids: list[str],
    delete_old_labels: bool = False,
    formatter=TableFormatter,
):
    response = codesec_api_v1_repositories_label(
        label_names=label_names,
        repository_ids=repository_ids,
        delete_old_labels=delete_old_labels,
    )
    formatter().print_formatted([{"message": response.text}], ["message"])
