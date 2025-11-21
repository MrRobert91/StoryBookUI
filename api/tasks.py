import os
import json
import logging
from api.celery_app import celery_app
from api.agents_test import graph
from supabase import create_client

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase_admin = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

@celery_app.task(bind=True, name="generate_story_task")
def generate_story_task(self, topic: str, user_id: str, jwt_token: str, model: str = "dall-e-3"):
    logger.info(f"Starting story generation for user {user_id} with topic: {topic}")
    
    try:
        # Invoke LangGraph workflow
        result = graph.invoke({
            "messages": [("user", topic)],
            "user_id": user_id,
            "jwt_token": jwt_token,
            "model": model
        })
        
        story_data = result.get("story_data")
        if not story_data:
            raise ValueError("No story data generated")
            
        # Convert to dict if it's a Pydantic model
        story_json = story_data.dict() if hasattr(story_data, "dict") else story_data
        
        # Save to database
        if supabase_admin:
            try:
                supabase_admin.table("stories").insert({
                    "user_id": user_id,
                    "title": story_json.get("title"),
                    "content": json.dumps(story_json),
                    "prompt": topic,
                }).execute()
                
                # Deduct credits
                resp = supabase_admin.table("profiles").select("credits").eq("id", user_id).single().execute()
                if resp.data:
                    current_credits = resp.data.get("credits", 0)
                    if current_credits > 0:
                        supabase_admin.table("profiles").update({"credits": current_credits - 1}).eq("id", user_id).execute()
                    else:
                        logger.warning(f"User {user_id} has 0 credits but task ran.")
                
            except Exception as e:
                logger.error(f"Error saving story or updating credits: {str(e)}")
        
        return story_json
        
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
