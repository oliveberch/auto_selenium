import json
import datetime
from app.core.llm_utils import get_llm, PromptTemplate, StrOutputParser

def generate_user_stories(requirements, model_id, app_url, app_pages, username, password):
    """
    Generates user stories in the required template from functional requirements using an LLM.
    Adds app_url, app_pages, username, and password to the prompt for technical context.
    """
    template = '''
    You are an expert agile analyst. Given the following functional requirements and application context:
    Requirements:
    {requirements}
    App URL: {app_url}
    App Pages: {app_pages}
    Username: {username}
    Password: {password}

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
              "dependencies": ["story_id_1", "story_id_2"] (optional),
              "page": "Relevant page(s) for this story",
              "url": "Relevant URL(s) for this story"
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
    - Add technical details (pages, URLs) for each story.
    - Do not include any explanation, only output valid JSON.
    '''

    prompt = PromptTemplate(
        template=template,
        input_variables=["requirements", "app_url", "app_pages", "username", "password"],
    )

    try:
        llm = get_llm(model_id, output_format='json')
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
            "requirements": requirements,
            "app_url": app_url,
            "app_pages": app_pages,
            "username": username,
            "password": password
        })
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

def match_requirements_to_features(requirements, features, model_id):
    """
    Uses LLM to match user requirements to extracted codebase features.
    Returns a list of matches with match_score (0-1).
    """
    template = '''
    You are an expert software analyst. Given the following user requirements and extracted codebase features, match each requirement to the most relevant feature(s) in the codebase. For each match, provide a match_score (0-1) indicating confidence.

    Requirements:
    {requirements}

    Features:
    {features}

    Output a JSON array of objects with:
      - requirement (string)
      - feature (object)
      - match_score (float, 0-1)
    Only output valid JSON, no explanation.
    '''
    prompt = PromptTemplate(
        template=template,
        input_variables=["requirements", "features"],
    )
    try:
        llm = get_llm(model_id, output_format='json')
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
            "requirements": requirements,
            "features": features
        })
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        matches = json.loads(cleaned_response)
        return matches
    except Exception as e:
        print(f"Error matching requirements to features: {e}")
        return []

def _generate_story_from_feature(feature: dict, model_id: str, app_context: dict) -> dict:
    """Uses LLM to generate a user story from a single codebase feature."""
    template = '''
    You are a test analyst. Given the following codebase feature and application context, write a concise user story in JSON format to test its functionality.
    - The story should include a title, a description (in the 'As a user...' format), and at least one acceptance criterion.
    - The `page` should be the feature's location.
    - The `url` should be the application's base URL, as it will be used for testing.

    Application Context:
    Base URL: {app_url}

    Codebase Feature:
    {feature}

    Output only the JSON object for the story (no preamble or surrounding text). Example:
    {{
      "title": "Verify Login Form Submission",
      "description": "As a user, I want to submit the login form to authenticate.",
      "acceptance_criteria": ["The form submits successfully with valid credentials."],
      "page": "src/login.html",
      "url": "{app_url}"
    }}
    '''
    prompt = PromptTemplate(template=template, input_variables=["feature", "app_url"])
    try:
        llm = get_llm(model_id, output_format='json')
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
            "feature": json.dumps(feature),
            "app_url": app_context.get("url", "")
        })
        
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        
        story = json.loads(cleaned_response)
        # Ensure essential keys are present
        story.setdefault("title", "Untitled Feature Test")
        story.setdefault("description", f"Test for feature at {feature.get('location')}")
        story.setdefault("acceptance_criteria", ["The feature works as expected."])
        story.setdefault("url", app_context.get("url", "")) # Ensure URL is set
        return story
    except Exception as e:
        print(f"Error generating story from feature: {e}")
        return None

def create_comprehensive_test_plan(requirements: str, features: list, model_id: str, app_context: dict) -> dict:
    """
    Orchestrates the creation of a comprehensive test plan by:
    1. Matching requirements to features.
    2. Generating stories from requirements, enriching them with matched feature data.
    3. Generating stories for unmatched features.
    """
    # 1. Match requirements to features
    matches = match_requirements_to_features(requirements, features, model_id)
    # Ensure matches is a list of dicts with expected keys
    matched_feature_locations = {
        match['feature']['location']
        for match in matches
        if isinstance(match, dict) and 'feature' in match and isinstance(match.get('feature'), dict) and match.get('feature').get('location') and match.get('match_score', 0) > 0.5
    }
    
    # 2. Generate stories from requirements (will be enriched later)
    # The existing `generate_user_stories` works well for this part.
    story_backlog = generate_user_stories(
        requirements, model_id, 
        app_context['url'], app_context['pages'], 
        app_context['username'], app_context['password']
    )
    
    # 3. Generate stories for unmatched features
    unmatched_features = [f for f in features if f['location'] not in matched_feature_locations]
    
    unmatched_stories = []
    for feature in unmatched_features:
        story = _generate_story_from_feature(feature, model_id, app_context)
        if story:
            unmatched_stories.append(story)
            
    # 4. Combine the story lists
    if story_backlog and 'backlog' in story_backlog:
        if unmatched_stories:
            # Add a new epic for "Existing Feature Tests"
            story_backlog['backlog'].append({
                "epic": "Existing Feature Tests",
                "description": "Tests generated from existing codebase features not covered by requirements.",
                "stories": unmatched_stories
            })
        
        # Simple enrichment: add feature info to description of matched stories (can be improved)
        for epic in story_backlog.get('backlog', []):
            for story in epic.get('stories', []):
                for match in matches:
                    if (
                        isinstance(match, dict)
                        and 'requirement' in match
                        and isinstance(match['requirement'], str)
                        and 'feature' in match
                        and isinstance(match['feature'], dict)
                    ):
                        if story['title'].lower() in match['requirement'].lower():
                            story['description'] += f"\n\n[Codebase reference: {match['feature'].get('type', 'Unknown')} at {match['feature'].get('location', 'Unknown')}]"
                            break  # Move to next story once enriched
    else:
        # Handle case where no requirements were provided, but features were found
        story_backlog = {
            "backlog": [{
                "epic": "Existing Feature Tests",
                "description": "Tests generated from existing codebase features.",
                "stories": unmatched_stories
            }],
            "metadata": {}
        }

    return story_backlog 