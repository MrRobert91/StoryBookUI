from typing import Dict, Any
from api.prompts.utils import get_localized_prompts

def get_guided_story_prompts(
    lang: str,
    age_group: str,
    protagonist_name: str,
    protagonist_desc: str,
    scientific_topic: str,
    mission: str,
    visual_style: str,
    num_chapters: int
) -> Dict[str, str]:
    """
    Constructs the localized story and image prompts for a guided story.
    """
    prompts = get_localized_prompts(lang)
    
    TOPIC_PROMPTS = prompts["TOPIC_PROMPTS"]
    MISSION_PROMPTS = prompts["MISSION_PROMPTS"]
    VISUAL_STYLE_PROMPTS = prompts["VISUAL_STYLE_PROMPTS"]
    GUIDED_STORY_FORMAT = prompts["GUIDED_STORY_FORMAT"]
    
    topic_description = TOPIC_PROMPTS.get(scientific_topic, scientific_topic)
    mission_description = MISSION_PROMPTS.get(mission, mission)
    visual_style_description = VISUAL_STYLE_PROMPTS.get(visual_style, visual_style)
    
    # Construct Story Prompt
    system_base = GUIDED_STORY_FORMAT["system"].format(age_group=age_group)
    labels = GUIDED_STORY_FORMAT["data_labels"]
    structure = GUIDED_STORY_FORMAT["structure"].format(num_chapters=num_chapters)
    
    story_prompt = (
        f"{system_base}\n\n"
        f"DATA:\n"
        f"- {labels['protagonist']}: {protagonist_name}.\n"
        f"- {labels['topic']}: {topic_description}\n"
        f"- {labels['mission']}: {mission_description}\n\n"
        f"{structure}"
    )
    
    # Construct Image Style Context
    image_style_context = (
        f"CHARACTER DESIGN:\n"
        f"- Name: {protagonist_name}\n"
        f"- Description: {protagonist_desc}\n\n"
        f"ARTISTIC DIRECTION (Must follow strictly):\n"
        f"{visual_style_description}\n\n"
        f"TARGET AUDIENCE: Children {age_group} years old (keep it age-appropriate, safe, and engaging)."
    )
    
    return {
        "story_prompt": story_prompt,
        "image_style_context": image_style_context
    }
