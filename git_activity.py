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

    for event in events:
        event_type = event.get('type')
        repo_name = event['repo']['name']

        if event_type == 'PushEvent':
            commits_list = event['payload'].get('commits', [])
            print(f"- Pushed {len(commits_list)} commits to {repo_name}")
        
        elif event_type == 'IssuesEvent':
            action = event['payload']['action']
            print(f"- {action.capitalize()} an issue in {repo_name}")

        elif event_type == 'WatchEvent':
            print(f"- Starred {repo_name}")

if __name__ == "__main__":
    main()