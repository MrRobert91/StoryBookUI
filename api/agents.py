from pydantic import BaseModel, Field
from typing import List
import json
import re
import logging
from datetime import datetime
from collections import defaultdict
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict






# Config logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Cargar .env si existe (útil para desarrollo local)
load_dotenv()  # busca .env en el working dir

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    logger.error("GROQ_API_KEY no definido. Define la variable de entorno o añade GROQ_API_KEY a tu .env")
    # no crear el LLM si no hay clave (evita traceback). Lanza si quieres fallo explícito:
    raise EnvironmentError("GROQ_API_KEY no definido; exporta la variable o añade a .env")


class Chapter(BaseModel):
    """Schema for a single chapter"""
    title: str = Field(description="Chapter title")
    content: str = Field(description="Chapter content/text")
    image_url: str | None = Field(default=None, description="Generated image URL for this chapter")

class Story(BaseModel):
    """Complete story with metadata and chapters"""
    title: str = Field(description="Story title")
    cover_image_url: str | None = Field(default=None, description="Cover image URL")
    chapters: List[Chapter] = Field(description="List of chapters with content and images")

# helper to extract url from various tool outputs
def extract_image_url(result) -> str | None:
    """
    Robust extractor for image URLs from various LangChain / tool responses.
    Handles: None, str, dict, list, message-like objects (with .content), nested structures.
    """
    logger.debug("extract_image_url input type=%s", type(result))
    try:
        if result is None:
            return None

        # If it's a list, try each item
        if isinstance(result, list):
            for item in result:
                url = extract_image_url(item)
                if url:
                    logger.debug("Found url in list item: %s", url)
                    return url
            return None

        # Message-like objects (HumanMessage, SystemMessage, etc.)
        # Many langchain message objects provide a `.content` attribute — use duck typing
        if hasattr(result, "content"):
            content = getattr(result, "content", None)
            logger.debug("Message-like object found, attempting extraction from content (type=%s)", type(content))
            if isinstance(content, (dict, list)):
                return extract_image_url(content)
            if isinstance(content, str):
                m = re.search(r"https?://\S+", content)
                if m:
                    return m.group(0)
                try:
                    parsed = json.loads(content)
                    return extract_image_url(parsed)
                except Exception:
                    pass
            return None

        # dict-like responses
        if isinstance(result, dict):
            # common direct keys
            for key in ("url", "image_url", "src", "data", "output"):
                if key in result:
                    val = result[key]
                    # if data is a list, inspect items
                    if key == "data" and isinstance(val, list):
                        for item in val:
                            url = extract_image_url(item)
                            if url:
                                return url
                    # if direct string url
                    if isinstance(val, str) and val.startswith("http"):
                        return val
                    # otherwise recurse
                    url = extract_image_url(val)
                    if url:
                        return url
            # try all values
            for v in result.values():
                url = extract_image_url(v)
                if url:
                    return url
            return None

        # string: search for http url or parse json
        if isinstance(result, str):
            m = re.search(r"https?://\S+", result)
            if m:
                return m.group(0)
            try:
                parsed = json.loads(result)
                return extract_image_url(parsed)
            except Exception:
                return None

        # fallback: stringify and search
        s = str(result)
        m = re.search(r"https?://\S+", s)
        if m:
            return m.group(0)

    except Exception:
        logger.exception("Error extracting image url")
    return None



logger.info("Construyendo story_agent (texto) usando langchain-groq...")

# build a ChatGroq LLM instance using GROQ_API_KEY
story_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

# Story generation with structured output using the Groq LLM instance
story_agent = create_agent(
    model=story_llm,
    tools=[],  # No tools needed for text generation
    response_format=Story,
    system_prompt="Generate creative stories with multiple chapters. Return structured JSON with title and chapters."
)
logger.info("story_agent (groq) construido")


client = OpenAI()

# Valid image models supported by OpenAI images endpoint
_IMAGE_MODEL_ALIASES = {
    "dalle-3": "dall-e-3",
    "dall-e-3": "dall-e-3",
    "dall-e-2": "dall-e-2",
    "gpt-image-1": "gpt-image-1",
    "gpt-image-1-mini": "gpt-image-1-mini",
}
_ALLOWED_IMAGE_MODELS = set(_IMAGE_MODEL_ALIASES.values())

# env/default selection (keeps previous logic)
IMAGE_MODEL_FLAG = os.getenv("IMAGE_MODEL", "dall-e-3").strip().lower()
_selected_image_model = _IMAGE_MODEL_ALIASES.get(IMAGE_MODEL_FLAG, "dall-e-3")
logger.info("Image generation model selected: %s (from IMAGE_MODEL=%s)", _selected_image_model, IMAGE_MODEL_FLAG)

