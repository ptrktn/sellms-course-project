#!/bin/bash

# Start Ollama in the background
/bin/ollama serve &

# Record the process ID
pid=$!

# Give the server a moment to start
sleep 10

# Use OLLAMA_MODEL from environment or default to gemma3:1b
MODEL=${OLLAMA_MODEL:-gemma3:1b}
echo "Pulling model: $MODEL"
ollama pull "$MODEL"

# Wait for Ollama to finish
wait $pid

