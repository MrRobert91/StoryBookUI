<p align="center">
  <img src="frontend/public/icon.svg" alt="Cuentee Logo" width="80" />
</p>

<h1 align="center">Cuentee — AI-Powered Children's Story Generator</h1>

<p align="center">
  <strong>Create magical, illustrated stories for children in seconds using AI.</strong><br/>
  Personalized tales with consistent characters, educational themes, and beautiful illustrations.
</p>

<p align="center">
  <a href="https://www.cuentee.com">Live App</a> · 
  <a href="#quick-start">Quick Start</a> · 
  <a href="#architecture">Architecture</a> · 
  <a href="#llm-evaluation">Evaluation</a>
</p>

---

## Screenshots

| Home Page | Story Type Selection |
|:-:|:-:|
| ![Home](docs/screenshots/home.png) | ![Make Tale](docs/screenshots/make-tale.png) |

| Open Story Creator | Guided Story Creator |
|:-:|:-:|
| ![Open Story](docs/screenshots/open-story.png) | ![Guided Story](docs/screenshots/guided-story.png) |

| Story Viewer | Gallery |
|:-:|:-:|
| ![Story Viewer](docs/screenshots/story-viewer.png) | ![Gallery](docs/screenshots/gallery.png) |

> **Note:** To add screenshots, save them in `docs/screenshots/` with the names shown above.

---

## Features

### Story Generation
- **Two creation modes**: Free-form (open) and structured (guided) story generation
- **Guided stories** include educational scientific topics, age-appropriate missions, and custom protagonists
- **6 visual styles**: Cartoons, Watercolor, 3D Animation, Anime, Child Crayons, Editorial Illustration
- **Configurable chapters** (3–10 per story)
- **Voice input**: Dictate your story idea via real-time speech-to-text (Speechmatics)

### AI-Powered Illustrations
- **Automatic image generation** for cover and every chapter using DALL-E 3 / GPT-Image
- **Character Consistency System**: Extracts all characters after story generation and injects identical visual descriptions into every image prompt — no LLM reformulation, fully deterministic
- **Per-chapter filtering**: Only characters present in each chapter are included in its image prompt

### Multilingual
- **6 languages**: English, Spanish, French, German, Italian, Portuguese
- Full localization of UI, story prompts, topics, missions, and visual style descriptions

### User System
- **Authentication** via Supabase Auth (email/password, OAuth)
- **Credit-based** usage model (Free: 3 credits, Plus: auto-refill 10/month)
- **Story gallery** with history, search, and pagination
- **PDF export** with OpenDyslexic font for accessibility

### Observability & Evaluation
- **LangSmith tracing** across the full generation pipeline
- **Safety evaluation framework** with LLM-as-a-judge (quality gate: 90% safe ratio)
- **Test story generator** for automated evaluation without API costs

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Next.js 15)                        │
│  App Router · React 19 · TailwindCSS · Radix UI · Supabase Auth    │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ REST API + WebSocket
┌──────────────────────────────▼──────────────────────────────────────┐
│                        BACKEND (FastAPI)                            │
│  /stories/generate-story-async    POST  → Celery task               │
│  /stories/generate_guided_story   POST  → Celery task               │
│  /tasks/{task_id}                 GET   → Poll status                │
│  /transcription/transcribe        WS    → Speechmatics STT          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                     CELERY WORKER (Redis)                           │
│  Picks up generation tasks → Invokes LangGraph → Saves to DB       │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                   LANGGRAPH WORKFLOW (3 nodes)                      │
│                                                                     │
│  ┌─────────────────┐   ┌──────────────────┐   ┌─────────────────┐  │
│  │ Story Generation │──▶│ Character Extract │──▶│ Image Generation│  │
│  │  (Groq LLaMA 3) │   │  (Groq LLaMA 3)  │   │ (DALL-E 3/GPT) │  │
│  └─────────────────┘   └──────────────────┘   └─────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│                        DATA LAYER                                   │
│  Supabase PostgreSQL (stories, profiles)                            │
│  Supabase S3 Storage (images, PDFs)                                 │
│  LangSmith (traces, evaluations)                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 15, React 19, TypeScript, TailwindCSS, Radix UI, Lucide Icons |
| **Backend** | FastAPI, Python 3.11, Celery, Redis |
| **AI — Text** | Groq API (LLaMA 3.3-70B-Versatile) via LangChain |
| **AI — Images** | OpenAI (DALL-E 3, GPT-Image-1, GPT-Image-1-mini, GPT-Image-1.5) |
| **AI — Orchestration** | LangGraph (StateGraph workflow) |
| **AI — Speech** | Speechmatics (real-time WebSocket STT) |
| **Database** | Supabase (PostgreSQL + Auth + S3 Storage) |
| **Observability** | LangSmith (tracing, datasets, evaluations) |
| **Payments** | Stripe |
| **Deployment** | Docker, Docker Compose |

