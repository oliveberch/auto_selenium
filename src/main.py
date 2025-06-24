from src.json_reader import load_stories
from src.ai_processor import generate_test_steps
from src.code_generator import generate_selenium_code
from src.output_writer import save_test_case

JSON_FILE = 'data.json'
OLLAMA_MODEL = 'llama3.2'

def main():
    stories = load_stories(JSON_FILE)
    if not stories:
        print('No stories found. Exiting.')
        return
    print(f'Found {len(stories)} stories to process.')
    for story in stories:
        story_title = story.get('title', 'Untitled Story')
        print(f'--- Processing Story: {story_title} ---')
        test_steps = generate_test_steps(story, model_name=OLLAMA_MODEL)
        if not test_steps:
            print(f'Could not generate test steps for story: {story_title}')
            continue
        print(f'Generated {len(test_steps)} test steps.')
        selenium_code = generate_selenium_code(story, test_steps)
        if not selenium_code:
            print(f'Could not generate selenium code for story: {story_title}')
            continue
        save_test_case(story_title, selenium_code)
        print('-' * 50)

main()