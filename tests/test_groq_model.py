import json
from pathlib import Path
import runpy

import dotenv
import groq
import httpx
import pytest

from api.agents import story_agent as agents
from api.core.config import GROQ_MODEL


@pytest.mark.parametrize("value", [None, "", "  ", "custom-groq-model"])
def test_groq_model_configuration(monkeypatch, value):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda: None)
    monkeypatch.delenv("GROQ_MODEL", raising=False)
    if value is not None:
        monkeypatch.setenv("GROQ_MODEL", value)
    config_path = Path(__file__).resolve().parents[1] / "api/core/config.py"
    config = runpy.run_path(str(config_path))
    assert config["GROQ_MODEL"] == (value.strip() if value and value.strip() else "openai/gpt-oss-120b")


def test_groq_requests_use_configured_model_and_parse_story(monkeypatch):
    requests = []
    story = {"title": "La nube", "chapters": [{"title": "Un amigo", "content": "Una nube encontró un amigo."}]}

    def respond(request):
        payload = json.loads(request.content)
        requests.append(payload)
        content = json.dumps(story) if payload.get("response_format") else "A friendly cloud in a storybook sky."
        return httpx.Response(200, json={
            "id": "chatcmpl-test", "object": "chat.completion", "created": 0,
            "model": GROQ_MODEL,
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": content}}],
        })

    with httpx.Client(transport=httpx.MockTransport(respond)) as http_client:
        client = groq.Groq(api_key="test-key", http_client=http_client)
        monkeypatch.setattr(agents.story_llm, "client", client.chat.completions)
        monkeypatch.setattr(agents.image_llm, "client", client.chat.completions)
        result = agents.story_generation_node({
            "messages": [{"role": "user", "content": "Escribe un cuento sobre una nube."}],
            "num_chapters": 1, "language": "es",
        })
        image_prompt = agents.make_image_prompt("Una nube encontró un amigo.", lang="es")

    assert result["story_data"].title == "La nube"
    assert len(result["story_data"].chapters) == 1
    assert image_prompt == "A friendly cloud in a storybook sky."
    assert len(requests) == 2
    assert all(request["model"] == GROQ_MODEL for request in requests)
    assert requests[0]["response_format"] == {"type": "json_object"}
