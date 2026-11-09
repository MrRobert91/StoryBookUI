# Cuentee

AI-powered children's story generator for creating illustrated, multilingual tales.

[Live app](https://www.cuentee.com) | [Quick start](#quick-start) | [Architecture](#architecture) | [API](#api-endpoints)

## Screenshots

Reference screenshots stored in `docs/screenshots/`. They illustrate the UI and are not a live deployment check.

| Home | Public gallery |
|:-:|:-:|
| ![Home page](docs/screenshots/home.png) | ![Public gallery](docs/screenshots/gallery.png) |

| Story modal | Story type selection |
|:-:|:-:|
| ![Story viewer modal](docs/screenshots/story-viewer.png) | ![Story type selection](docs/screenshots/make-tale.png) |

| Open story creator | Guided story creator |
|:-:|:-:|
| ![Open story creator](docs/screenshots/open-story.png) | ![Guided story creator](docs/screenshots/guided-story.png) |

## Features

- Open story generation from a free-form prompt.
- Guided educational story generation with age group, protagonist, scientific topic, mission, visual style, language, and chapter count.
- AI-generated cover and chapter illustrations through OpenAI image models.
- Character consistency pipeline: the backend extracts character descriptions once, filters them per chapter, and injects the selected descriptions into image prompts.
- Multilingual UI and prompts for English, Spanish, French, German, Italian, and Portuguese.
- Supabase authentication with email/password and Google OAuth.
- Credit-based usage model with free credits and a `plus` plan refill job.
- Private account library, public gallery, story visibility controls, pagination, and story modal viewing.
- PDF generation and upload for generated stories.
- Optional real-time speech-to-text input through Speechmatics.

## Architecture

```text
Browser / Next.js app
  - Next.js 15 App Router
  - React 19, TypeScript, Tailwind CSS, Radix UI, Lucide icons
  - Supabase client auth and story queries
        |
        | REST + WebSocket
        v
FastAPI backend
  - /stories/generate-story-async
  - /stories/generate_guided_story_async
  - /tasks/{task_id}
  - /transcription/transcribe
        |
        | Celery task queue
        v
Celery worker + Redis
        |
        v
LangGraph story workflow
  1. Generate structured story with the configured Groq model
  2. Extract character visual descriptions
  3. Generate cover/chapter images with OpenAI image models
        |
        v
Supabase
  - PostgreSQL: stories, profiles
  - Auth: users and JWTs
  - Storage: images and PDFs
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, Radix UI, Lucide React |
| Backend | FastAPI, Python 3.11, Celery, Redis |
| Text AI | Groq via LangChain; default `openai/gpt-oss-120b`, configurable with `GROQ_MODEL` |
| Workflow | LangGraph |
| Image AI | OpenAI images: GPT Image 2.5 Flare / Sunburst, GPT Image 2, and legacy GPT Image / DALL·E models |
| Speech | Speechmatics WebSocket STT |
| Data/Auth | Supabase PostgreSQL, Auth, and Storage |
| PDFs | fpdf2 with bundled fonts |
| Deployment | Dockerfiles and Docker Compose configs for backend, worker, and frontend |

## Project Structure

```text
.
|-- api/                         FastAPI backend
|   |-- agents/                  LangGraph workflow, story schemas, image upload helpers
|   |-- celery_tasks/            Celery app and story generation task
|   |-- core/                    Environment config and auth dependencies
|   |-- prompts/                 Localized story, guided story, image, and character prompts
|   |-- routers/                 Stories, task status, and transcription routes
|   `-- services/                Supabase, user credits, and PDF services
|-- db/                          Base Supabase SQL schema
|-- docs/screenshots/            README screenshots captured from the live app
|-- frontend/                    Next.js application
|   |-- app/                     App Router pages
|   |-- components/              Forms, navigation, gallery, story modal/viewer, UI primitives
|   |-- hooks/                   Story generation polling hook
|   |-- lib/supabase/            Supabase clients and story/profile operations
|   `-- locales/                 UI translations
|-- tests/                       Pytest coverage for environment, story node, and image generation
|-- docker-compose.yml           Backend API and worker compose file
`-- .env.example                 Minimal local environment template
```

## Story Generation Flow

Open stories:

```text
Prompt + options
  -> POST /stories/generate-story-async
  -> Celery task
  -> LangGraph story generation
  -> character extraction
  -> image generation and upload
  -> PDF generation and upload
  -> Supabase story record
  -> client polls GET /tasks/{task_id}
```

Guided stories use the same Celery and LangGraph pipeline, but the backend first builds the story prompt from structured fields: age group, protagonist, scientific topic, mission, visual style, language, and chapter count.

## Character Consistency

The backend reuses character descriptions to improve consistency across images:

1. `character_extraction_node` reads the full generated story and creates concrete visual descriptions.
2. `_build_chapter_character_block` selects only the characters that appear in each chapter.
3. `make_image_prompt` appends the selected descriptions verbatim to the image prompt so they are not rewritten by another LLM call.

This is text-based guidance: the current pipeline does not pass reference images between chapters and does not guarantee identical characters. Preserve the verbatim description block when editing `api/agents/story_agent.py` or `api/agents/utils.py`.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20 (matching the frontend Dockerfile) and pnpm 10.28.2 (pinned in `frontend/package.json`)
- Redis for Celery
- Supabase project
- OpenAI and Groq API keys
- Optional: Speechmatics API key for voice input

### Environment variables

Copy `.env.example` to `.env` in the repository root and replace all example
credentials. The backend loads `.env` using `python-dotenv`; existing process or
container environment values take precedence. Never commit real credentials.
For local Next.js development, put the frontend variables in
`frontend/.env.local` (the root `.env` is not the frontend's env file).

#### Backend: credentials and connections

Configure these on both API and worker containers for a full deployment.
Credentials have no built-in usable defaults.

| Variable | Accepted value / default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for an account with access to the selected image model; required | Image generation. Missing or empty values fail during agent import. |
| `GROQ_API_KEY` | Groq API key; required | Story writing, character descriptions and illustration prompt writing. Missing or empty values fail during agent import. |
| `SUPABASE_URL` | Project API URL, e.g. `https://PROJECT_REF.supabase.co`; required | Auth, database and storage operations. |
| `SUPABASE_ANON_KEY` | The project's anon key; required | User-scoped Supabase client and JWT-authenticated image storage uploads. |
| `SUPABASE_SERVICE_ROLE_KEY` | The project's service-role key; required for the complete API/worker workflow | Server-side story persistence, PDF uploads and credit operations. Keep this backend-only. |
| `SUPABASE_PROJECT_REF` | Your project's reference string | Image S3 endpoint is derived as `https://REF.storage.supabase.co/storage/v1/s3`. Code defaults to `qvzbjollfgllkxxzlsoa`; explicitly set your own reference. |
| `REDIS_URL` | Redis connection URL; default `redis://localhost:6379/0` when missing or empty | Shared Celery broker, result backend and API startup connectivity check. Use `redis://USER:PASSWORD@HOST:PORT/DB` or a TLS `rediss://...` URL as required by the service. URL-encode credentials. Inside Docker, `localhost` means that container. |
| `STORAGE_BUCKET_NAME` | Existing Supabase image bucket name; default `cuentee_images` when unset | Image uploads. The PDF bucket is separately hardcoded to `cuentee_pdfs`; this variable does not change it. |
| `SPEECHMATICS_API_KEY` | Speechmatics API key; optional | Needed only for voice transcription; missing/empty values close the transcription WebSocket with code 1011. |

Create/configure the image and PDF storage buckets and their access policies in
Supabase. Image storage uses the user's JWT; PDF storage uses the service-role
client. Environment variables do not create buckets or database tables.
`SUPABASE_KEY` is present in the root Compose file but is **not read by the
backend** and cannot replace the anon and service-role variables above.

#### Backend: models and story defaults

| Variable | Accepted value / default | Behavior |
|---|---|---|
| `IMAGE_MODEL` | Exact options listed below; default `gpt-image-2-2026-04-21` when missing, empty or whitespace | Sole effective image-model selection. Trimmed and lowercased. Unsupported values fail at startup with the accepted names. Legacy per-story overrides are ignored. |
| `GROQ_MODEL` | A Groq model identifier available to your account and compatible with the workflow's JSON output; default `openai/gpt-oss-120b` when missing, empty or whitespace | Shared text model for stories, character extraction and illustration prompts. The application has no fixed allowlist. The legacy value `llama-3.3-70b-versatile` is replaced with the default and a warning; other explicit choices are sent unchanged. |
| `NUM_CHAPTERS` | Integer string; default `10` when unset | Prompt default when a workflow does not supply a chapter count. The open-story API request defaults to `3`; guided requests require a count. Request values take precedence. No environment range validation is implemented; use a positive integer. Blank/non-integer strings fail when prompts are imported. |

`IMAGE_MODEL` options accepted by `api/core/config.py`:

| Family | Environment values |
|---|---|
| GPT Image 2.5 Flare | `gpt-image-2.5-flare`, `gpt-image-2.5-flare-2026-09-08` |
| GPT Image 2.5 Sunburst | `gpt-image-2.5-sunburst`, `gpt-image-2.5-sunburst-2026-09-08` |
| GPT Image 2 | `gpt-image-2`, `gpt-image-2-2026-04-21` (default) |
| Earlier GPT Image | `gpt-image-1.5`, `gpt-image-1-mini`, `gpt-image-1` |
| Legacy DALL·E | `dall-e-3` / `dalle-3`, `dall-e-2` / `dalle-2` |

This table describes **code acceptance**, not guaranteed provider availability.
Legacy models may be retired; the API account must have access to the chosen
model. GPT Image 2.6 is not in this application's allowlist.

All GPT Image options use `quality="low"`, `size="1024x1024"`, `n=1` and base64
image uploads. DALL·E uses URL uploads, with `style="vivid"` for DALL·E 3.
There are currently **no** `IMAGE_QUALITY`, `IMAGE_SIZE`, image-provider or PDF
bucket environment settings. The image model does not select the text model.

For Flare, set:

```env
IMAGE_MODEL=gpt-image-2.5-flare
```

For Sunburst, set instead:

```env
IMAGE_MODEL=gpt-image-2.5-sunburst
```

In Sliplane or another Docker host, apply the selected value to **both API and
worker** (the worker generates images), save and redeploy/recreate both
containers. Deploy code supporting these model names first. Subsequent switches
only require changing the environment and recreating the containers, without a
source change or image rebuild. To return to the previous model, use
`IMAGE_MODEL=gpt-image-2-2026-04-21`.

Verify the worker startup logs contain:

```text
Image generation configuration: IMAGE_MODEL=gpt-image-2.5-flare
Worker configuration: Groq model=openai/gpt-oss-120b; deployment commit=...
```

The image-model value will reflect your selection. `SLIPLANE_COMMIT_HASH` is
provided by Sliplane for the deployment commit log, or defaults to `unknown`.
Changing environment variables does not rerun failed Celery tasks: generate a
new story to test the new configuration. A Groq `model_not_found` error concerns
`GROQ_MODEL`, not `IMAGE_MODEL` or the frontend.

#### Frontend

| Variable | Accepted value / default | Purpose |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project URL matching the backend; required for auth and library/gallery queries | Public Supabase endpoint. |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Matching project anon key; required for Supabase features | Public client key; never use the service-role key here. |
| `NEXT_PUBLIC_FASTAPI_URL` | Backend base URL, e.g. `http://localhost:8000` locally or `https://api.example.com` in production | Used by generation, task polling and transcription. Set explicitly: the shared generation hook has no default. Use a browser-reachable URL, without a trailing slash. |
| `NEXT_PUBLIC_SITE_URL` | Optional site origin, e.g. `https://www.cuentee.com` | OAuth callback redirect origin; falls back to the request origin when absent/empty. Match Supabase's configured redirect URLs. |

The frontend Dockerfile builds with placeholders and replaces the three required
`NEXT_PUBLIC_*` values in the compiled JavaScript at container startup. Set those
variables on the frontend container and recreate it when they change.
`NEXT_PUBLIC_SITE_URL` is read by the server-side auth callback and is not part
of that replacement list. For a local production build outside Docker, supply
public variables when running `pnpm build`.

`frontend/docker-compose.yml` supplies development placeholders for Supabase;
replace them before using real auth. It also declares `SUPABASE_SERVICE_ROLE_KEY`
and `SUPABASE_JWT_SECRET`, but the frontend application does not read either.
They are not required frontend settings.

#### Runtime, tracing and test settings

| Variable | Accepted value / default | Scope |
|---|---|---|
| `PORT` | TCP port number `1`–`65535`; frontend Docker default `3000`, worker health-server default `8000` | Frontend standalone server and worker startup script. Does not change FastAPI's port: its Docker command explicitly uses `8000`. Update port mappings/probes if changed. |
| `HOSTNAME` | Bind address for the frontend standalone server; Dockerfile sets `0.0.0.0` | The worker script separately sets its Celery hostname from the container hostname. |
| `NODE_ENV` | `development`, `production` or `test`; frontend Docker sets `production` | Next.js runtime mode. |
| `PYTHONPATH` | Python module search path; backend Dockerfiles set `/app` | Keeps the `api` package importable. Normally leave the Docker value unchanged. |
| `LANGSMITH_TRACING` | Optional `true` / `false`; legacy `LANGCHAIN_TRACING_V2` is also supported by the tracing SDK | Enable/disable LangSmith traces used by the decorated workflow and wrapped OpenAI client. |
| `LANGSMITH_API_KEY` | LangSmith key; legacy `LANGCHAIN_API_KEY` alias | Required for authenticated hosted tracing, not for story generation itself. |
| `LANGSMITH_PROJECT` | Optional project name; legacy `LANGCHAIN_PROJECT` alias | LangSmith trace destination project. |
| `RUN_REAL_API_TESTS` | Exactly `true` enables the opt-in real Groq test; otherwise skipped | Tests only. Can make billable provider calls. |

Tracing settings are consumed by the installed LangSmith/LangChain SDKs rather
than application config. These dependencies are not version-pinned in
`api/requirements.txt`; consult the installed SDK for additional tracing options.

### Redis Cloud database replacement

The API startup Redis check, Celery broker and Celery result backend share `REDIS_URL`.
For local development it defaults to `redis://localhost:6379/0`; hosted services
must supply their Redis Cloud URL as a deployment secret.

Use the endpoint and credentials of your active Redis Cloud database. The
`.env.redis-cloud.example` file records a connection template; it is not proof
that a hosted database is currently running. Replace its host, port and password
with your current connection details. Keep the full URL in deployment secrets
or an ignored local `.env` file.

When replacing a deleted database:

1. Replace the existing `REDIS_URL` secret in **both** the API and Celery worker
   services. Reusing the database name does not preserve its endpoint or password.
2. Restart/redeploy both services so they discard the previous connections.
3. Verify the API startup Redis check and worker broker connection succeed.
4. Generate a test story and verify that its task completes.

Merging this change does not update deployment secrets. The new database also
does not restore queued tasks or task results from the deleted instance.

### Backend and Worker

From the repository root, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
```

With `.env` configured, run each process in a separate terminal (activate the
virtual environment in the Python terminals):

```bash
# Terminal 1: Redis, unless using a hosted service
redis-server

# Terminal 2: HTTP API
uvicorn api.main:app --reload

# Terminal 3: worker; import the tasks module so generation is registered
celery -A api.celery_tasks.tasks worker --loglevel=info --pool=solo
```

The API listens on `http://localhost:8000`; interactive API docs are at `/docs`.
Redis and the worker must be reachable for queued story generation to complete.

### Frontend

Populate `frontend/.env.local` with the frontend variables, then:

```bash
cd frontend
npm install -g pnpm@10.28.2
pnpm install --frozen-lockfile
pnpm dev
```

The frontend runs at `http://localhost:3000`. The canonical dependency lockfile
for Docker is `frontend/pnpm-lock.yaml`; `pnpm-workspace.yaml` explicitly allows
build scripts for `sharp` and `unrs-resolver`.

```bash
pnpm build
pnpm start
```

The current Next.js config skips ESLint and TypeScript failures during builds;
a successful build alone does not establish that lint/type checks passed.

### Docker

The root Compose file builds API and worker; Redis and Supabase are external.
It explicitly forwards only a subset of the backend environment. Compose's
`.env` performs interpolation and **does not automatically inject every variable
into containers**. To pass the complete backend `.env` without editing the base
file, create a local `docker-compose.local.yml` (do not commit credentials):

```yaml
services:
  api:
    env_file:
      - .env
  worker:
    env_file:
      - .env
```

Then run from the repository root:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

This supplies missing backend settings such as `SUPABASE_ANON_KEY`,
`SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_PROJECT_REF`. Explicit `environment`
entries in the base Compose file take precedence over `env_file`.
Use a Redis URL reachable from containers, not the host's `localhost`.
After an `IMAGE_MODEL` change in `.env`, recreate with the same overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --force-recreate api worker
```

For separate Docker-host deployments, use `api/Dockerfile` with build context
`api/`, and `api/celery_tasks/Dockerfile.worker` with the repository root as build
context. The worker script starts an HTTP liveness server on `PORT` alongside
Celery; its `OK` response does not prove a story can be generated.

The frontend has a separate Dockerfile and Compose file. With frontend variables
in `frontend/.env.local`, run from the repository root:

```bash
docker compose --env-file frontend/.env.local -f frontend/docker-compose.yml up -d --build
```

Its `/api/health` endpoint checks frontend liveness without calling Supabase or
the backend. See [frontend/README.md](frontend/README.md) for Docker build details.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API liveness (`status: ok`); no per-request dependency check |
| `POST` | `/stories/generate-story-async` | Enqueue open story generation |
| `POST` | `/stories/generate_guided_story_async` | Enqueue guided story generation |
| `GET` | `/tasks/{task_id}` | Read Celery task status and result |
| `WS` | `/transcription/transcribe` | Speechmatics transcription WebSocket |

Story generation endpoints require a Supabase Bearer token and available credits.
The WebSocket uses a `token` query parameter and accepts `lang=en|es|fr|de|it|pt`
(default `en`). The task-status route currently has no authentication dependency.
The API attempts a Redis connection check at startup but still starts if Redis
is unavailable; `/` is not a readiness check for Redis, providers or storage.

## Database

The base schema in `db/schema.sql` defines:

- `stories`: generated story content, prompt, type, metadata, timestamps, and RLS policies for user-owned records.
- `profiles`: user credits, plan, plus refill timestamps, and signup trigger.

Additional SQL scripts in `frontend/scripts/` extend the schema with fields and
policies used by the UI, including usernames, story visibility and public gallery
access. `db/migration_metadata.sql` adds story metadata/type fields to existing
installations. Inspect the current database before applying scripts: several
scripts are alternative fixes, not a single ordered migration sequence.

The base schema grants three signup credits. The API's background job checks
`plus` profiles daily and adds ten credits when at least 30 days have elapsed
since the last refill or plan start. These values are code/SQL constants, not
environment options. Deployment database state can differ from the base schema.

## Tests

```bash
python -m pytest tests -q
```

The real Groq integration test is gated by `RUN_REAL_API_TESTS=true`:

```bash
RUN_REAL_API_TESTS=true python -m pytest tests/test_agents.py::test_real_story_generation_integration -v
```

The default suite uses fake credentials and mocked provider calls; it does not
verify production credentials, provider access, Redis connectivity or storage
permissions. Image tests inspect SDK HTTP payloads and base64/URL processing.
The current autouse fixture in `tests/conftest.py` replaces keys with test values,
so setting the opt-in flag alone is not a reliable live-provider check. A
credential-preserving test fixture/client is needed before using that test to
validate real access. For a deployed check, generate a new story and inspect
its images, PDF and saved record: image failures return empty URLs, and PDF or
database errors can be logged without changing the Celery task to `FAILURE`.

## License

No license file is currently included in this repository.
