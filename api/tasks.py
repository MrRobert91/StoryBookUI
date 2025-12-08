import os
import json
import logging
from api.celery_app import celery_app
from api.agents_test import graph
from supabase import create_client

# Configurar logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase_admin = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
else:
    logger.warning("⚠️ SUPABASE CREDENTIALS NOT FOUND. Database operations will fail.")

@celery_app.task(bind=True, name="generate_story_task")
def generate_story_task(self, topic: str, user_id: str, jwt_token: str, model: str | None = None):
    task_id = self.request.id
    logger.info(f" [Task {task_id}] RECEIVED by worker.")
    logger.info(f" [Task {task_id}] INPUT -> User: {user_id} | Topic: '{topic}' | Model: {model}")
    
    try:
        # 1. Invocar Workflow
        logger.info(f"🤖 [Task {task_id}] Invoking LangGraph workflow...")
        result = graph.invoke({
            "messages": [{"role": "user", "content": topic}],
            "user_id": user_id,
            "jwt_token": jwt_token,
            "model": model
        })
        
        story_data = result.get("story_data")
        
        if not story_data:
            logger.error(f" [Task {task_id}] Workflow finished but returned NO story_data.")
            raise ValueError("No story data generated")
            
        # Convertir a dict si es modelo Pydantic
        story_json = story_data.dict() if hasattr(story_data, "dict") else story_data
        
        # Log del resultado generado
        title = story_json.get("title", "Untitled")
        chapters = story_json.get("chapters", [])
        logger.info(f" [Task {task_id}] GENERATION SUCCESS -> Title: '{title}' | Chapters: {len(chapters)}")
        logger.info(f" [Task {task_id}] Story Preview: {json.dumps(story_json, indent=2)[:500]}...") # Muestra los primeros 500 caracteres
        
        # 2. Guardar en Base de Datos
        if supabase_admin:
            logger.info(f"💾 [Task {task_id}] Saving to Supabase 'stories' table...")
            try:
                db_response = supabase_admin.table("stories").insert({
                    "user_id": user_id,
                    "title": title,
                    "content": json.dumps(story_json),
                    "prompt": topic,
                }).execute()
                
                logger.info(f" [Task {task_id}] Story saved to DB. ID: {db_response.data[0].get('id') if db_response.data else 'Unknown'}")
                
                # 3. Descontar Créditos
                logger.info(f" [Task {task_id}] Checking user credits...")
                resp = supabase_admin.table("profiles").select("credits").eq("id", user_id).single().execute()
                
                if resp.data:
                    current_credits = resp.data.get("credits", 0)
                    logger.info(f" [Task {task_id}] Current credits: {current_credits}")
                    
                    if current_credits > 0:
                        new_credits = current_credits - 1
                        supabase_admin.table("profiles").update({"credits": new_credits}).eq("id", user_id).execute()
                        logger.info(f" [Task {task_id}] Credits deducted. New balance: {new_credits}")
                    else:
                        logger.warning(f" [Task {task_id}] User has 0 credits but task ran (Check API validation).")
                else:
                    logger.warning(f" [Task {task_id}] User profile not found for credits deduction.")
                
            except Exception as db_err:
                logger.error(f" [Task {task_id}] DATABASE ERROR: {str(db_err)}")
                # No relanzamos aquí para no perder el resultado generado si solo falló el guardado, 
                # aunque idealmente debería ser transaccional.
                raise db_err
        else:
            logger.error(f" [Task {task_id}] Skipping DB save (Supabase client not initialized)")
        
        logger.info(f"🏁 [Task {task_id}] FINISHED successfully.")
        return story_json
        
    except Exception as e:
        logger.error(f"🔥 [Task {task_id}] CRITICAL FAILURE: {str(e)}", exc_info=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)
