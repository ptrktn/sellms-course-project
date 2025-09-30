# Introduction

This system is a locally hosted, containerized web application that generates season- and location-aware wine and cheese recommendations using an Ollama-backed LLM. It blends automatic context (current date/time and IP-based geolocation) with manual overrides, prioritizing privacy and resilience.

- **Purpose:** Deliver delightful, culturally relevant pairings by interpreting seasonal cues and regional availability, while remaining fully controllable and reproducible in a local environment.
- **Scope:** Includes a Dockerized LLM service (Ollama), a containerized web frontend, an API layer, configurable context derivation, secure logging, monitoring hooks, and testable, deterministic behavior with fallbacks.

---

# Overall description

## Product perspective

- **Architecture:** Two primary containers: an Ollama LLM engine and a web frontend (with API). Communication occurs over an internal Docker network, with explicit health checks, resource limits, and persistent storage volumes for LLM models and app state.
- **Context sources:** Manual inputs for season and location, plus automatic derivation via system clock and IP-based geolocation. Users can toggle or blend these sources.
- **Operational model:** Local-first, offline-capable where possible. Minimal external dependencies beyond optional geolocation. Configuration via environment variables and mounted volumes.

## Product functions

- **Pairing generation:** Produce wine + cheese recommendations with rationale, regional fit, seasonal mood, and serving notes.
- **Context derivation:** Determine season from current date/time and location from IP geolocation; allow user overrides at any time.
- **Explainability:** Provide brief justifications (style, region, climate cues) and alternates (budget, availability).
- **Persisted settings:** Save preferred regions, dietary constraints, and style preferences locally.
- **Observability:** Log requests, prompt parameters, and model metadata with redaction; expose health/metrics endpoints.
- **Reliability:** Graceful fallbacks when geolocation fails or LLM is unavailable; deterministic test modes.

## User characteristics

- **Casual users:** Prefer simple inputs and clear recommendations with minimal configuration.
- **Power users:** Want parameterization (model selection, temperature, region biases), reproducibility, and control over privacy and data flows.
- **Operators:** Need deployment clarity, resource controls, health checks, logs, and backup/restore of local state.

---

# Specific requirements

## System architecture

- **AR-1:** The system SHALL consist of two containers: ollama-llm and web-frontend, connected via an internal Docker network.
- **AR-2:** The ollama-llm container SHALL persist model files via a mounted volume to avoid re-downloads.
- **AR-3:** The web-frontend container SHALL expose HTTP endpoints to users and communicate with ollama-llm over the internal network.
- **AR-4:** Both containers SHALL define health checks, resource limits (CPU/memory), and restart policies.
- **AR-5:** The system SHOULD support docker-compose for single-command setup.

## Functional requirements

- **FR-1:** The system SHALL accept manual inputs for season and location.
- **FR-2:** The system SHALL automatically derive season from current date/time and location from IP-based geolocation when enabled.
- **FR-3:** The system SHALL allow users to toggle between manual and automatic context at any time.
- **FR-4:** The system SHALL generate wine + cheese recommendations with justification, regional fit, seasonal notes, and serving suggestions.
- **FR-5:** The system SHALL provide at least three pairing alternatives (standard, budget, adventurous) when requested.
- **FR-6:** The system SHALL allow user preferences (region bias, wine styles, cheese categories, dietary constraints) to influence output.
- **FR-7:** The system SHALL cache recent contexts to speed repeat queries within a configurable window.
- **FR-8:** The system SHALL provide a deterministic test mode by fixing seed, temperature, and context inputs.

## LLM integration and prompt design

- **LLM-1:** The system SHALL run Ollama locally and support configurable model selection (e.g., via environment variable).
- **LLM-2:** The system SHALL expose parameters (temperature, top_p, max_tokens) and document defaults.
- **LLM-3:** The prompt template SHALL incorporate season, location, regional cuisines, user preferences, and tone instructions.
- **LLM-4:** The system SHALL implement guardrails to avoid unsafe content and non-actionable recommendations (e.g., unavailable products without alternatives).
- **LLM-5:** The system SHOULD support short/long response modes and JSON output for structured rendering.

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

- **REQ-1:** Input schema SHALL validate season (e.g., spring, summer, autumn, winter) and location (ISO country, region, or city).
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
| OLLAMA_MODEL | "llama2" | Selected LLM model | ollama-llm |
| OLLAMA_PORT | 11434 | LLM service port | ollama-llm |
| APP_PORT | 8080 | Frontend HTTP port | web-frontend |
| GEOLOCATE_ENABLED | true | Toggle IP geolocation | web-frontend |
| DEFAULT_REGION | "" | Region bias fallback | web-frontend |

