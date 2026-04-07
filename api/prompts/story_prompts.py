import os
from api.prompts.utils import get_localized_prompts

DEFAULT_NUM_CHAPTERS = int(os.getenv("NUM_CHAPTERS", "10"))
WORDS_PER_CHAPTER = 350

OBJECTIVE_CHARACTER_EXTRACTION_PROMPT = (
    "You are a visual character specification extractor for children's book illustration.\n"
    "Read the full story and extract EVERY named character.\n"
    "For each character, produce an objective visual spec for consistent illustration.\n\n"
    "Output EXACTLY one bullet line per character with this format:\n"
    "- [Name]: [species/type], [apparent age], [hair/fur style and color], "
    "[eye color], [skin/fur/scale color], [clothing items and colors], "
    "[distinctive physical markers], [body size/build]\n\n"
    "Rules:\n"
    "- Use only observable, concrete attributes.\n"
    "- Every character line MUST include all fields in the required order.\n"
    "- Avoid subjective or emotional wording (e.g., warm smile, refreshing smile, lively look, pastel vibe).\n"
    "- Prefer precise terms: exact colors, garment types, materials, shapes, lengths, sizes, patterns.\n"
    "- Colors must be explicit (e.g., dark brown, light blue, olive green), not vague (colorful, pastel, bright).\n"
    "- Clothing must be explicit (e.g., red hooded cape, denim overalls, white cotton shirt), not generic (nice clothes).\n"
    "- Body description must be explicit (e.g., short and slim, medium build, tall and broad).\n"
    "- If a detail is missing, infer a neutral, concrete visual detail that fits the story context.\n"
    "- Include ALL named characters, including minor ones.\n"
    "- Do NOT add any extra text outside the bullet list.\n"
    "- Write descriptions in English regardless of story language."
)

def get_story_system_prompt(lang: str = "en", num_chapters: int = DEFAULT_NUM_CHAPTERS) -> str:
    prompts = get_localized_prompts(lang)
    sys_prompts = prompts["STORY_SYSTEM_PROMPTS"]
    
    system = sys_prompts["system"].format(num_chapters=num_chapters)
    guidelines = sys_prompts["guidelines"].format(words_per_chapter=WORDS_PER_CHAPTER)
    
    return f"{system}\n\n{guidelines}"

def get_image_prompt_system(lang: str = "en") -> str:
    prompts = get_localized_prompts(lang)
    return prompts["STORY_SYSTEM_PROMPTS"]["image_system"]

def get_character_extraction_prompt(lang: str = "en") -> str:
    _ = lang
    return OBJECTIVE_CHARACTER_EXTRACTION_PROMPT

