AVAILABLE_MODELS = [
    {"name": "Claude Sonnet 4", "id": "claude"},
    {"name": "Ollama Llama3", "id": "ollama-llama3"}
]

# Simple in-memory state for the selected model
# In a multi-user environment, this would be handled by a session manager.
SELECTED_MODEL = {"id": "claude"} # Default to Claude 

# Simple in-memory state for app context
APP_CONTEXT = {
    "url": "",
    "pages": "",
    "username": "",
    "password": ""
} 