# StoryBookUI

StoryBookUI is a prototype application for generating personalized children's tales using AI. It features a modern frontend built with **Next.js 15** and a robust backend powered by **FastAPI**, capable of generating both text stories and illustrated tales using advanced AI models.

> [!NOTE]
> The application is currently deployed and available for use at **[https://www.cuentee.com/](https://www.cuentee.com/)**.

## Features

- **Personalized Story Generation**: Create unique stories based on user prompts.
- **Illustrated Tales**: Generate stories with accompanying images using a LangGraph workflow.
- **Multiple AI Models**:
  - Text generation: **Llama 3** (via Groq).
  - Image generation: **DALL-E 3**, **GPT-image-1**, **GPT-Image-1-mini**, **GPT-Image-1.5**.
- **User System**:
  - Secure Authentication via **Supabase Auth**.
  - Credit-based system for controlling usage.
- **Responsive UI**: Modern, accessible interface built with Radix UI and TailwindCSS.
- **Background Processing**: Asynchronous task handling for long-running generation jobs.

## Architecture & Tech Stack

The project follows a decoupled architecture:

### Frontend (`/frontend`)
- **Framework**: Next.js 15 (App Router)
- **Styling**: TailwindCSS, Tailwind Merge, CLSX
- **Components**: Radix UI (Primitives), Lucide React (Icons)
- **State/Auth**: Supabase Auth Helpers

### Backend (`/api`)
- **Framework**: FastAPI
- **Asynchronous Tasks**: Celery with Redis broker
- **AI Integration**:
  - **LangChain** & **LangGraph** for orchestration.
  - **Groq** for high-speed LLM inference.
  - **OpenAI** for image generation.
- **Database**: Supabase (PostgreSQL)

## Project Structure

```
├── frontend/           # Next.js application
│   ├── app/            # App Router pages and layouts
│   └── components/     # Reusable UI components
├── api/                # FastAPI backend service
│   ├── agents/         # AI agents and workflows (LangGraph)
│   ├── celery_tasks/   # Background jobs
│   ├── routers/        # API endpoints
│   └── services/       # Business logic and external services
├── docker-compose.yml  # Container orchestration setup
└── README.md
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.10+ (for local backend dev)
- Accounts/API Keys for: OpenAI, Groq, Supabase

### Environment Variables
Create a `.env` file in the root directory by copying `.env.example`:

```bash
# AI Services
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Backend
NEXT_PUBLIC_API_URL=http://localhost:8000
REDIS_URL=redis://localhost:6379/0
```

### Running with Docker

Start both the frontend and backend services:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### Running Locally

**Backend:**
```bash
cd StoryBookUI
# Install dependencies
pip install -r api/requirements.txt
# Run Redis (required for Celery)
# ... start redis server ...
# Start API
uvicorn api.main:app --reload
# Start Celery Worker (in a separate terminal)
celery -A api.celery_tasks.app worker --loglevel=info
```

**Frontend:**
```bash
cd StoryBookUI/frontend
npm install
npm run dev
```

## License
MIT
