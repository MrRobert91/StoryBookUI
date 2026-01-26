from celery import Celery
import os
import asyncio
from asgiref.sync import async_to_sync
import json
from api.celery_tasks.app import celery_app
from api.agents.story_agent import graph, StoryState
from supabase import create_client
import logging

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
def generate_story_task(self, topic: str, user_id: str, jwt_token: str, model: str | None = None, image_style_context: str | None = None):
    task_id = self.request.id
    logger.info(f" [Task {task_id}] RECEIVED by worker.")
    logger.info(f" [Task {task_id}] INPUT -> User: {user_id} | Topic: '{topic}' | Model: {model} | Style Context: {bool(image_style_context)}")
    
    try:
        # 1. Invocar Workflow
        logger.info(f"🤖 [Task {task_id}] Invoking LangGraph workflow...")
        result = graph.invoke({
            "messages": [{"role": "user", "content": topic}],
            "user_id": user_id,
            "jwt_token": jwt_token,
            "model": model,
            "image_style_context": image_style_context
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
        
        # 2b. Generar PDF y subir a Supabase
        pdf_url = None
        try:
            from api.services.pdf_service import generate_story_pdf
            logger.info(f" [Task {task_id}] Generando PDF del cuento...")
            pdf_bytes = generate_story_pdf(story_json)
            
            logger.info(f" [Task {task_id}] PDF generado. Tipo: {type(pdf_bytes)}, Tamaño: {len(pdf_bytes)} bytes")
            
            pdf_filename = f"{user_id}/{task_id}.pdf"
            bucket_name = "cuentee_pdfs"

            if supabase_admin:
                logger.info(f" [Task {task_id}] Subiendo PDF a bucket '{bucket_name}' como '{pdf_filename}'...")
                
                # Upload
                # Note: 'upsert' option might be needed if overwriting, but task_id is unique enough.
                # In python supabase client, storage.from_().upload() takes file bytes.
                res = supabase_admin.storage.from_(bucket_name).upload(
                    path=pdf_filename,
                    file=pdf_bytes,
                    file_options={"content-type": "application/pdf", "upsert": "true"}
                )
                
                # Get Public URL
                # Assuming bucket is public. If private, we'd need create_signed_url every time or just store path.
                # For this implementation, we try to get public URL.
                public_url_resp = supabase_admin.storage.from_(bucket_name).get_public_url(pdf_filename)
                pdf_url = public_url_resp
                
                logger.info(f" [Task {task_id}] PDF subido exitosamente. URL: {pdf_url}")
                
                # Add to story structure to be saved in DB
                story_json["pdf_url"] = pdf_url
            else:
                logger.warning(f" [Task {task_id}] No se pudo subir PDF (Supabase client missing).")

        except Exception as pdf_err:
            logger.error(f" [Task {task_id}] ERROR Generando/Subiendo PDF: {pdf_err}", exc_info=True)
            # No fallamos la tarea entera si solo falla el PDF, pero lo logueamos.

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
        
        logger.info(f"🏁 [Task {task_id}] FINISHED successfully. PDF URL: {pdf_url}")
        return story_json
        
    except Exception as e:
        logger.error(f"🔥 [Task {task_id}] CRITICAL FAILURE: {str(e)}", exc_info=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)
