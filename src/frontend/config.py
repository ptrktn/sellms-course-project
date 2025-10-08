import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama-llm:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
DEFAULT_REGION = os.getenv("DEFAULT_REGION", "FR")
DEFAULT_HEMISPHERE = os.getenv("DEFAULT_HEMISPHERE", "northern")