- **CFG-1:** The system SHALL read configuration from environment variables and an optional config file.
- **CFG-2:** Sensitive values (tokens) SHALL be excluded or stored via secrets mechanisms.

## Containerization and deployment

- **CD-1:** Images SHALL be reproducible, pinned to specific base versions, and built via Dockerfiles.
- **CD-2:** Volumes SHALL persist: models (ollama), app state (preferences), and logs.
- **CD-3:** Networking SHALL use a private bridge; LLM port SHOULD be internal-only unless explicitly exposed.
- **CD-4:** Health checks SHALL verify LLM readiness (model loaded) and API responsiveness.
- **CD-5:** Startup order SHALL ensure ollama-llm is ready before serving recommendation requests.

## Security and privacy

- **SEC-1:** No personal data SHALL be transmitted to third parties by default; geolocation SHOULD use IP-only with minimal retention.
- **SEC-2:** Logs SHALL redact IPs and any identifiers unless explicitly enabled for diagnostics.
- **SEC-3:** TLS termination SHOULD be supported when deployed behind a reverse proxy.
- **SEC-4:** CSRF protection and input validation SHALL be implemented for API endpoints.
- **SEC-5:** The system SHALL provide a clear privacy toggle disabling geolocation and analytics.

## Performance, reliability, and scalability

- **PERF-1:** P95 recommendation latency SHOULD be under 1.5s on a typical local setup; configurable timeouts and fallbacks MUST exist.
- **PERF-2:** The system SHALL support concurrent requests with a configurable worker pool and backpressure.
- **REL-1:** On LLM errors/timeouts, the system SHALL provide cached/previous recommendations or a graceful message with retry.
- **REL-2:** The system SHALL handle geolocation failures by falling back to manual location or DEFAULT_REGION.
- **SCAL-1:** Stateless API design SHOULD allow horizontal scaling; state (preferences) stored locally with export/import.

## Logging and observability

- **OBS-1:** Structured logs SHALL include request id, context source, model params, and outcomes; sensitive data redacted.
- **OBS-2:** Metrics endpoint SHALL expose request counts, latency histograms, error rates, and cache hits.
- **OBS-3:** A debug mode SHALL surface prompt, parameters, and derivation details; disabled by default.

## Error handling and edge cases

- **ERR-1:** If season is ambiguous (e.g., equinox), the system SHALL choose nearest season with confidence metadata and provide alternatives.
- **ERR-2:** If location is unknown or IP-derived region conflicts with user preferences, the system SHALL ask for confirmation or apply a documented precedence rule.
- **ERR-3:** If model download/availability fails, the system SHALL present an actionable message and degraded mode without LLM (static recommendations, if configured).
- **ERR-4:** Network partition between containers SHALL trigger retries with exponential backoff and a clear status.

## Internationalization and accessibility

- **I18N-1:** The frontend SHALL support multiple languages; default to system locale, override via user settings.
- **I18N-2:** Units and naming conventions SHALL adapt to region (e.g., local cheese names).
- **A11Y-1:** UI SHALL meet WCAG AA for color contrast and keyboard navigation.

## Testing and acceptance criteria

- **TST-1:** Unit tests SHALL cover context derivation, prompt assembly, and schema validation.
- **TST-2:** Integration tests SHALL verify LLM interaction, fallbacks, and health checks.
- **TST-3:** Deterministic mode tests SHALL produce repeatable outputs with fixed seeds and parameters.
- **ACC-1:** A user can generate at least one valid pairing with rationale using automatic context within 2s P95 latency on reference hardware.
- **ACC-2:** Manual overrides SHALL supersede automatic context immediately and persist for the session.
- **ACC-3:** Geolocation disabled mode SHALL function fully with manual inputs and no external calls.

## Frontend requirements

- **FE-1:** Provide inputs for manual season/location and a toggle for automatic context.
- **FE-2:** Display recommendations with rationale, alternates, and simple filters (budget, adventurous).
- **FE-3:** Surface derivation metadata (how season/location was computed) and confidence.
- **FE-4:** Provide a preferences panel with clear defaults and reset/export options.
- **FE-5:** Show status indicators for LLM readiness, cache usage, and error notifications without leaking sensitive details.


