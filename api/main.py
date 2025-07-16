from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaleRequest(BaseModel):
    description: str

@app.post("/generate-story")
async def generate_story(req: TaleRequest):
    # Placeholder implementation replacing previous Supabase function
    return {"tale": f"Once upon a time about {req.description}"}
