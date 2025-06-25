import os
import zipfile
from .to_snake_case import to_snake_case

def save_script(story_title: str, content: str, directory: str = "scripts"):
    """Saves a single script to a file."""
    os.makedirs(directory, exist_ok=True)
    file_name = f"test_{to_snake_case(story_title)}.py"
    path = os.path.join(directory, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def zip_scripts(scripts: list, directory: str = "scripts", zip_name: str = "selenium_scripts.zip") -> str:
    """Saves and zips a list of generated scripts."""
    os.makedirs(directory, exist_ok=True)
    script_paths = []
    for script in scripts:
        path = save_script(script['title'], script['script'], directory)
        script_paths.append(path)

    zip_path = os.path.join(directory, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for script_path in script_paths:
            zipf.write(script_path, arcname=os.path.basename(script_path))
    
    return zip_path 