---

## Project Structure

```
StoryBookUI/
├── api/                              # FastAPI Backend
│   ├── main.py                       # App setup, CORS, credit refill scheduler
│   ├── agents/
│   │   ├── story_agent.py            # LangGraph workflow (3 nodes), character consistency
│   │   └── utils.py                  # Story/Chapter schemas, image upload, Supabase S3
│   ├── routers/
│   │   ├── stories.py                # Story generation endpoints (open + guided)
│   │   ├── tasks.py                  # Celery task status polling
│   │   └── transcription.py          # WebSocket speech-to-text
│   ├── celery_tasks/
│   │   ├── app.py                    # Celery config (Redis broker)
│   │   └── tasks.py                  # generate_story_task (orchestrates full pipeline)
│   ├── services/
│   │   ├── user_service.py           # JWT verification, credit management
│   │   ├── supabase_client.py        # Supabase client init
│   │   └── pdf_service.py            # PDF generation (fpdf2, OpenDyslexic)
│   ├── prompts/
│   │   ├── story_prompts.py          # System prompts, character extraction prompt
│   │   ├── guided_story_prompts.py   # Guided story prompt builder
│   │   └── translations/             # Localized prompts (en, es, fr, de, it, pt)
│   └── core/
│       ├── config.py                 # Environment config
│       └── dependencies.py           # Auth + credit dependency injection
│
├── frontend/                         # Next.js 15 Application
│   ├── app/
│   │   ├── page.tsx                  # Landing page
│   │   ├── make-tale/
│   │   │   ├── page.tsx              # Story type selection (open vs guided)
│   │   │   ├── open/page.tsx         # Free-form story creator
│   │   │   └── guided/page.tsx       # Guided story creator
│   │   ├── gallery/page.tsx          # Story gallery with pagination
│   │   ├── account/page.tsx          # User account & credits
│   │   ├── auth/                     # Login, signup, OAuth callback
│   │   ├── pricing/page.tsx          # Plans & pricing
│   │   ├── about/page.tsx            # About page
│   │   └── faq/page.tsx              # FAQ
│   ├── components/
│   │   ├── tale-generator.tsx        # Open story form (text + voice input)
│   │   ├── guided-tale-generator.tsx # Guided story form (age, topic, mission, style)
│   │   ├── story-viewer.tsx          # Full story display with images
│   │   ├── story-modal.tsx           # Story preview modal
│   │   └── ui/                       # Radix-based design system
│   ├── hooks/
│   │   └── use-story-generation.ts   # Generation logic, API polling, state
│   ├── lib/supabase/                 # Supabase clients, session, queries
│   └── locales/                      # UI translations (en, es, fr, de, it, pt)
│
├── db/
│   └── schema.sql                    # PostgreSQL schema (stories, profiles, RLS)
│
├── llm_evaluation/                   # LLM Evaluation Framework
│   └── safety/safety_evals/
│       ├── scripts/
│       │   └── evaluate_safety.py    # LLM-as-a-judge safety evaluator
│       └── test_generator/
│           ├── generate_test_stories.py  # Test story generator (bypasses API)
│           ├── evaluate_from_file.py     # Offline file-based evaluator
│           ├── prompts/                  # 10 open + 10 guided test prompts
│           └── results/
│               ├── story_generation/          # Generated stories output
│               └── story_safety_evaluation/   # Evaluation results
│
├── docker-compose.yml
└── .env.example
```

