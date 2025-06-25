import json
from langchain_ollama import OllamaLLM
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import datetime

# TODO: Ask user for the specific Ollama model they are using. Defaulting to 'llama2'.
DEFAULT_OLLAMA_MODEL = 'llama3.2'
DEFAULT_CLAUDE_MODEL = 'claude-sonnet-4-20250514'

def get_llm(provider, model_name=None, output_format=None):
    if provider == 'claude':
        model = model_name or DEFAULT_CLAUDE_MODEL
        return ChatAnthropic(model=model, temperature=0.2)
    elif provider == 'ollama':
        model = model_name or DEFAULT_OLLAMA_MODEL
        if output_format == 'json':
            return OllamaLLM(model=model, temperature=0.2, format="json")
        return OllamaLLM(model=model, temperature=0.2)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def generate_test_steps(story, provider, model_name=None):
    """
    Generates structured test steps from a user story using an LLM.

    Args:
        story (dict): A dictionary representing the user story.
        provider (str): The LLM provider to use ('ollama' or 'claude').
        model_name (str): The name of the LLM model to use.

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
        llm = get_llm(provider, model_name, output_format='json')

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


def generate_user_stories_from_requirements(requirements, provider, model_name=None):
    """
    Generates user stories in the required template from functional requirements using an LLM.

    Args:
        requirements (str): The functional requirements as a string.
        provider (str): The LLM provider to use ('ollama' or 'claude').
        model_name (str): The name of the LLM model to use.

    Returns:
        dict: The generated user stories in the required JSON template.
    """
    template = '''
    You are an expert agile analyst. Given the following functional requirements:
    {requirements}

    Generate a product backlog in the following JSON format (no preamble, only valid JSON!):
    {{
      "backlog": [
        {{
          "epic": "Epic Name (e.g., 'Payment System')",
          "description": "Brief epic goal (optional)",
          "stories": [
            {{
              "title": "User Story Title (e.g., 'Process Credit Card Payments')",
              "description": "As a [user role], I want [action] so that [benefit].",
              "acceptance_criteria": [
                "Criterion 1 (e.g., 'Supports Visa/Mastercard')",
                "Criterion 2 (e.g., 'Declined cards show error messages')"
              ],
              "priority": "high/medium/low",
              "status": "todo/in-progress/done (optional)",
              "story_points": 3 (optional),
              "dependencies": ["story_id_1", "story_id_2"] (optional)
            }}
          ]
        }}
      ],
      "metadata": {{
        "version": "1.0",
        "last_updated": "YYYY-MM-DD",
        "total_epics": 0,
        "total_stories": 0
      }}
    }}
    - Group stories under appropriate epics.
    - Fill out as many fields as possible, but optional fields can be omitted if not clear.
    - Do not include any explanation, only output valid JSON.
    '''

    prompt = PromptTemplate(
        template=template,
        input_variables=["requirements"],
    )

    try:
        llm = get_llm(provider, model_name, output_format='json')
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"requirements": requirements})
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        data = json.loads(cleaned_response)

        # Post-process to ensure metadata is correct
        backlog = data.get('backlog', [])
        total_epics = len(backlog)
        total_stories = sum(len(epic.get('stories', [])) for epic in backlog)
        today = datetime.date.today().isoformat()
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['version'] = '1.0'
        data['metadata']['last_updated'] = today
        data['metadata']['total_epics'] = total_epics
        data['metadata']['total_stories'] = total_stories
        return data
    except Exception as e:
        print(f"Error generating user stories: {e}")
        return None

def read_requirements_from_file(file_path):
    """
    Reads requirements from a text file.
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading requirements file: {e}")
        return None
