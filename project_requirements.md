# Introduction

This system is a locally hosted, containerized web application that generates season- and location-aware wine and cheese recommendations using an Ollama-backed LLM. It blends automatic context (current date/time and IP-based geolocation) with manual overrides, prioritizing privacy and resilience.

- **Purpose:** Deliver delightful, culturally relevant pairings by interpreting seasonal cues and regional availability, while remaining fully controllable and reproducible in a local environment.
- **Scope:** Includes a Dockerized LLM service (Ollama) and a containerized web frontend.

---

# Overall description

## Product perspective

- **Architecture:** Two primary containers: an Ollama LLM engine and a web frontend (with API). Communication occurs over an internal Docker network, and persistent storage volumes for LLM models.
- **Context sources:** Manual inputs for season and location, plus automatic derivation via system clock and IP-based geolocation. Users can toggle or blend these sources.
- **Operational model:** Local-first, offline-capable. Minimal external dependencies beyond optional geolocation. Configuration via environment variables.

## Product functions

- **Pairing generation:** Produce wine and cheese recommendations with rationale, regional fit, seasonal mood, and serving notes.
- **Context derivation:** Determine season from current date/time and location from IP geolocation; allow user overrides at any time.
- **Explainability:** Provide brief justifications (style, region, climate cues).

---

# Specific requirements

## System architecture

- **AR-1:** The system SHALL consist of two containers: ollama-llm and web-frontend, connected via an internal Docker network.
- **AR-2:** The ollama-llm container SHALL persist model files via a mounted volume to avoid re-downloads.
- **AR-3:** The web-frontend container SHALL expose HTTP endpoints to users and communicate with ollama-llm over the internal network.
- **AR-4:** Both containers SHALL define restart policies.
- **AR-5:** The system SHALL support docker-compose for single-command setup.

## Functional requirements

- **FR-1:** The system SHALL accept manual inputs for season and location.
- **FR-2:** The system SHALL automatically derive season from current date/time and location from IP-based geolocation when user has not provided those parameters.
- **FR-3:** The system SHALL allow users to toggle between manual and automatic context at any time.
- **FR-4:** The system SHALL generate wine and cheese recommendations with justification, regional fit, seasonal notes, and serving suggestions.


## LLM integration and prompt design

- **LLM-1:** The system SHALL run Ollama locally and support configurable model selection (e.g., via environment variable).
- **LLM-2:** The system SHALL expose parameters (temperature, top_p, max_tokens) and document defaults.
- **LLM-3:** The prompt template SHALL incorporate season and location instructions.
- **LLM-4:** The system SHALL implement guardrails to avoid unsafe content and non-actionable recommendations (e.g., unavailable products without alternatives).

## API requirements

### REST endpoints

| Endpoint | Method | Purpose | Auth | Notes |
|---|---|---|---|---|
| /api/recommendations | POST | Generate pairing from context | Optional | Accepts manual inputs; returns primary + alternates |
| /api/context/auto | GET | Return auto-derived season and location | None | Includes derivation metadata and confidence |
| /api/context/manual | POST | Set manual season/location | Optional | Persists for session/user |
| /api/preferences | GET/PUT | Read/update user preferences | Optional | Stored locally; schema validated |
| /api/health | GET | Health status | None | Reports LLM and frontend health |
| /api/metrics | GET | Metrics | Restricted | Request counts, latency, errors |

> Sources: Internal architecture; no external citations.

### Request/response contracts

- **REQ-1:** Input schema SHALL validate season (e.g., spring, summer, autumn, winter) and location (ISO 3166-1 country code).
- **REQ-2:** Output schema SHALL include pairing items, rationale, alternates, and metadata (model, parameters, context).

## Data model

- **DM-1:** Preference object: wine styles, cheese categories, region bias, budget range, dietary constraints, response verbosity.
- **DM-2:** Context object: season, location (country/region/city), derived flags, timestamp, confidence, source.
- **DM-3:** Recommendation object: wine, cheese, region, notes, serving suggestions, availability hints, alternates.
- **DM-4:** Logs metadata: request id, user id (optional), model, parameters, latency, errors, redaction flags.

## Configuration

### Environment variables

| Variable | Default | Description | Scope |
|---|---|---|---|
| OLLAMA_MODEL | "gemma3:1b" | Selected LLM model | ollama-llm |
| OLLAMA_PORT | 11434 | LLM service port | ollama-llm |
| APP_PORT | 8080 | Frontend HTTP port | web-frontend |
| GEOLOCATE_ENABLED | true | Toggle IP geolocation | web-frontend |
| DEFAULT_REGION | "" | Region bias fallback | web-frontend |

- **CFG-1:** The system SHALL read configuration from environment variables and an optional config file.
- **CFG-2:** Sensitive values (tokens) SHALL be excluded or stored via secrets mechanisms.

## Containerization and deployment

- **CD-1:** Images SHALL be reproducible, pinned to specific base versions, and built via Dockerfiles.
- **CD-2:** Volumes SHALL persist: models (ollama).
- **CD-3:** Startup order SHALL ensure ollama-llm is started before serving recommendation requests.

## Security and privacy

- **SEC-1:** No personal data SHALL be transmitted to third parties by default; geolocation SHOULD use IP-only with minimal retention.


## Error handling and edge cases

- **ERR-1:** If season is ambiguous (e.g., equinox), the system SHALL choose nearest season with confidence metadata and provide alternatives.
- **ERR-2:** If location is unknown or IP-derived region conflicts with user preferences, the system SHALL ask for confirmation or apply a documented precedence rule.
- **ERR-3:** If model download/availability fails, the system SHALL present an actionable message and degraded mode without LLM (static recommendations, if configured).
- **ERR-4:** Network partition between containers SHALL trigger retries with exponential backoff and a clear status.

## Frontend requirements

- **FE-1:** Provide inputs for manual season/location and a toggle for automatic context.
- **FE-2:** Display recommendations with rationale.
- **FE-3:** Surface derivation metadata (how season/location was computed) and confidence.

