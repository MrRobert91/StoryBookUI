# StoryBookUI

StoryBookUI is a simple prototype for generating personalized children's tales using AI. The system now consists of a React frontend and a FastAPI backend, both running in Docker.

## Features

- Responsive SPA with pages: Home, Make a Tale, About Us, Pricing and FAQ
- Tale generation handled by a FastAPI service
- Docker setup to run the frontend and the API

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Running locally
```bash
git clone <repo>
cd StoryBookUI
docker-compose up --build
```
The frontend will be available at `http://localhost:3000`.

### Environment Variables
Copy `.env.example` to `.env` and update the values if you want to connect to OpenAI:
```bash
OPENAI_API_KEY=<your-openai-key>
```

## Project Structure
```
frontend/       React application (Vite + Tailwind)
api/            FastAPI backend
docker-compose.yml  Docker orchestration
```

## API
The FastAPI service exposes a `/generate-story` endpoint that returns a short tale based on the provided description.

## License
MIT
