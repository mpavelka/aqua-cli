from app.client.client import AquaClient
from app.formatter.table_formatter import TableFormatter


def select_code_repositories(
    source: str,
    integration_id: str | None = None,
    integration_name: str | None = None,
    include_by_days: int | None = None,
    select_all: bool = False,
    include_ids=[],
    exclude_ids=[],
):
    payload = {
        "source": source,
        "includeIds": include_ids,
        "excludeIds": exclude_ids,
        "selectAll": select_all,
    }
    if integration_id:
        payload["integrationId"] = integration_id
    if integration_name:
        payload["integrationName"] = integration_name
    if include_by_days is not None:
        payload["includeByDays"] = include_by_days

    response = AquaClient.post("/codesec/api/repositories/selection", json=payload)
    if response.status_code != 200:
        raise Exception(f"Error selecting code repositories: {response.text}")

    return response
