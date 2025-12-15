import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

# Allow running this file directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock
from api.agents.story_agent import story_generation_node
from api.agents.utils import Story, StoryState
from api.prompts.story_prompts import STORY_SYSTEM_PROMPT

# ============================================================================
# UNIT TESTS (MOCKED)
# ============================================================================

def test_story_generation_node_success(mock_story_agent):
    """Test story generation with mocked agent response."""
    logger.info(">>> TEST START: test_story_generation_node_success")
    
    # Mock the 'story_agent' imported in api.agents.story_agent
    with patch("api.agents.story_agent.story_agent", mock_story_agent):
        state = StoryState(
            messages=[{"role": "user", "content": "Write a story about a brave toaster"}],
            story_data=None,
            final_output=None,
            user_id="test_user",
            jwt_token="fake_token",
            model="dall-e-3"
        )
        
        logger.info(f"Invoking story_generation_node with state: {state}")
        result = story_generation_node(state)
        
        logger.info(f"Node result: {result}")
        
        assert "story_data" in result
        story = result["story_data"]
        
        logger.info(f"Generated Story Title: {story.title}")
        logger.info(f"Chapter count: {len(story.chapters)}")
        
        # Allow checking against the MagicMock or actual Pydantic model depending on how patch works
        assert story.title == "Test Story"
        assert len(story.chapters) == 3
        
    logger.info("<<< TEST PASS: test_story_generation_node_success")

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
    logger.info(">>> TEST START: test_real_story_generation_integration")
    
    # Ensure real keys are present
    if not os.getenv("GROQ_API_KEY"):
        pytest.fail("GROQ_API_KEY must be set for integration tests")

    # Import the real agent (it's already configured with the real key if env var is set)
    from api.agents.story_agent import story_agent
    
    messages = [
        {"role": "user", "content": "Write a very short 1-chapter story about a happy cloud."}
    ]
    
    # We might need to override the prompt temporarly to ask for fewer chapters if we want speed,
    # but the agent is configured globally. Let's just run it as is.
    
    try:
        logger.info("Invoking real story_agent (Groq)...")
        # Must include 'json' in prompt for json_mode to work (STORY_SYSTEM_PROMPT has it)
        system_msg = {"role": "system", "content": STORY_SYSTEM_PROMPT}
        user_msg = {"role": "user", "content": "Write a micro story about a cat."}
        
        response = story_agent.invoke([system_msg, user_msg])
        
        assert isinstance(response, Story)
        assert len(response.chapters) > 0
        assert response.title is not None
        
        logger.info(f"[Integration] Generated Story: {response.title}")
        logger.info(f"[Integration] Chapters: {len(response.chapters)}")
        
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        pytest.fail(f"Integration test failed: {e}")
        
    logger.info("<<< TEST PASS: test_real_story_generation_integration")

if __name__ == "__main__":
    # When running directly (e.g. from IDE "Run" button), invoke pytest with -s to show logs
    sys.exit(pytest.main(["-s", __file__]))
