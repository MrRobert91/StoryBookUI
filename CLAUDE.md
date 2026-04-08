# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Cuentee — AI-powered children's story generator. Next.js 15 frontend + FastAPI backend + Celery/Redis workers, orchestrated via a LangGraph workflow that calls Groq (LLaMA 3.3-70B) for text and OpenAI (DALL-E 3 / GPT-Image) for illustrations. Data and auth live in Supabase (Postgres + S3 storage).

## Commands

### Run the stack (Docker)
```bash
docker-compose up --build
# Frontend: http://localhost:3000   API docs: http://localhost:8000/docs
```

### Run locally
```bash
# Backend — three terminals:
pip install -r api/requirements.txt
redis-server                                         # 1
uvicorn api.main:app --reload                        # 2
celery -A api.celery_tasks.app worker --loglevel=info  # 3

# Frontend:
cd frontend && npm install && npm run dev
```
`npm run lint` / `npm run build` for frontend checks. The `worker` process is required for anything that calls `/stories/*` — the API enqueues Celery tasks and returns a task id; without the worker, generation hangs forever.

### Tests
```bash
pytest                       # full suite
pytest tests/test_agents.py::test_name -v   # single test
```
`tests/conftest.py` injects fake API keys via `monkeypatch` and provides a `mock_story_agent` fixture that returns a real `Story` object (needed to pass the `isinstance(story, Story)` check inside the workflow node).

### LLM evaluation (safety)
Two-step offline flow — generates stories directly via the LangGraph workflow (no Celery, no API) and then scores them with an LLM-as-a-judge:
```bash
# 1. Generate — --skip-images is the default, keeps the run cheap
python -m llm_evaluation.safety.safety_evals.test_generator.generate_test_stories \
  --type both --count 5

# 2. Evaluate the JSON output from step 1
python -m llm_evaluation.safety.safety_evals.test_generator.evaluate_from_file \
  --input llm_evaluation/safety/safety_evals/test_generator/results/story_generation/eval_stories_YYYYMMDD_HHMMSS.json
```
Quality gate: ≥90% of stories must score ≥2 (on a 0–3 scale). The script exits non-zero on failure, so this is suitable for CI.

A LangSmith-backed variant (`scripts/evaluate_safety.py --project <name> --limit 50`) pulls recent successful runs from LangSmith instead of a file.

## Architecture

### Request path (story generation)
```
Client → FastAPI router (/stories/generate-story-async or /stories/generate_guided_story_async)
       → enqueue Celery task (generate_story_task) in Redis
       → worker picks up task → invokes LangGraph `graph` in api/agents/story_agent.py
       → result saved to Supabase; client polls GET /tasks/{task_id} until SUCCESS/FAILURE
```
All story endpoints require a Supabase JWT (Bearer token) and decrement the user's credit balance via `api/core/dependencies.py`.

### LangGraph workflow (`api/agents/story_agent.py`)
Three sequential nodes sharing a `StoryState` TypedDict (see `api/agents/utils.py`):

1. **`story_generation_node`** — Groq LLaMA 3.3-70B with `with_structured_output(Story, method="json_mode")` to emit a Pydantic `Story` directly. System prompt comes from `get_story_system_prompt(lang, num_chapters)`.
2. **`character_extraction_node`** — second Groq call that reads the full story and returns a character list with concrete visual specs (species, hair, eyes, clothing, etc.). The result is stored in `story.metadata["characters"]` and in state as `character_descriptions`.
3. **`image_generation_node`** — for the cover and each chapter, calls `make_image_prompt` (which invokes the image-prompt LLM) and then `generate_image` (OpenAI), uploading the output to Supabase S3 under the authenticated user's JWT.

### Character consistency — the critical invariant
This is the part that surprises. Character descriptions are **never** passed through the image-prompt LLM. `make_image_prompt` generates the scene prompt from the chapter text and visual style, then `_build_chapter_character_block` prepends a verbatim character block — so the bytes describing each character are byte-identical across every chapter. For each chapter, only characters whose name (or name tokens ≥3 chars, case-insensitive, word-boundary match via `_name_variants`) actually appear in the chapter text are included. When editing this pipeline, preserve the "append verbatim, never LLM-rewrite" property or character consistency across chapters will regress.

### State handoff for image generation
`image_generation_node` calls `set_user_context(user_id, jwt_token, story_id)` which stores the JWT in module-level globals in `api/agents/utils.py` and caches a boto3 S3 client keyed by that token. This means the node is **not thread-safe across users** — Celery's per-task worker concurrency model is what keeps it safe. Don't call the graph directly from request handlers, and don't share a worker process across users without resetting the context.

### Prompt localization
All prompts (story system prompt, image prompt, character extraction, guided builder) are localized across 6 languages in `api/prompts/translations/`. Getter functions in `api/prompts/story_prompts.py` and `guided_story_prompts.py` take a `lang` argument; always route language through them rather than hardcoding English.

### Frontend generation UX
`frontend/hooks/use-story-generation.ts` owns the end-to-end flow: POST to the async endpoint, poll `/tasks/{id}`, and update UI state. The two creator pages (`app/make-tale/open` and `app/make-tale/guided`) use different form components (`tale-generator.tsx` and `guided-tale-generator.tsx`) but share the same hook and backend workflow — the only difference is how the prompt is built before being sent.

### Data model
`db/schema.sql` defines `stories` (content stored as JSON in a TEXT column, plus a `metadata` JSONB for language/style/characters/etc.) and `profiles` (credits, plan, refill timestamps). Row-level security is enabled; the service-role key is only used from `api/main.py`'s background credit-refill loop and from Celery tasks that write on behalf of users.

## Environment

Required: `OPENAI_API_KEY`, `GROQ_API_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_PROJECT_REF`, `REDIS_URL`, `STORAGE_BUCKET_NAME`.
Optional: `SPEECHMATICS_API_KEY` (voice input), `LANGCHAIN_TRACING_V2` + `LANGCHAIN_API_KEY` (LangSmith), `IMAGE_MODEL` (one of `dalle-3`, `dalle-2`, `gpt-image-1`, `gpt-image-1-mini`, `gpt-image-1.5`).

`api/agents/utils.py` raises `EnvironmentError` at import time if `OPENAI_API_KEY` or `SUPABASE_ANON_KEY` is missing, so any test or script that imports the agents package must set these (the test suite does this via `conftest.py`).
