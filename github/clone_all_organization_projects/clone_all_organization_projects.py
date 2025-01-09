# github/clone_all_organization_projects/clone_all_organization_projects.py
import os

import requests
from env_variables import CLONE_DIR, GITHUB_TOKEN, ORG_NAME

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def clone_repos():
    os.makedirs(CLONE_DIR, exist_ok=True)
    page = 1
    while True:
        response = requests.get(
            f"https://api.github.com/orgs/{ORG_NAME}/repos?type=all&per_page=100&page={page}",
            headers=headers,
        )
        data = response.json()
        if response.status_code != 200 or not data:
            break

        for repo in data:
            os.system(f"git clone {repo['ssh_url']} {os.path.join(CLONE_DIR, repo['name'])}")

        if "next" not in response.links:
            break
        page += 1


if __name__ == "__main__":
    clone_repos()
