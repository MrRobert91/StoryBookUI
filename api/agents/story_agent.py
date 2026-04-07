import os
import uuid
import json
import logging
import re
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from api.prompts.story_prompts import get_story_system_prompt, get_image_prompt_system, get_character_extraction_prompt, DEFAULT_NUM_CHAPTERS, WORDS_PER_CHAPTER
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
logger.info(f"story_agent ready (configured for ~{WORDS_PER_CHAPTER} words per chapter)")

logger.info("Building image_llm (Groq)...")
image_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
logger.info("image_llm ready")

from langsmith import traceable

@traceable(run_type="chain", name="make_image_prompt")
def make_image_prompt(text: str, lang: str = "en", style_context: str = None) -> str:
    """Use LLM to create an image prompt for children's illustrations (non-realistic)."""
    try:
        user_content = f"Story text:\n\n{text[:2000]}"
        if style_context:
            user_content = f"VISUAL STYLE/CHARACTER INSTRUCTIONS:\n{style_context}\n\n" + user_content

        response = image_llm.invoke([
            {
                "role": "system",
                "content": get_image_prompt_system(lang),
            },
            {"role": "user", "content": user_content},
        ])
        prompt = response.content.strip() if hasattr(response, "content") else str(response).strip()
        
        logger.debug("Child-friendly prompt: %s", prompt[:200])
        return prompt
    except Exception as e:
        logger.error("Error creating image prompt: %s", e)
        base = (text[:500] if text else "A friendly fantasy scene")
        return f"{base}"


def _parse_character_lines(character_descriptions: str) -> list[tuple[str, str]]:
    """Parse '- Name: description' lines into (name, full_line) tuples."""
    parsed: list[tuple[str, str]] = []
    if not character_descriptions:
        return parsed

    for raw_line in character_descriptions.splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue

        body = line[2:].strip()
        if ":" not in body:
            continue

        name, _ = body.split(":", 1)
        name = name.strip()
        if not name:
            continue

        parsed.append((name, line))
    return parsed


def _name_variants(name: str) -> list[str]:
    """Generate search variants for a character name."""
    cleaned = re.sub(r"[^\w\s'-]", "", name, flags=re.UNICODE).strip()
    if not cleaned:
        return []

    tokens = [t for t in cleaned.split() if len(t) >= 3]
    variants = [cleaned, *tokens]

    # Deduplicate while preserving order
    unique_variants: list[str] = []
    seen = set()
    for variant in variants:
        key = variant.lower()
        if key not in seen:
            seen.add(key)
            unique_variants.append(variant)
    return unique_variants


def _build_chapter_character_block(character_descriptions: str, chapter_text: str) -> str:
    """Return only character lines that appear in chapter text/title."""
    chapter = chapter_text or ""
    if not character_descriptions or not chapter:
        return ""

    parsed = _parse_character_lines(character_descriptions)
    if not parsed:
        return ""

    matched_lines: list[str] = []
    for name, line in parsed:
        variants = _name_variants(name)
        if any(re.search(rf"\b{re.escape(v)}\b", chapter, flags=re.IGNORECASE) for v in variants):
            matched_lines.append(line)

    if not matched_lines:
        return ""

    return (
        "CHARACTER CONSISTENCY (Only characters present in this chapter; match exactly):\n"
        + "\n".join(matched_lines)
        + "\n\n"
    )

