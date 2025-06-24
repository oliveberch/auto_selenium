import json

def load_stories(file_path):
    """
    Loads user stories from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list: A list of user stories, or an empty list if an error occurs.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if 'backlog' not in data:
            print("Error: 'backlog' key not found in JSON file.")
            return []

        stories = []
        for epic in data.get('backlog', []):
            stories.extend(epic.get('stories', []))
        
        return stories

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return []
