import sys
import requests
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python git_activity.py <username>")
        return
    
    username = sys.argv[1]
    
    url = f"https://api.github.com/users/{username}/events"

    response = requests.get(url)
    
    if response.status_code == 404:
        print("User not found.")
        return
    elif response.status_code != 200:
        print(f"Error: {response.status_code}")
        return
    
    events = response.json()

    # formatted_data = json.dumps(events, indent=2)
    # print(formatted_data)
    if response.status_code == 200:
        lastest_event = events
        print(f"\nLatest events for {username}")

    seen_push = False
    seen_issue = False
    seen_watch = False

    for event in events:
        event_type = event.get('type')
        repo_name = event['repo']['name']

        if event_type == 'PushEvent' and not seen_push:
            # GitHub has discontinued sending commit counts via this API (updated Oct 2025).
            # Therefore, we will now only indicate that a commit has been pushed.
            print(f"- Pushed updates to {repo_name}")
            seen_push = True
        
        elif event_type == 'IssuesEvent' and not seen_issue:
            action = event['payload']['action']
            print(f"- {action.capitalize()} an issue in {repo_name}")
            seen_issue = True

        elif event_type == 'WatchEvent' and not seen_watch:
            print(f"- Starred {repo_name}")
            seen_watch = True

        if seen_push and seen_issue and seen_watch:
            break

if __name__ == "__main__":
    main()