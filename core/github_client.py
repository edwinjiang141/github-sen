# core/github_client.py

import requests
import os
from datetime import datetime, timedelta
from config.settings import GITHUB_API_URL
from config.secrets import GITHUB_TOKEN
from models.subscription import load_subscriptions

class GitHubClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

    def get_issues(self, repo_name, since=None, until=None):
        url = f"{GITHUB_API_URL}/repos/{repo_name}/issues"
        params = {}

        # 如果传入了时间范围，加入 since 参数
        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            issues = response.json()

            # 如果传入了 until 参数，手动过滤超出截止日期的 issues
            if until:
                until_date = datetime.fromisoformat(until)
                issues = [issue for issue in issues if datetime.fromisoformat(issue['created_at'][:-1]) <= until_date]

            return issues
        else:
            print(f"Failed to fetch issues for {repo_name}: {response.status_code}")
            return []

    def get_pull_requests(self, repo_name, since=None, until=None):
        url = f"{GITHUB_API_URL}/repos/{repo_name}/pulls"
        params = {}

        if since:
            params['since'] = since

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            pulls = response.json()

            # 如果传入了 until 参数，手动过滤超出截止日期的 pull requests
            if until:
                until_date = datetime.fromisoformat(until)
                pulls = [pull for pull in pulls if datetime.fromisoformat(pull['created_at'][:-1]) <= until_date]

            return pulls
        else:
            print(f"Failed to fetch pull requests for {repo_name}: {response.status_code}")
            return []

    def generate_report(self, since=None, until=None):
        subscriptions = load_subscriptions()
        report_date = datetime.now().strftime("%Y-%m-%d")
        since_date = since if since else (datetime.now() - timedelta(days=1)).isoformat()

        for repo in subscriptions:
            issues = self.get_issues(repo, since=since_date, until=until)
            pulls = self.get_pull_requests(repo, since=since_date, until=until)

            markdown_content = f"# {repo} - Report (from {since_date} to {until or 'now'})\n\n"
            markdown_content += "## Issues:\n"
            for issue in issues:
                markdown_content += f"- [{issue['title']}]({issue['html_url']}) (#{issue['number']})\n"

            markdown_content += "\n## Pull Requests:\n"
            for pull in pulls:
                markdown_content += f"- [{pull['title']}]({pull['html_url']}) (#{pull['number']})\n"

            filename = f"{repo.replace('/', '_')}_{report_date}.md"
            with open(os.path.join("reports", filename), "w") as file:
                file.write(markdown_content)

            print(f"Report for {repo} saved as {filename}")
