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
