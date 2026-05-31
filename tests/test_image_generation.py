import base64
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from api.agents import utils


def test_gpt_image_2_uses_low_quality_and_base64_upload():
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
    assert params["model"] == "gpt-image-2-2026-04-21"
    assert params["quality"] == "low"
    mock_upload.assert_called_once_with(b"fake-image-data", "cover")
