#!/usr/bin/env python

import ollama

# #model="gemma3:1b",
response = ollama.generate(
    model='gpt-oss:20b-cloud',
    prompt="How many different types of cheese are there in France?"
)

print(response['response'])

