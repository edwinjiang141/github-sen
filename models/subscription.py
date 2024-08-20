# models/subscription.py

import json
import os

SUBSCRIPTIONS_FILE = 'subscriptions.json'

def load_subscriptions():
    if not os.path.exists(SUBSCRIPTIONS_FILE):
        return []
    with open(SUBSCRIPTIONS_FILE, 'r') as file:
        return json.load(file)

def save_subscriptions(subscriptions):
    with open(SUBSCRIPTIONS_FILE, 'w') as file:
        json.dump(subscriptions, file, indent=4)

def add_subscription(repo_name):
    subscriptions = load_subscriptions()
    if repo_name not in subscriptions:
        subscriptions.append(repo_name)
        save_subscriptions(subscriptions)
        print(f"Repository '{repo_name}' added to the subscription list.")
    else:
        print(f"Repository '{repo_name}' is already in the subscription list.")

def remove_subscription(repo_name):
    subscriptions = load_subscriptions()
    if repo_name in subscriptions:
        subscriptions.remove(repo_name)
        save_subscriptions(subscriptions)
        print(f"Repository '{repo_name}' removed from the subscription list.")
    else:
        print(f"Repository '{repo_name}' not found in the subscription list.")

def list_subscriptions():
    return load_subscriptions()

