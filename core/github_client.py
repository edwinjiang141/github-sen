# core/github_client.py

import requests
import os
from datetime import datetime, timedelta
from config.settings import GITHUB_API_URL
from config.secrets import GITHUB_TOKEN
from models.subscription import load_subscriptions
from datetime import datetime, date, timedelta
from core.logger import LOG

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
    
    def fetch_updates(self, repo, since=None, until=None):
        # 获取指定仓库的更新，可以指定开始和结束日期
        updates = {
            'issues': self.get_issues(repo, since, until),  # 获取问题
            'pull_requests': self.get_pull_requests(repo, since, until)  # 获取拉取请求
        }
        return updates
    
    def export_progress_by_date_range(self, repo, days):
        today = date.today()  # 获取当前日期
        since = today - timedelta(days=days)  # 计算开始日期
        
        updates = self.fetch_updates(repo, since=since.isoformat(), until=today.isoformat())  # 获取指定日期范围内的更新
        
        repo_dir = os.path.join('daily_progress', repo.replace("/", "_"))  # 构建目录路径
        os.makedirs(repo_dir, exist_ok=True)  # 确保目录存在
        
        # 更新文件名以包含日期范围
        date_str = f"{since}_to_{today}"
        file_path = os.path.join(repo_dir, f'{date_str}.md')  # 构建文件路径
        
        with open(file_path, 'w') as file:
            file.write(f"# Progress for {repo} ({since} to {today})\n\n")
            file.write(f"\n## Issues Closed in the Last {days} Days\n")
            for issue in updates['issues']:  # 写入在指定日期内关闭的问题
                file.write(f"- {issue['title']} #{issue['number']}\n")
        
        LOG.info(f"[{repo}]项目最新进展文件生成： {file_path}")  # 记录日志
        return file_path