# ---- Cache + guards para evitar llamadas repetidas ----
_IMAGE_TOOL_CACHE: dict[str, str] = {}
_IMAGE_TOOL_COUNTER = defaultdict(int)
_MAX_IMAGE_TOOL_CALLS_PER_RUN = 10

def _reset_image_tool_state():
    _IMAGE_TOOL_CACHE.clear()
    _IMAGE_TOOL_COUNTER.clear()
    logger.debug("Image tool cache and counters reset")

# ---- Implementación directa de generación de imagen (sin StructuredTool) ----
def _generate_image_impl(prompt: str, **kwargs) -> str:
    # Guard: evitar llamadas excesivas
    _IMAGE_TOOL_COUNTER["total"] += 1
    if _IMAGE_TOOL_COUNTER["total"] > _MAX_IMAGE_TOOL_CALLS_PER_RUN:
        logger.error("Límite de llamadas a generate_image alcanzado (%d). Abortando llamadas adicionales.",
                     _MAX_IMAGE_TOOL_CALLS_PER_RUN)
        return ""

    model_name = kwargs.get("model_name") or kwargs.get("model") or _selected_image_model
    requested = str(model_name).strip().lower()
    model_to_use = _IMAGE_MODEL_ALIASES.get(requested, _selected_image_model)

    cache_key = f"{model_to_use}::" + re.sub(r"\s+", " ", prompt.strip())[:2000]
    if cache_key in _IMAGE_TOOL_CACHE:
        _IMAGE_TOOL_COUNTER["cache_hits"] += 1
        logger.info("generate_image: cache hit for prompt (len=%d). Returning cached URL.", len(prompt))
        return _IMAGE_TOOL_CACHE[cache_key]

    logger.info("Llamando a _generate_image_impl con prompt (len=%d) usando modelo=%s", len(prompt), model_to_use)
    try:
        response = client.images.generate(
            model=model_to_use,
            prompt=prompt,
            size="1024x1024",
            n=1
        )
        logger.debug("generate_image response repr: %s", repr(response)[:1000])

        url = None
        if hasattr(response, "data") and isinstance(response.data, list) and response.data:
            first = response.data[0]
            if isinstance(first, dict):
                url = first.get("url") or ("data:image/png;base64," + first["b64_json"] if "b64_json" in first else None)
            else:
                url = getattr(first, "url", None) or (
                    "data:image/png;base64," + getattr(first, "b64_json") if hasattr(first, "b64_json") else None
                )
        if not url and hasattr(response, "url"):
            url = getattr(response, "url")
        if not url:
            text = getattr(response, "content", str(response))
            m = re.search(r"https?://\S+", text)
            if m:
                url = m.group(0)

        logger.info("_generate_image_impl produced URL: %s", url)
        _IMAGE_TOOL_CACHE[cache_key] = url or ""
        return url or ""
    except Exception:
        logger.exception("Error procesando la respuesta de _generate_image_impl")
        _IMAGE_TOOL_CACHE[cache_key] = ""
        return ""

# Referencia directa para usar en el workflow
generate_image = _generate_image_impl

logger.info("Construyendo image_agent (imágenes: prompts con Groq, generación de imágenes con OpenAI)...")

# Eliminar por completo la creación de image_agent y su system prompt
logger.info("Inicializando image_llm (Groq) para redactar prompts de imagen; la generación se hace con generate_image() directa.")
image_llm = ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)
# Nota: no se usa create_agent ni herramientas para imágenes.

class StoryState(TypedDict):
    """State for the multi-agent workflow"""
    messages: list
    story_data: Story | None
    final_output: dict | None

def story_generation_node(state: StoryState):
    """Generate story text"""
    logger.info("Entrando en node: story_generation_node")
    try:
        logger.info("Invocando story_agent con state.messages: %s", state.get("messages"))
        result = story_agent.invoke(state)
        logger.info("story_agent ha respondido")
        # try to log small preview
        try:
            logger.debug("story_agent result preview: %s", str(result)[:1000])
        except Exception:
            pass
        structured = result.get("structured_response", result)
        logger.info("Estructura obtenida del agente de texto")
        return {"story_data": structured}
    except Exception as exc:
        logger.exception("Error en story_generation_node")
        raise

def extract_text(result) -> str | None:
    """Extrae texto simple de respuestas del LLM / agente (duck-typing)."""
    try:
        if result is None:
            return None
        if isinstance(result, str):
            return result.strip()
        if isinstance(result, list):
            for item in result:
                t = extract_text(item)
                if t:
                    return t
            return None
        if hasattr(result, "content"):
            c = getattr(result, "content")
            if isinstance(c, str):
                return c.strip()
            return extract_text(c)
        if isinstance(result, dict):
            for k in ("text", "content", "message", "result"):
                if k in result and isinstance(result[k], str):
                    return result[k].strip()
            # try any value
            for v in result.values():
                t = extract_text(v)
                if t:
                    return t
        # fallback
        s = str(result).strip()
        return s if s else None
    except Exception:
        logger.exception("Error extracting text from result")
    return None

