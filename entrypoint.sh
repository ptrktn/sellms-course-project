#!/bin/bash

# Start Ollama in the background
/bin/ollama serve &

# Record the process ID
pid=$!

# Give the server a moment to start
sleep 10

# Use MODEL_NAME from environment or default to gemma3:1b
MODEL=${MODEL_NAME:-gemma3:1b}
echo "Pulling model: $MODEL"
ollama pull "$MODEL"

# Wait for Ollama to finish
wait $pid

