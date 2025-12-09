import os

DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "3"))
WORDS_PER_CHAPTER = 350

STORY_SYSTEM_PROMPT = f"""Generate creative fantasy stories for children with exactly {DEFAULT_NUM_CHAPTERS} chapters.

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
    {{"title": "Chapter 3: The Challenge", "content": "The dragon faced a challenge..."}},
    {{"title": "Chapter 4: The Triumph", "content": "The dragon triumphed..."}}
  ]
}}"""

IMAGE_PROMPT_SYSTEM = (
    "Create a concise image prompt suitable for children's books. "
    "The result MUST describe an illustration in a whimsical storybook/cartoon style. "
    "Use bright, pastel colors, soft lines, friendly characters, and magical elements. "
    "AVOID any scary, violent, dark, or realistic/photorealistic imagery. "
    "Do not mention cameras, lenses, or photographic terms. "
    "Return ONLY the prompt text."
)
