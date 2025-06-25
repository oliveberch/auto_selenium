import json
from app.core.llm_utils import get_llm, PromptTemplate, StrOutputParser

def generate_selenium_scripts(user_stories, model_id):
    """
    For each user story, generate test steps and then Selenium code using the LLM.
    Returns a list of dicts with 'title' and 'script'.
    """
    if isinstance(user_stories, str):
        user_stories = json.loads(user_stories)
    scripts = []
    for story in user_stories:
        title = story.get("title", "unnamed_story")
        description = story.get("description", "")
        acceptance_criteria = story.get("acceptance_criteria", [])
        url = story.get("url", "YOUR_APP_URL_HERE")
        page = story.get("page", "the relevant page")
        # 1. Generate test steps
        steps_template = """
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
        steps_prompt = PromptTemplate(
            template=steps_template,
            input_variables=["title", "description", "acceptance_criteria"],
        )
        try:
            llm = get_llm(model_id, output_format='json')
            chain = steps_prompt | llm | StrOutputParser()
            steps_response = chain.invoke({
                "title": title,
                "description": description,
                "acceptance_criteria": "\n".join(acceptance_criteria),
            })
            cleaned_steps = steps_response.strip()
            if cleaned_steps.startswith('```json'):
                cleaned_steps = cleaned_steps[7:]
            if cleaned_steps.endswith('```'):
                cleaned_steps = cleaned_steps[:-3]
            cleaned_steps = cleaned_steps.strip()
            test_steps = json.loads(cleaned_steps)
        except Exception as e:
            print(f"Error generating test steps for story '{title}': {e}")
            test_steps = []
        # 2. Generate Selenium code
        code_template = '''
            You are an expert Python Selenium test developer.
            Given the following user story, acceptance criteria, and application context, generate a complete, runnable pytest-based Selenium test function.
            - Use the provided URL and Page information directly in the script.
            - Do not use placeholder values.
            - Use best practices for waits, selectors, and assertions.
            - Add comments explaining each step.
            - Use clear and robust code.

            Application Context:
            URL: {url}
            Page/Component: {page}

            User Story:
            Title: {title}
            Description: {description}
            Acceptance Criteria:
            {acceptance_criteria}
            {steps_section}
            Output only the Python code for the test (including imports and fixtures). No explanations.
            '''
        steps_section = f"Test Steps (optional):\n{json.dumps(test_steps, indent=2)}" if test_steps else ""
        code_prompt = PromptTemplate(
            template=code_template,
            input_variables=["title", "description", "acceptance_criteria", "steps_section", "url", "page"],
        )
        try:
            llm = get_llm(model_id)
            chain = code_prompt | llm | StrOutputParser()
            code_response = chain.invoke({
                "title": title,
                "description": description,
                "acceptance_criteria": "\n".join(acceptance_criteria),
                "steps_section": steps_section,
                "url": url,
                "page": page
            })
            cleaned_code = code_response.strip()
            code_lines = []
            in_code = False
            for line in cleaned_code.splitlines():
                if not in_code and (line.strip().startswith('import') or line.strip().startswith('from') or line.strip().startswith('def') or line.strip().startswith('@')):
                    in_code = True
                if in_code:
                    if line.strip().startswith('```') or line.strip().startswith('This code') or line.strip().startswith('The test') or line.strip().startswith('1.') or line.strip().startswith('*') or line.strip().startswith('# Run the test'):
                        break
                    code_lines.append(line)
            final_code = '\n'.join(code_lines).strip()
        except Exception as e:
            print(f"Error generating selenium code for story '{title}': {e}")
            final_code = ""
        scripts.append({"title": title, "script": final_code})
    return scripts 