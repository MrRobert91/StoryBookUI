import os
from api.prompts.utils import get_localized_prompts

DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "10"))
WORDS_PER_CHAPTER = 350

def get_story_system_prompt(lang: str = "en", num_chapters: int = DEFAULT_NUM_CHAPTERS) -> str:
    prompts = get_localized_prompts(lang)
    sys_prompts = prompts["STORY_SYSTEM_PROMPTS"]
    
    system = sys_prompts["system"].format(num_chapters=num_chapters)
    guidelines = sys_prompts["guidelines"].format(words_per_chapter=WORDS_PER_CHAPTER)
    
    return f"{system}\n\n{guidelines}"

def get_image_prompt_system(lang: str = "en") -> str:
    prompts = get_localized_prompts(lang)
    return prompts["STORY_SYSTEM_PROMPTS"]["image_system"]