# ============================================================================
# WORKFLOW NODES
# ============================================================================
def story_generation_node(state: StoryState):
    """Generate story text using Groq LLM"""
    logger.info("Node: story_generation")
    messages = state.get("messages", [])
    num_chapters = state.get("num_chapters", DEFAULT_NUM_CHAPTERS)
    lang = state.get("language", "en") or "en"
    
    # Construir mensajes con system prompt dinamico
    system_prompt = get_story_system_prompt(lang, num_chapters)
    full_messages = [
        {"role": "system", "content": system_prompt},
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
        story.story_type = state.get("story_type", "open")
        story.metadata = state.get("metadata", {})
        return {"story_data": story}
        
    except Exception as e:
        logger.exception(f"Error generating story: {e}")
        raise

def character_extraction_node(state: StoryState):
    """Extract character descriptions from the complete story for visual consistency."""
    logger.info("Node: character_extraction")

    story = state.get("story_data")
    if not story:
        logger.warning("No story_data found, skipping character extraction")
        return {}

    lang = state.get("language", "en") or "en"

    # Build full story text
    full_text = f"Title: {story.title}\n\n"
    for ch in story.chapters:
        full_text += f"## {ch.title}\n{ch.content}\n\n"

    # Include existing protagonist info from guided stories if available
    existing_context = state.get("image_style_context") or ""
    protagonist_hint = ""
    if "CHARACTER DESIGN:" in existing_context:
        start = existing_context.index("CHARACTER DESIGN:")
        end_offset = existing_context[start:].find("\n\n")
        end = start + end_offset if end_offset != -1 else len(existing_context)
        protagonist_hint = (
            f"\n\nNote - the protagonist is already defined as:\n"
            f"{existing_context[start:end]}\n"
            f"Include this character in your list with these details preserved and enhanced.\n"
        )

    system_prompt = get_character_extraction_prompt(lang)

    try:
        response = image_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{full_text}{protagonist_hint}"}
        ])

        character_descriptions = response.content.strip() if hasattr(response, "content") else str(response).strip()
        logger.info(f"Extracted characters:\n{character_descriptions[:500]}")

        # Store in metadata for final output
        story.metadata["characters"] = character_descriptions

        return {
            "character_descriptions": character_descriptions,
            "story_data": story
        }
    except Exception as e:
        logger.error(f"Error extracting characters: {e}")
        return {}

def image_generation_node(state: StoryState):
    """Generate images for cover and chapters and upload to Supabase Storage"""
    logger.info("Node: image_generation")

    user_id = state.get("user_id")
    jwt_token = state.get("jwt_token")
    image_style_context = state.get("image_style_context") or ""
    character_descriptions = state.get("character_descriptions")
    
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
    lang = state.get("language", "en") or "en"
    cover_text = f"Book cover for: {story.title}\n\nChapters: {', '.join(c.title for c in story.chapters)}"
    cover_style_context = image_style_context
    if character_descriptions:
        cover_style_context = (
            "CHARACTER CONSISTENCY (Use only relevant characters for the cover scene):\n"
            f"{character_descriptions}\n\n"
        ) + image_style_context

    cover_prompt = make_image_prompt(cover_text, lang=lang, style_context=cover_style_context)
    story.cover_image_url = generate_image(cover_prompt, image_type="cover", model=model)
    logger.info("Cover image URL (Supabase): %s", story.cover_image_url)
    
    # Chapter images
    logger.info(f"Generating {len(story.chapters)} chapter images...")
    for idx, chapter in enumerate(story.chapters, 1):
        logger.info(f"Chapter {idx}: {chapter.title}")
        chapter_text = f"{chapter.title}\n\n{chapter.content[:1500]}"

        chapter_character_block = _build_chapter_character_block(character_descriptions or "", chapter_text)
        chapter_style_context = f"{chapter_character_block}{image_style_context}".strip()
        chapter_prompt = make_image_prompt(
            chapter_text,
            lang=lang,
            style_context=chapter_style_context if chapter_style_context else None
        )
        chapter.image_url = generate_image(chapter_prompt, image_type="chapter", model=model)
        logger.info("Chapter %d image URL (Supabase): %s", idx, chapter.image_url)
    
    final_output = story.model_dump()
    final_output["story_id"] = story_id
    final_output["user_id"] = user_id
    final_output["story_type"] = story.story_type
    final_output["metadata"] = story.metadata
    
    logger.info("All images generated and uploaded to Supabase Storage")
    return {"final_output": final_output}

# ============================================================================
# WORKFLOW GRAPH
# ============================================================================
logger.info("Building workflow graph...")
workflow = StateGraph(StoryState)

workflow.add_node("generate_story", story_generation_node)
workflow.add_node("extract_characters", character_extraction_node)
workflow.add_node("generate_images", image_generation_node)

workflow.add_edge(START, "generate_story")
workflow.add_edge("generate_story", "extract_characters")
workflow.add_edge("extract_characters", "generate_images")
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
