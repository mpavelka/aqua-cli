
from app.client.client import AquaClient


def codesec_api_v1_repositories_label(
    label_names: list[str],
    repository_ids: list[str],
    delete_old_labels: bool = False,
):
    payload = {
        "labelNames": label_names,
        "repositoryIds": repository_ids,
        "deleteOldLabels": delete_old_labels,
    }

    response = AquaClient.post("/codesec/api/v1/repositories/labels", json=payload)
    if response.status_code != 200:
        raise Exception(f"Error retrieving code repositories labels: {response.text}")

    return response


def delete_codesec_api_v1_repositories_labels(
    label_name: list[str],
    repository_ids: list[str],
):
    payload = {
        "labelName": label_name,
        "repositoryIds": repository_ids,
    }

    response = AquaClient.delete("/codesec/api/v1/repositories/labels", json=payload)
    if response.status_code != 200:
        raise Exception(f"Error deleting code repositories labels: {response.text}")

    return response
