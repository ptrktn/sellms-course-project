#!/bin/bash

# Start Ollama in the background
/bin/ollama serve &

# Record the process ID
pid=$!

# Give the server a moment to start
sleep 10

# Use OLLAMA_MODEL from environment or default to gemma3:1b
MODEL=${OLLAMA_MODEL:-gemma3:1b}

# Check if the model is already pulled
if ! ollama list | grep -q "$MODEL"; then
  echo "Model $MODEL not found locally. Pulling now..."
  ollama pull "$MODEL"
else
  echo "Model $MODEL already exists. Skipping pull."
fi

# Wait for Ollama to finish
wait $pid

