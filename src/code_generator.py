import re

try:
    from langchain_ollama import OllamaLLM
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    DEFAULT_OLLAMA_MODEL = 'llama3.2'
    DEFAULT_CLAUDE_MODEL = 'claude-3-sonnet-20240229'
except ImportError:
    print("Warning: langchain libraries not installed. AI code generation will not work.")

def to_snake_case(name):
    """Converts a string to a valid Python identifier in snake_case."""
    return "".join(c if c.isalnum() else "_" for c in name).lower()


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


def generate_selenium_code(story, provider, test_steps=None, model_name=None):
    """
    Uses an LLM to generate robust Selenium test code from a user story and acceptance criteria.
    Returns the generated code as a string.
    """
    title = story.get("title", "unnamed_story")
    description = story.get("description", "")
    acceptance_criteria = story.get("acceptance_criteria", [])
    steps_str = ""
    if test_steps:
        # Format test steps for the prompt
        steps_str = "\n".join([
            f"- {step.get('action', '')}: {step.get('details', '')}" for step in test_steps
        ])
    prompt_template = '''
You are an expert Python Selenium test developer.
Given the following user story and acceptance criteria, generate a complete pytest-based Selenium test function.
- Use best practices for waits, selectors, and assertions.
- Add comments explaining each step.
- Use clear and robust code.

User Story:
Title: {title}
Description: {description}
Acceptance Criteria:
{acceptance_criteria}

{steps_section}
Output only the Python code for the test (including imports and fixtures).
'''
    steps_section = f"Test Steps (optional):\n{steps_str}" if steps_str else ""
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["title", "description", "acceptance_criteria", "steps_section"],
    )
    try:
        llm = get_llm(provider, model_name)
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
            "title": title,
            "description": description,
            "acceptance_criteria": "\n".join(acceptance_criteria),
            "steps_section": steps_section
        })
        # Clean up response (remove code fences if present)
        cleaned = response.strip()
        # Improved: Only keep the Python code block
        code_lines = []
        in_code = False
        for line in cleaned.splitlines():
            # Start at the first import or def
            if not in_code and (line.strip().startswith('import') or line.strip().startswith('from') or line.strip().startswith('def') or line.strip().startswith('@')):
                in_code = True
            if in_code:
                # Stop if we hit a markdown explanation, list, or summary
                if line.strip().startswith('```') or line.strip().startswith('This code') or line.strip().startswith('The test') or line.strip().startswith('1.') or line.strip().startswith('*') or line.strip().startswith('# Run the test'):
                    break
                code_lines.append(line)
        return '\n'.join(code_lines).strip()
    except Exception as e:
        print(f"AI code generation failed for story '{title}': {e}")
        return None