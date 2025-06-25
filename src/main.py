from src.json_reader import load_stories
from src.ai_processor import generate_test_steps, generate_user_stories_from_requirements, read_requirements_from_file
from src.code_generator import generate_selenium_code
from src.output_writer import save_test_case
import json
import os
from dotenv import load_dotenv

# --- Pre-computation ---
load_dotenv()

# --- Configuration ---
JSON_FILE = 'data.json'
REQUIREMENTS_FILE = 'proj-requirements.txt'

# --- LLM Settings ---
# Set the provider to 'ollama' or 'claude'
LLM_PROVIDER = 'ollama' 

# Model names for each provider
OLLAMA_MODEL = 'llama3.2'
CLAUDE_MODEL = 'claude-sonnet-4-20250514'

# --- Feature Flags ---
# Set this to True to generate user stories from requirements before running tests
generate_stories_first = False

def main():
    # Determine which model to use based on the provider
    model_name = OLLAMA_MODEL if LLM_PROVIDER == 'ollama' else CLAUDE_MODEL
    
    if generate_stories_first and os.path.exists(REQUIREMENTS_FILE):
        requirements = read_requirements_from_file(REQUIREMENTS_FILE)
        if requirements:
            print(f'Generating user stories using {LLM_PROVIDER.capitalize()}...')
            stories_json = generate_user_stories_from_requirements(
                requirements, 
                provider=LLM_PROVIDER, 
                model_name=model_name
            )
            if stories_json:
                with open(JSON_FILE, 'w') as f:
                    json.dump(stories_json, f, indent=2)
                print(f'User stories written to {JSON_FILE}')
            else:
                print('Failed to generate user stories.')
        else:
            print('No requirements found. Skipping story generation.')

    stories = load_stories(JSON_FILE)
    if not stories:
        print('No stories found. Exiting.')
        return
        
    print(f'Found {len(stories)} stories to process using {LLM_PROVIDER.capitalize()}.')
    for story in stories:
        story_title = story.get('title', 'Untitled Story')
        print(f'--- Processing Story: {story_title} ---')
        
        test_steps = generate_test_steps(
            story, 
            provider=LLM_PROVIDER, 
            model_name=model_name
        )
        if not test_steps:
            print(f'Could not generate test steps for story: {story_title}')
            continue
        print(f'Generated {len(test_steps)} test steps.')
        
        selenium_code = generate_selenium_code(
            story, 
            provider=LLM_PROVIDER, 
            test_steps=test_steps, 
            model_name=model_name
        )
        if not selenium_code:
            print(f'Could not generate selenium code for story: {story_title}')
            continue
            
        save_test_case(story_title, selenium_code)
        print('-' * 50)

if __name__ == '__main__':
    main()