---

## Story Generation Flow

### Open Story (Free-Form)

```
User writes prompt  ──▶  POST /stories/generate-story-async  ──▶  Celery Task
        │                                                              │
        │                                                              ▼
        │                                                     LangGraph Workflow
        │                                                    ┌─────────────────┐
        │                                                    │ 1. Generate Story│
        │                                                    │    (Groq LLaMA)  │
        │                                                    └────────┬────────┘
        │                                                             ▼
        │                                                    ┌─────────────────┐
        │                                                    │ 2. Extract Chars │
        │                                                    │  (visual specs)  │
        │                                                    └────────┬────────┘
        │                                                             ▼
        │                                                    ┌─────────────────┐
        │    polls GET /tasks/{id}                           │ 3. Gen Images   │
        │◀──────────────────────────────────────────────────│  (DALL-E 3)     │
                                                             └─────────────────┘
```

### Guided Story (Educational)

Same workflow, but the prompt is constructed from structured parameters:

| Parameter | Options |
|-----------|---------|
| **Age group** | 3–5, 5–8 |
| **Protagonist** | Custom name + description |
| **Scientific topic** | Shapes, Sound, Water, Animals, Space, Cultures, Human Body… |
| **Mission** | Topic-specific quest (e.g., "Lost Orchestra" for Sound) |
| **Visual style** | Cartoons, Watercolor, 3D Animation, Anime, Child Crayons, Illustration |
| **Chapters** | 3–10 |

---

## Character Consistency System

One of the key challenges in AI-generated illustrated stories is maintaining visual consistency across chapters. Cuentee solves this with a 3-step approach:

1. **Extract** — After story generation, a dedicated LangGraph node reads the full story and produces a structured character list with concrete visual specs (species, hair color/style, eye color, skin tone, clothing, body type, distinguishing features).

2. **Filter** — For each chapter, only characters that appear in that chapter's text are selected.

3. **Inject verbatim** — Character descriptions are appended **after** the image-prompt LLM generates the scene description. They never pass through the LLM, so they remain **byte-identical** across every chapter.

```
Character extraction output (stored once):
  - Luna: human girl, 8 years old, long curly red hair, green eyes, fair skin,
    blue denim overalls with yellow star patch, freckles on nose, slim build
  - Rocco: gray tabby cat, adult, amber eyes, dark stripes, green collar
    with bell, stocky build

Chapter 1 image prompt (Luna + Rocco present):
  [LLM-generated scene description]
  CHARACTER CONSISTENCY (exact visual specs):
  - Luna: human girl, 8 years old, long curly red hair, green eyes, ...
  - Rocco: gray tabby cat, adult, amber eyes, dark stripes, ...

Chapter 2 image prompt (only Luna present):
  [LLM-generated scene description]
  CHARACTER CONSISTENCY (exact visual specs):
  - Luna: human girl, 8 years old, long curly red hair, green eyes, ...
```

---

## LLM Evaluation

The project includes a safety evaluation framework to ensure all generated content is appropriate for children.

### Safety Evaluator (`evaluate_safety.py`)

Uses an **LLM-as-a-judge** pattern with Groq to evaluate stories:

| Field | Description |
|-------|-------------|
| `verdict` | `CHILD_SAFE` or `NOT_CHILD_SAFE` |
| `score` | 0–3 (3 = perfectly safe, 0 = highly unsafe) |
| `reason` | Explanation |
| `flagged_categories` | Violence, adult content, scary elements, etc. |

**Quality gate**: ≥ 90% of stories must score ≥ 2 (safe). Exit code 0 = pass, 1 = fail.

### Test Story Generator (`generate_test_stories.py`)

Generates stories directly via LangGraph (bypasses Celery/API) for evaluation:

```bash
# Generate 5 open + 5 guided stories, skip images
python -m llm_evaluation.safety.safety_evals.test_generator.generate_test_stories \
  --type both --count 5 --skip-images

# Evaluate the generated stories offline
python -m llm_evaluation.safety.safety_evals.test_generator.evaluate_from_file \
  --input results/story_generation/eval_stories_YYYYMMDD_HHMMSS.json
```

