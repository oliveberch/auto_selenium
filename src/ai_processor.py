import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# TODO: Ask user for the specific Ollama model they are using. Defaulting to 'llama2'.
DEFAULT_MODEL = 'llama3.2'

def generate_test_steps(story, model_name=DEFAULT_MODEL):
    """
    Generates structured test steps from a user story using an LLM.

    Args:
        story (dict): A dictionary representing the user story.
        model_name (str): The name of the Ollama model to use.

    Returns:
        list: A list of dictionaries, where each dictionary is a test step.
              Returns an empty list if generation fails.
    """
    template = """
    You are an expert in software testing and Selenium. Your task is to convert a user story and its acceptance criteria into a list of concrete, actionable steps for a Selenium test.

    Provide the output as a JSON array of objects, where each object has an "action" and "details".
    Possible actions are: "navigate", "click", "type", "select", "assert_text", "assert_element".
    
    - For "navigate", "details" should be the URL.
    - For "click", "details" should be the CSS selector of the element to click.
    - For "type", "details" should be a dictionary with "selector" (CSS selector) and "text".
    - For "select", "details" should be a dictionary with "selector" (CSS selector) and "value".
    - For "assert_text", "details" should be the text to check for on the page.
    - For "assert_element", "details" should be the CSS selector of the element to verify its presence.

    IMPORTANT: Your response must be a valid JSON array. Do not include any explanatory text.
    Example format:
    [
        {{"action": "navigate", "details": "https://example.com"}},
        {{"action": "type", "details": {{"selector": "#email", "text": "user@example.com"}}}}
    ]

    User Story:
    Title: {title}
    Description: {description}
    Acceptance Criteria:
    {acceptance_criteria}

    Response (JSON array only):
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["title", "description", "acceptance_criteria"],
    )

    try:
        llm = OllamaLLM(
            model=model_name,
            temperature=0.7,
            format="json"
        )

        chain = prompt | llm | StrOutputParser()

        story_input = {
            "title": story.get("title"),
            "description": story.get("description"),
            "acceptance_criteria": "\n".join(story.get("acceptance_criteria", [])),
        }
        
        response = chain.invoke(story_input)
        
        # Clean up the response to make it valid JSON
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        # If the response isn't a list/array, wrap it in one
        if not cleaned_response.startswith('['):
            cleaned_response = f'[{cleaned_response}]'
            
        test_steps = json.loads(cleaned_response)
        if isinstance(test_steps, list):
            return test_steps
        return []

    except Exception as e:
        print(f"Error generating test steps for story '{story.get('title')}': {e}")
        return []
