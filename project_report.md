# Project report

## Challenges faced during project execution

One of the earliest and most pivotal decisions was selecting the appropriate language model for the project. While using an API-based LLM like ChatGPT offered convenience, it also introduced potential cost concerns. Running the model locally emerged as a more sustainable and cost-effective alternative.

Among the local deployment options, GPT4All and Ollama were considered. Ollama ultimately proved more suitable, especially for a Dockerized setup, offering smoother integration and better containerization support.

Despite the web frontend being intentionally minimal, ensuring it behaved as intended required careful tuning. Even simple interfaces can demand nuanced adjustments to align with backend logic and user expectations.

Debugging Python Flask within a Dockerized environment presented its own set of hurdles. The lack of straightforward visibility into runtime behavior made troubleshooting more time-consuming, requiring extra attention to logging, container configuration, and development workflow.

## Key outcomes and achievements

The project successfully delivered a fully Dockerized environment, integrating an Ollama-powered backend with a responsive web frontend. This modular setup ensures maintainability and ease of deployment across varied systems.

A notable achievement was enabling the LLM to run locally within a development environment equipped with 16 GB of RAM. This setup proved sufficient for smooth operation, demonstrating that advanced language models can be effectively utilized without cloud dependency.

Performance optimization was also a key focus. By carefully trimming the prompt structure, response times were reduced to a swift 5–10 seconds, striking a balance between speed and quality.

Using the default model, Gemma3 1B, the system generates seemingly insightful and context-aware responses, particularly well-suited to enhancing the experience of pairing wine and cheese. This opens the door to more enjoyable and personalized culinary exploration, guided by AI with a taste for nuance.

## Leveraging large language models: approach and implementation

Large Language Models (LLMs), particularly GPT-5, played a pivotal role in shaping the project from its earliest stages. The initial software requirements were generated using GPT-5, providing a broad and imaginative foundation. These requirements were then manually refined—mostly trimmed down—to better align with practical constraints and project scope.

For the web frontend, GitHub Copilot was employed to draft a prototype using Python Flask. This accelerated development and offered a functional starting point for further customization.

Throughout the project, GPT-5 continued to serve as a reliable assistant, offering quick solutions to various technical details. Whether it was clarifying syntax, suggesting function usage, or resolving minor implementation issues, the model helped maintain momentum and reduce friction.

Even this report has been drafted with the assistance of GPT-5, ensuring clarity, consistency, and a touch of creative polish.s

## Potential next steps

This project is not intended to be a finished, production-ready application. Rather, it serves as a functional prototype that demonstrates the feasibility of running a local LLM-powered pairing system. With further development, it could evolve into a full-fledged application by incorporating a more feature-rich frontend.

Future enhancements might include support for user preferences—such as selecting specific types of wine, cheese, or even regional pairings. These additions would allow for a more personalized and engaging experience, transforming the system from a technical demonstration into a delightful tool for culinary exploration.
