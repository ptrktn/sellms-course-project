import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama-llm:11434")
DEFAULT_REGION = os.getenv("DEFAULT_REGION", "france")
GEOLOCATE_ENABLED = os.getenv("GEOLOCATE_ENABLED", "true").lower() == "true"

