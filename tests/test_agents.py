import os
import sys

# Allow running this file directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock
from api.agents import story_generation_node, StoryState, Story

# ============================================================================
# UNIT TESTS (MOCKED)
# ============================================================================

def test_story_generation_node_success(mock_story_agent):
    """Test story generation with mocked agent response."""
    
    # Mock the 'story_agent' imported in api.agents
    with patch("api.agents.story_agent", mock_story_agent):
        state = StoryState(
            messages=[{"role": "user", "content": "Write a story about a brave toaster"}],
            story_data=None,
            final_output=None,
            user_id="test_user",
            jwt_token="fake_token",
            model="dall-e-3"
        )
        
        result = story_generation_node(state)
        
        assert "story_data" in result
        story = result["story_data"]
        # Allow checking against the MagicMock or actual Pydantic model depending on how patch works
        assert story.title == "Test Story"
        assert len(story.chapters) == 3

# ============================================================================
# INTEGRATION TESTS (REAL API CALLS)
# ============================================================================

# To run these: set RUN_REAL_API_TESTS=true in environment
@pytest.mark.skipif(
    os.getenv("RUN_REAL_API_TESTS") != "true",
    reason="Skipping real API integration tests. Set RUN_REAL_API_TESTS=true to enable."
)
def test_real_story_generation_integration():
    """Verify we can actually talk to Groq and get a structured response."""
    # Ensure real keys are present
    if not os.getenv("GROQ_API_KEY"):
        pytest.fail("GROQ_API_KEY must be set for integration tests")

    # Import the real agent (it's already configured with the real key if env var is set)
    from api.agents import story_agent
    
    messages = [
        {"role": "user", "content": "Write a very short 1-chapter story about a happy cloud."}
    ]
    
    # We might need to override the prompt temporarly to ask for fewer chapters if we want speed,
    # but the agent is configured globally. Let's just run it as is.
    
    try:
        response = story_agent.invoke([{"role": "user", "content": "Write a micro story about a cat."}])
        
        assert isinstance(response, Story)
        assert len(response.chapters) > 0
        assert response.title is not None
        print(f"\n[Integration] Generated Story: {response.title}")
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")
