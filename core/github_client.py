# core/github_client.py

import requests
import os
from datetime import datetime
from config.settings import GITHUB_API_URL
from config.secrets import GITHUB_TOKEN
from models.subscription import load_subscriptions

class GitHubClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }
    
    def get_issues(self, repo_name):
        url = f"{GITHUB_API_URL}/repos/{repo_name}/issues"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch issues for {repo_name}: {response.status_code}")
            return []

    def get_pull_requests(self, repo_name):
        url = f"{GITHUB_API_URL}/repos/{repo_name}/pulls"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch pull requests for {repo_name}: {response.status_code}")
            return []

    def generate_daily_report(self):
        subscriptions = load_subscriptions()
        today = datetime.now().strftime("%Y-%m-%d")

        for repo in subscriptions:
            issues = self.get_issues(repo)
            pulls = self.get_pull_requests(repo)
            
            markdown_content = f"# {repo} - Daily Report ({today})\n\n"
            markdown_content += "## Issues:\n"
            for issue in issues:
                markdown_content += f"- [{issue['title']}]({issue['html_url']}) (#{issue['number']})\n"

            markdown_content += "\n## Pull Requests:\n"
            for pull in pulls:
                markdown_content += f"- [{pull['title']}]({pull['html_url']}) (#{pull['number']})\n"

            # 写入 Markdown 文件
            filename = f"{repo.replace('/', '_')}_{today}.md"
            with open(os.path.join("reports", filename), "w") as file:
                file.write(markdown_content)

            print(f"Daily report for {repo} saved as {filename}")
