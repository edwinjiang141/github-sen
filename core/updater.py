# core/updater.py

from config.settings import GITHUB_API_URL
from config.secrets import GITHUB_TOKEN
import requests

def fetch_updates():
    repositories = ["langchain-ai/langchain"]
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    updates = []

    for repo in repositories:
        url = f"{GITHUB_API_URL}/repos/{repo}/releases/latest"
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            updates.append(response.json())
            print(updates)
        else:
            print(f"Failed to fetch updates for {repo}: {response.status_code}")

    return updates