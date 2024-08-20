# core/updater.py

import requests
from config.settings import GITHUB_API_URL
from config.secrets import GITHUB_TOKEN
from models.subscription import load_subscriptions

def fetch_updates():
    # 从文件中读取用户订阅的仓库列表
    repositories = load_subscriptions()
    if not repositories:
        print("No repositories subscribed.")
        return []

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }
    updates = []

    for repo in repositories:
        url = f"{GITHUB_API_URL}/repos/{repo}/releases/latest"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            updates.append(response.json())
        else:
            print(f"Failed to fetch updates for {repo}: {response.status_code} - {response.text}")

    return updates
