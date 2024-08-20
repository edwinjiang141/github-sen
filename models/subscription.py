# models/subscription.py

subscriptions = []

def add_subscription(repo_name):
    if repo_name not in subscriptions:
        subscriptions.append(repo_name)

def remove_subscription(repo_name):
    if repo_name in subscriptions:
        subscriptions.remove(repo_name)

def list_subscriptions():
    return subscriptions
