import base64
import json
from pathlib import Path
import runpy
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import dotenv
import httpx
from openai import OpenAI
import pytest

from api.agents import utils


def load_image_config(monkeypatch, value):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda: None)
    monkeypatch.delenv("IMAGE_MODEL", raising=False)
    if value is not None:
        monkeypatch.setenv("IMAGE_MODEL", value)
    return runpy.run_path(str(Path(__file__).resolve().parents[1] / "api/core/config.py"))


@pytest.mark.parametrize("value", [None, "", "  "])
def test_image_model_defaults(monkeypatch, value):
    assert load_image_config(monkeypatch, value)["IMAGE_MODEL"] == "gpt-image-2-2026-04-21"


def test_invalid_image_model_fails_at_startup(monkeypatch):
    with pytest.raises(ValueError, match="Unsupported IMAGE_MODEL"):
        load_image_config(monkeypatch, "gpt-image-2.5-typo")


@pytest.mark.parametrize("model", [
    "gpt-image-1", "gpt-image-1-mini", "gpt-image-1.5",
    "gpt-image-2-2026-04-21", "gpt-image-2",
    "gpt-image-2.5-flare", "gpt-image-2.5-sunburst",
    "gpt-image-2.5-flare-2026-09-08", "gpt-image-2.5-sunburst-2026-09-08",
])
def test_environment_model_reaches_openai_sdk_and_base64_upload(monkeypatch, model):
    config = load_image_config(monkeypatch, f"  {model.upper()}  ")
    monkeypatch.setattr(utils, "IMAGE_MODEL", config["IMAGE_MODEL"])
    requests = []

    def respond(request):
        assert request.url.path == "/v1/images/generations"
        requests.append(json.loads(request.content))
        return httpx.Response(200, json={
            "created": 0,
            "data": [{"b64_json": base64.b64encode(b"fake-image-data").decode("ascii")}],
        })

    with (
        httpx.Client(transport=httpx.MockTransport(respond)) as http_client,
        patch.object(utils, "client", OpenAI(api_key="test-key", http_client=http_client)),
        patch.object(utils, "upload_image_bytes_to_supabase", return_value="https://example.test/image.png") as upload,
    ):
        image_url = utils.generate_image("A bright storybook castle", image_type="cover")

    assert image_url == "https://example.test/image.png"
    assert requests == [{
        "model": model, "quality": "low", "size": "1024x1024", "n": 1,
        "prompt": "A bright storybook castle",
    }]
    upload.assert_called_once_with(b"fake-image-data", "cover")


def test_legacy_override_cannot_replace_environment_model(monkeypatch, caplog):
    monkeypatch.setattr(utils, "IMAGE_MODEL", "gpt-image-2.5-sunburst")
    response = SimpleNamespace(
        data=[
            SimpleNamespace(
                b64_json=base64.b64encode(b"fake-image-data").decode("ascii")
            )
        ]
    )
    mock_generate = MagicMock(return_value=response)

    with (
        patch.object(utils.client.images, "generate", mock_generate),
        patch.object(utils, "upload_image_bytes_to_supabase", return_value="https://example.test/image.png") as mock_upload,
    ):
        image_url = utils.generate_image(
            "A bright storybook castle",
            model="gpt-image-2-2026-04-21",
            image_type="cover",
        )

    assert image_url == "https://example.test/image.png"
    mock_generate.assert_called_once()
    params = mock_generate.call_args.kwargs
    assert params["model"] == "gpt-image-2.5-sunburst"
    assert params["quality"] == "low"
    assert "Ignoring legacy image model override" in caplog.text
    mock_upload.assert_called_once_with(b"fake-image-data", "cover")


@pytest.mark.parametrize("value, expected", [
    ("dalle-3", "dall-e-3"), ("dall-e-3", "dall-e-3"),
    ("dalle-2", "dall-e-2"), ("dall-e-2", "dall-e-2"),
])
def test_legacy_dalle_environment_and_url_upload(monkeypatch, value, expected):
    config = load_image_config(monkeypatch, value)
    monkeypatch.setattr(utils, "IMAGE_MODEL", config["IMAGE_MODEL"])
    response = SimpleNamespace(data=[SimpleNamespace(url="https://example.test/generated.png")])
    with (
        patch.object(utils.client.images, "generate", return_value=response) as generate,
        patch.object(utils, "upload_to_supabase_storage", return_value="https://example.test/stored.png"),
    ):
        assert utils.generate_image("A castle", image_type="cover") == "https://example.test/stored.png"
    params = generate.call_args.kwargs
    assert params["model"] == expected
    assert "quality" not in params
    assert params.get("style") == ("vivid" if expected == "dall-e-3" else None)
