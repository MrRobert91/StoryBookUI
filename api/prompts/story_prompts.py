import os

DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "10"))
WORDS_PER_CHAPTER = 350

def get_story_system_prompt(num_chapters: int = DEFAULT_NUM_CHAPTERS) -> str:
    return f"""Generate creative fantasy stories for children with exactly {num_chapters} chapters.

IMPORTANT GUIDELINES:
- Each chapter must have approximately {WORDS_PER_CHAPTER} words
- Content must be family-friendly and appropriate for children
- Use colorful, imaginative descriptions
- Include positive messages and friendly characters
- Return structured JSON with 'title' and 'chapters' array
- Each chapter must have 'title' and 'content' fields

Example structure:
{{
  "title": "The Dragon's Adventure",
  "chapters": [
    {{"title": "Chapter 1: The Discovery", "content": "Once upon a time..."}},
    {{"title": "Chapter 2: The Journey", "content": "The young dragon..."}},
    ...
  ]
}}"""

IMAGE_PROMPT_SYSTEM = (
    "Create a concise image prompt suitable for children's books. "
    "The result MUST describe an illustration consistent with the requested visual style. "
    "Focus on describing the scene, characters, and emotions clearly for a young audience. "
    "AVOID any scary, violent, dark, or realistic/photorealistic imagery. "
    "Do not mention cameras, lenses, or photographic terms. "
    "Return ONLY the prompt text."
)