# BUILD image_llm already exists above
# image_agent can remain but no longer used to call the tool

def _make_image_prompt_from_llm(text_for_prompt: str) -> str:
    """
    Ask the image_llm to produce a single concise image prompt string.
    Instruct the model to return only the prompt text.
    """
    system = (
        "You are an image-prompt engineer. Given the following story text, produce a single, "
        "concise, vivid image prompt suitable for an image-generation API. "
        "Return ONLY the prompt text, nothing else."
    )
    user = f"Text for prompt generation:\n\n{text_for_prompt}\n\nReturn only the prompt text."
    try:
        # invoke LLM directly to get prompt (no tools)
        resp = image_llm.invoke([{"role": "system", "content": system},
                                 {"role": "user", "content": user}])
        logger.debug("image_llm.invoke resp type=%s preview=%s", type(resp), str(resp)[:500])
        prompt_text = extract_text(resp)
        if not prompt_text:
            logger.warning("image_llm returned no prompt_text; falling back to raw input text")
            prompt_text = text_for_prompt
        return prompt_text
    except Exception:
        logger.exception("Error generating image prompt from image_llm; falling back to raw text")
        return text_for_prompt

# Replace image_agent.invoke usage inside image_generation_node with prompt-generation + single generate_image call:

def image_generation_node(state: StoryState):
    logger.info("Entrando en node: image_generation_node")
    story = state.get("story_data")
    if not story:
        logger.error("No hay story_data en el estado")
        return {"final_output": None}
    try:
        # Portada: generar prompt (con LLM) y llamar una sola vez a generate_image()
        logger.info("Generando imagen de portada...")
        cover_input = f"Book cover for: {story.title}\n\nStory summary: " + " ".join([c.title + ". " for c in story.chapters])
        logger.debug("Cover input for prompt generation: %s", cover_input[:500])
        cover_prompt_text = _make_image_prompt_from_llm(cover_input)
        logger.info("Cover prompt generated (len=%d): %s", len(cover_prompt_text), cover_prompt_text[:200])
        cover_url = generate_image(cover_prompt_text)
        story.cover_image_url = cover_url
        logger.info("Cover image URL: %s", cover_url)

        # Capítulos: 1 llamada por capítulo
        logger.info("Generando imágenes para capítulos (%d)...", len(story.chapters))
        for idx, chapter in enumerate(story.chapters):
            try:
                logger.info("Generando prompt para capítulo %d: %s", idx+1, chapter.title)
                chapter_input = f"{chapter.title}: {chapter.content[:2000]}"
                chap_prompt_text = _make_image_prompt_from_llm(chapter_input)
                logger.info("Chapter %d prompt (len=%d): %s", idx+1, len(chap_prompt_text), chap_prompt_text[:200])
                ch_url = generate_image(chap_prompt_text)
                chapter.image_url = ch_url
                logger.info("Capítulo %d image_url: %s", idx+1, ch_url)
            except Exception:
                logger.exception("Error generando imagen para capítulo %d", idx+1)

        final = story.model_dump()
        logger.info("Imagenes generadas, preparando final_output")
        return {"final_output": final}
    except Exception:
        logger.exception("Error en image_generation_node")
        raise

# Build graph
logger.info("Construyendo workflow graph...")
workflow = StateGraph(StoryState)
workflow.add_node("generate_story", story_generation_node)
workflow.add_node("generate_images", image_generation_node)
workflow.add_edge(START, "generate_story")
workflow.add_edge("generate_story", "generate_images")
workflow.add_edge("generate_images", END)

graph = workflow.compile()
logger.info("Workflow compilado correctamente")

logger.info("Invocando workflow...")
_reset_image_tool_state()
try:
    result = graph.invoke({
        "messages": [{"role": "user", "content": "Write a 3-chapter fantasy story about dragons"}]
    })
    logger.info("Workflow finalizado correctamente")
    logger.debug("Workflow raw result: %s", str(result)[:2000])
except Exception:
    logger.exception("Error al invocar el workflow")
    result = {"final_output": None}

# Guardar resultado estructurado en output.json (UTF-8, legible)
final = result.get("final_output", result)
output_path = "output.json"
try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    logger.info("Resultado guardado en %s", output_path)
    print(f"Resultado guardado en {output_path}")
except Exception:
    logger.exception("Error guardando el resultado en %s", output_path)