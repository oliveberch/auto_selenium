from langchain_ollama import OllamaLLM
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

DEFAULT_OLLAMA_MODEL = 'llama3.2'
DEFAULT_CLAUDE_MODEL = 'claude-sonnet-4-20250514'

def get_llm(provider, model_name=None, output_format=None):
    if provider == 'claude':
        model = model_name or DEFAULT_CLAUDE_MODEL
        return ChatAnthropic(model=model, temperature=0.2)
    elif provider == 'ollama' or provider == 'ollama-llama3':
        model = model_name or DEFAULT_OLLAMA_MODEL
        if output_format == 'json':
            return OllamaLLM(model=model, temperature=0.2, format="json")
        return OllamaLLM(model=model, temperature=0.2)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}") 