**CLI Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--type` | `both` | `open`, `guided`, or `both` |
| `--count` | `10` | Stories per type |
| `--model` | `llama-3.3-70b-versatile` | Groq model |
| `--lang` | per-prompt | Override language |
| `--skip-images` | `true` | Skip image generation (saves cost) |
| `--with-images` | — | Enable image generation |
| `--project` | `story-eval-test` | LangSmith project name |
| `--delay` | `5` | Seconds between generations (rate limit) |

### Evaluation Workflow

```
Step 1: Generate                          Step 2: Evaluate
┌──────────────────────┐                 ┌──────────────────────┐
│  generate_test_       │                │  evaluate_from_       │
│  stories.py           │    JSON file   │  file.py              │
│                       │───────────────▶│                       │
│  → story_generation/  │                │  → story_safety_      │
│    eval_stories_*.json│                │    evaluation/        │
└──────────────────────┘                 │    eval_*.json        │
                                         └──────────┬───────────┘
                                                    │
                                                    ▼
                                           Quality Gate ≥ 90%
                                           exit 0 ✓ / exit 1 ✗
```

### LangSmith Integration

For production evaluation using traces:

```bash
python -m llm_evaluation.safety.safety_evals.scripts.evaluate_safety \
  --project your-langsmith-project --limit 50
```

This fetches recent successful runs from LangSmith, creates a dataset, and runs the safety evaluator on each story.

---

## Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Node.js 18+** (local frontend dev)
- **Python 3.11+** (local backend dev)
- API keys: **OpenAI**, **Groq**, **Supabase**

### Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
# AI Services
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
SUPABASE_PROJECT_REF=xxx

# Infrastructure
NEXT_PUBLIC_API_URL=http://localhost:8000
REDIS_URL=redis://localhost:6379/0
STORAGE_BUCKET_NAME=cuentee_images

# Optional
SPEECHMATICS_API_KEY=...          # Voice input
LANGCHAIN_TRACING_V2=true         # LangSmith tracing
LANGCHAIN_API_KEY=ls__...         # LangSmith key
IMAGE_MODEL=dalle-3               # Image model override
```

### Run with Docker

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |

### Run Locally

**Backend:**

```bash
pip install -r api/requirements.txt

# Terminal 1: Start Redis
redis-server

# Terminal 2: Start API
uvicorn api.main:app --reload

# Terminal 3: Start Celery worker
celery -A api.celery_tasks.app worker --loglevel=info
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/stories/generate-story-async` | Generate an open story (async) |
| `POST` | `/stories/generate_guided_story_async` | Generate a guided story (async) |
| `GET` | `/tasks/{task_id}` | Poll task status (`PENDING` → `SUCCESS`/`FAILURE`) |
| `WS` | `/transcription/transcribe` | Real-time speech-to-text |
| `GET` | `/` | Health check |

All story endpoints require a Bearer token (Supabase JWT) and available credits.

---

## Database Schema

```sql
-- stories: Generated stories with full content and metadata
stories (
  id          UUID PRIMARY KEY,
  user_id     UUID REFERENCES auth.users,
  title       TEXT,
  content     TEXT,          -- JSON-serialized Story object
  prompt      TEXT,          -- Original user prompt
  story_type  TEXT,          -- 'open' or 'guided'
  metadata    JSONB,         -- language, style, age_group, topic, characters...
  created_at  TIMESTAMPTZ,
  updated_at  TIMESTAMPTZ    -- Auto-updated via trigger
);

-- profiles: User accounts with credit system
profiles (
  id              UUID PRIMARY KEY REFERENCES auth.users,
  credits         INTEGER DEFAULT 3,
  plan            TEXT DEFAULT 'free',   -- 'free' or 'plus'
  plus_since      TIMESTAMPTZ,
  last_credited_at TIMESTAMPTZ
);

-- Row-Level Security: users can only access their own data
```

---

## License

MIT
