from app.client.client import AquaClient


def retrieve_code_repositories(
    search=None,
):
    params = {}
    if search is not None:
        params["search"] = search

    response = AquaClient.get("/codesec/v1/api/repositories", params=params)
    if response.status_code != 200:
        raise Exception(f"Error retrieving code repositories: {response.text}")

    return response


def codesec_api_v1_repositories(
    ids: list[str] | None = None,
    name: str | None = None,
    disable_pagination: bool = False,
):
    """
    Retrieves code repositories from the Aqua Security API.

    :param search: Search term to filter repositories by name.
    """
    params = {
        "disable_pagination": str(disable_pagination).lower(),
    }
    if name is not None:
        params["name"] = name
    if ids is not None:
        params["ids"] = ids

    response = AquaClient.get("/codesec/api/v1/repositories", params=params)
    if response.status_code != 200:
        raise Exception(f"Error retrieving code repositories: {response.text}")

    return response
