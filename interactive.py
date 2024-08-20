# interactive.py

import cmd
from core.scheduler import start_scheduler_in_background
from core.updater import fetch_updates
from models.subscription import add_subscription, remove_subscription, list_subscriptions
from reports.report_generator import generate_report
from core.notifier import notify

class GitHubSentinel(cmd.Cmd):
    intro = 'Welcome to GitHub Sentinel! Type help or ? to list commands.\n'
    prompt = '(GitHub Sentinel) '

    def do_add(self, repo_name):
        "Add a repository to the subscription list: add <owner/repo>"
        add_subscription(repo_name)
        print(f"Repository '{repo_name}' added to the subscription list.")

    def do_remove(self, repo_name):
        "Remove a repository from the subscription list: remove <owner/repo>"
        remove_subscription(repo_name)
        print(f"Repository '{repo_name}' removed from the subscription list.")

    def do_list(self, arg):
        "List all subscribed repositories"
        subscriptions = list_subscriptions()
        if subscriptions:
            print("Subscribed repositories:")
            for repo in subscriptions:
                print(f"  - {repo}")
        else:
            print("No subscriptions found.")

    def do_fetch(self, arg):
        "Fetch updates from subscribed repositories immediately"
        updates = fetch_updates()
        report = generate_report(updates)
        print(report)
        # notify(report)

    def do_exit(self, arg):
        "Exit the tool"
        print("Exiting GitHub Sentinel.")
        return True

if __name__ == '__main__':
    # Start scheduler in the background
    start_scheduler_in_background()
    # Start the interactive command line interface
    GitHubSentinel().cmdloop()
