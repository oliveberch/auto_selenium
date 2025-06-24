import os
import re

def to_snake_case(name):
    """Converts a string to a valid Python identifier in snake_case."""
    return "".join(c if c.isalnum() else "_" for c in name).lower()

def save_test_case(story_title, code, output_dir="tests"):
    """
    Saves the generated Selenium test code to a Python file.

    Args:
        story_title (str): The title of the user story.
        code (str): The generated Python code.
        output_dir (str): The directory to save the test file in.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_name = f"test_{to_snake_case(story_title)}.py"
    file_path = os.path.join(output_dir, file_name)
    
    try:
        with open(file_path, 'w') as f:
            f.write(code)
        print(f"Successfully saved test case to {file_path}")
    except IOError as e:
        print(f"Error saving test case to {file_path}: {e}")
