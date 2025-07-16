# StoryBookUI

StoryBookUI is a SaaS prototype for generating personalized children's tales using AI. The system is built with React, Supabase and OpenAI, and is fully dockerized for easy deployment.

## Features

- User authentication with Supabase Auth (Google OAuth)
- Credit-based usage control stored in Supabase PostgreSQL
- Secure generation of tales via Supabase Edge Functions
- Responsive SPA with pages: Home, Make a Tale, About Us, Pricing and FAQ
- Docker setup to run the frontend and Deno edge functions

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- A Supabase project with environment variables for URL and API keys
- An OpenAI API key

### Running locally
```bash
git clone <repo>
cd StoryBookUI
docker-compose up --build
```
The frontend will be available at `http://localhost:3000`.

### Environment Variables
Copy `.env.example` to `.env` and update the values with your credentials:
```bash
VITE_SUPABASE_URL=<your-supabase-url>
VITE_SUPABASE_ANON_KEY=<your-anon-key>
OPENAI_API_KEY=<your-openai-key>
SUPABASE_URL=<your-supabase-url>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
```
The `OPENAI_API_KEY` is used by the edge functions.

## Project Structure
```
frontend/       React application (Vite + Tailwind)
functions/      Supabase Edge Functions (Deno)
docker-compose.yml  Docker orchestration
```

## Database Schema
A single table `user_credits` stores the available credits for each user:
```sql
CREATE TABLE user_credits (
  id uuid PRIMARY KEY REFERENCES auth.users(id),
  credits integer NOT NULL DEFAULT 0,
  created_at timestamptz DEFAULT now()
);
```

## Edge Functions
- `generate_tale`: validates credits, calls OpenAI and returns a tale
- `initialize_credits`: assigns initial credits when a new user registers

## License
MIT
