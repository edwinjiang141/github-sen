# interactive.py

import cmd
from core.github_client import GitHubClient
from reports.report_generator import ReportGenerator
from core.llm import LLM
from models.subscription import add_subscription, remove_subscription, list_subscriptions
from datetime import date
from config.configs import Config  # 导入配置管理模块
config = Config()
class GitHubSentinel(cmd.Cmd):
    intro = 'Welcome to GitHub Sentinel! Type help or ? to list commands.\n'
    prompt = '(GitHub Sentinel) '
    
    # 初始化 GitHubClient 实例
    def __init__(self):
        super().__init__()
        self.github_client = GitHubClient()

    # 添加订阅
    def do_add(self, repo_name):
        "Add a repository to the subscription list: add <owner/repo>"
        add_subscription(repo_name)
        print(f"Repository '{repo_name}' added to the subscription list.")

    # 移除订阅
    def do_remove(self, repo_name):
        "Remove a repository from the subscription list: remove <owner/repo>"
        remove_subscription(repo_name)
        print(f"Repository '{repo_name}' removed from the subscription list.")

    # 列出所有订阅
    def do_list(self, arg):
        "List all subscribed repositories"
        subscriptions = list_subscriptions()
        if subscriptions:
            print("Subscribed repositories:")
            for repo in subscriptions:
                print(f"  - {repo}")
        else:
            print("No subscriptions found.")

    # 手动获取订阅仓库的更新（issues 和 pull requests）
    def do_fetch(self, arg):
        "Fetch updates (issues and pull requests) from all subscribed repositories and generate daily Markdown reports"
        print("Fetching updates and generating daily reports...")
        self.github_client.generate_report()
        print("Daily reports generated successfully.")

    # 手动获取时间范围内的更新
    def do_fetch_range(self, args):
        "Fetch updates from all subscribed repositories based on time range: fetch_range <since> <until>"
        try:
            params = args.split()
            since = params[0]
            until = params[1] if len(params) > 1 else None

            since_date = date.fromisoformat(since).isoformat()
            until_date = date.fromisoformat(until).isoformat() if until else None

            print(f"Fetching updates from {since} to {until or 'now'}...")
            self.github_client.generate_report(since=since_date, until=until_date)
            print(f"Reports for the period {since} to {until or 'now'} generated successfully.")
        except (IndexError, ValueError):
            print("Please provide a valid 'since' date and optionally an 'until' date (in ISO format: YYYY-MM-DD).")


    # 生成最终报告
    def do_report(self, arg):
        "Generate a summarized report for the day by reading all daily reports"
        print("Generating final summarized report...")
        llm = LLM(config)
        report = ReportGenerator(llm)
        report.generate_final_report()
        print("Final report generated successfully.")

    # 退出工具
    def do_exit(self, arg):
        "Exit the tool"
        print("Exiting GitHub Sentinel.")
        return True

if __name__ == '__main__':
    # Start scheduler in the background
    # start_scheduler_in_background()
    # Start the interactive command line interface
    GitHubSentinel().cmdloop()
