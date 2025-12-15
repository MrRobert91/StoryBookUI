import os
import uuid
import json
import logging
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from api.prompts.story_prompts import STORY_SYSTEM_PROMPT, IMAGE_PROMPT_SYSTEM, DEFAULT_NUM_CHAPTERS, WORDS_PER_CHAPTER
# Import utilities from the sibling module
from .utils import (
    Story, 
    StoryState, 
    generate_image, 
    set_user_context, 
    logger, 
    _image_counter
)

# Cargar API keys
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY not found. Set it in your .env file.")

# ============================================================================
# AGENTS SETUP
# ============================================================================
logger.info("Building story_agent (Groq)...")
story_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

story_agent = story_llm.with_structured_output(Story, method="json_mode")
logger.info(f"story_agent ready (configured for {DEFAULT_NUM_CHAPTERS} chapters, ~{WORDS_PER_CHAPTER} words each)")

logger.info("Building image_llm (Groq)...")
image_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
logger.info("image_llm ready")

def make_image_prompt(text: str) -> str:
    """Use LLM to create an image prompt for children's illustrations (non-realistic)."""
    try:
        response = image_llm.invoke([
            {
                "role": "system",
                "content": IMAGE_PROMPT_SYSTEM,
            },
            {"role": "user", "content": f"Story text:\n\n{text[:2000]}"},
        ])
        prompt = response.content.strip() if hasattr(response, "content") else str(response).strip()
        
        logger.debug("Child-friendly prompt: %s", prompt[:200])
        return prompt
    except Exception as e:
        logger.error("Error creating image prompt: %s", e)
        base = (text[:500] if text else "A friendly fantasy scene")
        return f"{base}"

# ============================================================================
# WORKFLOW NODES
# ============================================================================
def story_generation_node(state: StoryState):
    """Generate story text using Groq LLM"""
    logger.info("Node: story_generation")
    messages = state.get("messages", [])
    
    # Construir mensajes con system prompt
    full_messages = [
        {"role": "system", "content": STORY_SYSTEM_PROMPT},
        *messages
    ]
    
    user_content = "No content"
    if messages:
        first_msg = messages[0]
        if isinstance(first_msg, dict):
            user_content = first_msg.get('content', "No content")
        elif isinstance(first_msg, tuple) and len(first_msg) > 1:
             user_content = first_msg[1]
        elif hasattr(first_msg, 'content'):
             user_content = first_msg.content
        else:
             user_content = str(first_msg)

    logger.info(f" [LLM Input] Sending prompt to Groq: '{user_content}'")
    
    try:
        story = story_agent.invoke(full_messages)
        
        if not story or not isinstance(story, Story):
            logger.error("Invalid story response from LLM")
            raise ValueError("Failed to generate valid story structure")
        
        logger.info(f"Story generated: {story.title}, {len(story.chapters)} chapters")
        return {"story_data": story}
        
    except Exception as e:
        logger.exception(f"Error generating story: {e}")
        raise

def image_generation_node(state: StoryState):
    """Generate images for cover and chapters and upload to Supabase Storage"""
    logger.info("Node: image_generation")
    
    user_id = state.get("user_id")
    jwt_token = state.get("jwt_token")
    
    if not user_id or not jwt_token:
        logger.error("user_id or jwt_token not provided in state")
        raise ValueError("user_id and jwt_token are required for image generation")
    
    story_id = str(uuid.uuid4())
    set_user_context(user_id, jwt_token, story_id)
    
    # Reset counters from utils
    _image_counter["cover"] = 0
    _image_counter["chapter"] = 0
    
    story = state.get("story_data")
    model = state.get("model")
    
    if not story:
        logger.error("No story_data in state")
        return {"final_output": None}
    
    # Cover image
    logger.info("Generating cover image...")
    cover_text = f"Book cover for: {story.title}\n\nChapters: {', '.join(c.title for c in story.chapters)}"
    cover_prompt = make_image_prompt(cover_text)
    story.cover_image_url = generate_image(cover_prompt, image_type="cover", model=model)
    logger.info("Cover image URL (Supabase): %s", story.cover_image_url)
    
    # Chapter images
    logger.info(f"Generating {len(story.chapters)} chapter images...")
    for idx, chapter in enumerate(story.chapters, 1):
        logger.info(f"Chapter {idx}: {chapter.title}")
        chapter_text = f"{chapter.title}\n\n{chapter.content[:1500]}"
        chapter_prompt = make_image_prompt(chapter_text)
        chapter.image_url = generate_image(chapter_prompt, image_type="chapter", model=model)
        logger.info("Chapter %d image URL (Supabase): %s", idx, chapter.image_url)
    
    final_output = story.model_dump()
    final_output["story_id"] = story_id
    final_output["user_id"] = user_id
    
    logger.info("All images generated and uploaded to Supabase Storage")
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
# EXECUTION (TEST)
# ============================================================================
if __name__ == "__main__":
    logger.info("Starting workflow...")
    
    try:
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Write a sci-fi story about dragons in space."}],
            "user_id": "test_user",
            "jwt_token": None
        })
        logger.info("Workflow completed")
        
        final_output = result.get("final_output") or result
        
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(final_output, f, ensure_ascii=False, indent=2)
        
        logger.info("Result saved to output.json")
        print("Resultado guardado en output.json")
        
    except Exception as e:
        logger.exception("Error in workflow")
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(None, f)
