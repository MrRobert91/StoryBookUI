import json
import re
import logging
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from openai import OpenAI
import os
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

# Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

# Cargar API keys desde variables de entorno
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Set it in your .env file.")

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY not found. Set it in your .env file.")

client = OpenAI(api_key=openai_key)

# ============================================================================
# SCHEMAS
# ============================================================================
class Chapter(BaseModel):
    title: str = Field(description="Chapter title")
    content: str = Field(description="Chapter content/story text")
    image_url: str | None = None

class Story(BaseModel):
    title: str = Field(description="Story title")
    cover_image_url: str | None = None
    chapters: List[Chapter] = Field(description="List of story chapters")

class StoryState(TypedDict):
    messages: list
    story_data: Story | None
    final_output: dict | None

# ============================================================================
# IMAGE MODEL CONFIGURATION
# ============================================================================
IMAGE_MODELS = {
    "dalle-3": "dall-e-3",
    "dalle-2": "dall-e-2",
    "gpt-image-1": "gpt-image-1",
    "gpt-image-1-mini": "gpt-image-1-mini",
}
DEFAULT_IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3").strip().lower()
SELECTED_IMAGE_MODEL = IMAGE_MODELS.get(DEFAULT_IMAGE_MODEL, "dall-e-3")
logger.info(f"Image model: {SELECTED_IMAGE_MODEL}")

# ============================================================================
# IMAGE GENERATION
# ============================================================================
def generate_image(prompt: str, model: str = None) -> str:
    """Generate image using OpenAI API"""
    model_name = IMAGE_MODELS.get((model or SELECTED_IMAGE_MODEL).lower(), SELECTED_IMAGE_MODEL)
    logger.info(f"Generating image with {model_name}, prompt length: {len(prompt)}")
    
    try:
        # Preparar parámetros base
        params = {
            "model": model_name,
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1
        }
        
        # Añadir 'quality' solo para gpt-image-1 y gpt-image-1-mini
        if model_name in ["gpt-image-1", "gpt-image-1-mini"]:
            params["quality"] = "low"
            logger.debug(f"Added quality='low' for {model_name}")
        
        response = client.images.generate(**params)
        logger.info(f"Image generation response: {response}") # Eliminar en producción
        url = response.data[0].url
        logger.info(f"Generated image: {url}")
        return url
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return ""

def make_image_prompt(text: str) -> str:
    """Use LLM to create optimized DALL-E prompt from story text"""
    try:
        response = image_llm.invoke([
            {
                "role": "system", 
                "content": (
                    "Create a concise image prompt suitable for children's books. "
                    "The result MUST describe an illustration in a whimsical storybook/cartoon style, and appropriate for all ages. "
                    "Use bright, pastel colors, soft lines, and magical elements. "
                    "AVOID any scary, violent, dark, or realistic/photorealistic imagery. Focus on bright colors, friendly characters, "
                    "and magical elements. Return only the prompt text."
                )
            },
            {"role": "user", "content": f"Story text:\n\n{text[:2000]}"}
        ])
        prompt = response.content.strip() if hasattr(response, 'content') else text[:500]
        logger.debug(f"Generated child-friendly prompt: {prompt[:200]}")
        return prompt
    except Exception as e:
        logger.error(f"Error creating image prompt: {e}")
        return text[:500]

# ============================================================================
# CONFIGURATION
# ============================================================================
DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "3"))
WORDS_PER_CHAPTER = 250

# ============================================================================
# AGENTS
# ============================================================================
'''
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY not found. Set it in your .env file.")

'''
logger.info("Building story_agent (Groq)...")
story_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

story_system_prompt = f"""Generate creative fantasy stories for children with exactly {DEFAULT_NUM_CHAPTERS} chapters.

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
    {{"title": "Chapter 2: The Journey", "content": "The young dragon..."}}
  ]
}}"""

story_agent = create_agent(
    model=story_llm,
    tools=[],
    response_format=Story,
    system_prompt=story_system_prompt
)
logger.info(f"story_agent ready (configured for {DEFAULT_NUM_CHAPTERS} chapters, ~{WORDS_PER_CHAPTER} words each)")

logger.info("Building image_llm (Groq)...")
image_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
logger.info("image_llm ready")

# ============================================================================
# WORKFLOW NODES
# ============================================================================
def story_generation_node(state: StoryState):
    """Generate story text using Groq LLM"""
    logger.info("Node: story_generation")
    messages = state.get("messages", [])
    '''
     # Añadir instrucción explícita sobre número de capítulos si no está en el mensaje
    user_message = messages[0]["content"] if messages else ""
    if "chapter" not in user_message.lower():
        enhanced_message = f"{user_message}. Generate exactly {DEFAULT_NUM_CHAPTERS} chapters, each with approximately {WORDS_PER_CHAPTER} words."
        messages = [{"role": "user", "content": enhanced_message}]
    '''
    logger.info(f"Invoking story_agent with messages: {messages}")
    
    result = story_agent.invoke({"messages": messages})
    logger.info("story_agent responded")
    
    # Extract structured Story from result
    story = result.get("structured_response") or result.get("story_data") or result
    if isinstance(story, dict):
        story = Story(**story)
    
    logger.info(f"Story generated: {story.title}, {len(story.chapters)} chapters")
    return {"story_data": story}

def image_generation_node(state: StoryState):
    """Generate images for cover and chapters"""
    logger.info("Node: image_generation")
    story = state.get("story_data")
    
    if not story:
        logger.error("No story_data in state")
        return {"final_output": None}
    
    # Cover image
    logger.info("Generating cover image...")
    cover_text = f"Book cover for: {story.title}\n\nChapters: {', '.join(c.title for c in story.chapters)}"
    cover_prompt = make_image_prompt(cover_text)
    story.cover_image_url = generate_image(cover_prompt)
    logger.info("Cover image URL: %s", story.cover_image_url)
    
    # Chapter images
    logger.info(f"Generating {len(story.chapters)} chapter images...")
    for idx, chapter in enumerate(story.chapters, 1):
        logger.info(f"Chapter {idx}: {chapter.title}")
        chapter_text = f"{chapter.title}\n\n{chapter.content[:1500]}"
        chapter_prompt = make_image_prompt(chapter_text)
        chapter.image_url = generate_image(chapter_prompt)
        logger.info("Chapter %d image URL: %s", idx, chapter.image_url)
    
    final_output = story.model_dump()
    # Log completo del JSON final (portada + capítulos con URLs)
    #logger.info("Final output JSON:\n%s", json.dumps(final_output, ensure_ascii=False, indent=2))
    logger.info("All images generated")
    return {"final_output": final_output}

# ============================================================================
# WORKFLOW GRAPH
# ============================================================================
logger.info("Building workflow graph...")
workflow = StateGraph(StoryState)

workflow.add_node("generate_story", story_generation_node)
workflow.add_node("generate_images", image_generation_node)

workflow.add_edge(START, "generate_story")
workflow.add_edge("generate_story", "generate_images")
workflow.add_edge("generate_images", END)

graph = workflow.compile()
logger.info("Workflow compiled")

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    logger.info("Starting workflow...")
    
    try:
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Write a sci-fi story about dragons in space."}]
        })
        logger.info("Workflow completed")
        
        final_output = result.get("final_output") or result
        # Log del JSON también en ejecución directa
        #logger.info("Final output JSON (main):\n%s", json.dumps(final_output, ensure_ascii=False, indent=2))
        
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, ensure_ascii=False, indent=2)
        
        logger.info("Result saved to output.json")
        print("Resultado guardado en output.json")
        
    except Exception as e:
        logger.exception("Error in workflow")
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(None, f)