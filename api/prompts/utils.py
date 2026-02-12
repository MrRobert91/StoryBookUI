import importlib
import logging

logger = logging.getLogger(__name__)

def get_localized_prompts(lang: str):
    """
    Loads localized prompts for the given language.
    Defaults to English if the language is not supported.
    """
    # Normalize language code (e.g., 'es-ES' -> 'es', 'Spanish' -> 'es')
    lang_map = {
        "es": "es",
        "spanish": "es",
        "en": "en",
        "english": "en",
        "fr": "fr",
        "pt": "pt",
        "it": "it",
        "de": "de"
    }
    
    clean_lang = lang.lower().split("-")[0]
    target_lang = lang_map.get(clean_lang, "en")
    
    try:
        module = importlib.import_module(f"api.prompts.translations.{target_lang}")
        return {
            "VISUAL_STYLE_PROMPTS": getattr(module, "VISUAL_STYLE_PROMPTS"),
            "TOPIC_PROMPTS": getattr(module, "TOPIC_PROMPTS"),
            "MISSION_PROMPTS": getattr(module, "MISSION_PROMPTS"),
            "STORY_SYSTEM_PROMPTS": getattr(module, "STORY_SYSTEM_PROMPTS"),
            "GUIDED_STORY_FORMAT": getattr(module, "GUIDED_STORY_FORMAT")
        }
    except Exception as e:
        logger.error(f"Error loading localized prompts for {target_lang}: {e}")
        # Fallback to English
        module = importlib.import_module("api.prompts.translations.en")
        return {
            "VISUAL_STYLE_PROMPTS": getattr(module, "VISUAL_STYLE_PROMPTS"),
            "TOPIC_PROMPTS": getattr(module, "TOPIC_PROMPTS"),
            "MISSION_PROMPTS": getattr(module, "MISSION_PROMPTS"),
            "STORY_SYSTEM_PROMPTS": getattr(module, "STORY_SYSTEM_PROMPTS"),
            "GUIDED_STORY_FORMAT": getattr(module, "GUIDED_STORY_FORMAT")
        }
