# StoryBookUI

StoryBookUI is a simple prototype for generating personalized children's tales using AI. The frontend has been migrated to **Next.js** using the App Router while the backend remains in FastAPI.

## Features

- Responsive UI with pages: Home, Make a Tale, About Us, Pricing and FAQ
- Tale generation handled by a FastAPI service
- Docker setup to run the frontend and the API
- Placeholder authentication structure ready for future Supabase integration

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Running locally
```bash
git clone <repo>
cd StoryBookUI
npm install --prefix nextapp
npm run dev --prefix nextapp
```
The frontend will be available at `http://localhost:3000`.

### Environment Variables
Copy `.env.example` to `.env` and fill in the required values for OpenAI, Groq and Supabase:
```bash
OPENAI_API_KEY=<your-openai-key>
GROQ_API_KEY=<your-groq-key>
NEXT_PUBLIC_SUPABASE_URL=<your-supabase-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure
```
nextapp/        Next.js application
api/            FastAPI backend
docker-compose.yml  Docker orchestration
```

### Authentication
The app includes React context and hooks prepared for a future Supabase integration. Buttons for Register, Login and Logout are visible in the header but currently use mock state.

## API
The FastAPI service exposes a `/generate-story` endpoint that returns a short tale based on the provided description.

## License
MIT
