import os
import sys
import pytest
from unittest.mock import MagicMock
from api.agents import Story

# Add the project root to PYTHONPATH so we can import 'api'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Set fake env vars for testing to avoid missing key errors."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fake-openai-key")
    monkeypatch.setenv("GROQ_API_KEY", "gsk_fake_groq_key")
    monkeypatch.setenv("SUPABASE_URL", "https://fake.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "fake-key")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "fake-anon-key")
    monkeypatch.setenv("SUPABASE_PROJECT_REF", "fake-project")

@pytest.fixture
def mock_story_agent():
    """Mock the story generation LLM agent."""
    mock_agent = MagicMock()
    # Create a real Story object for the mock to return
    # This passes the isinstance(story, Story) check in the code
    story_data = Story(
        title="Test Story",
        chapters=[
            {"title": "Chapter 1", "content": "Content 1"},
            {"title": "Chapter 2", "content": "Content 2"},
            {"title": "Chapter 3", "content": "Content 3"},
        ]
    )
    mock_agent.invoke.return_value = story_data
    return mock_agent
