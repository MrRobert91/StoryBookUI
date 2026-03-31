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
def generate_story_task(self, topic: str, user_id: str, jwt_token: str, model: str | None = None, image_style_context: str | None = None, num_chapters: int | None = None, story_type: str = "open", metadata: dict = None):
    task_id = self.request.id
    logger.info(f" [Task {task_id}] RECEIVED by worker.")
    logger.info(f" [Task {task_id}] INPUT -> User: {user_id} | Topic: '{topic}' | Model: {model} | Style Context: {bool(image_style_context)} | Chapters: {num_chapters}")
    
    try:
        # 1. Invocar Workflow
        logger.info(f"🤖 [Task {task_id}] Invoking LangGraph workflow...")
        
        from langchain_core.runnables import RunnableConfig
        from langsmith import traceable
        
        # Normalize metadata for LangSmith filters
        run_metadata = {
            "agent_name": "story_agent",
            "story_type": story_type,
            "topic": topic,
            "user_id": user_id,
            "num_chapters": num_chapters,
            "language": (metadata or {}).get("language", "en"),
            "model": model or "llama-3.3-70b-versatile",
            "image_style": bool(image_style_context),
            "story_id": str(task_id)
        }
        if metadata:
            run_metadata.update(metadata)
            
        config = RunnableConfig(
            run_name="Story Generation Root",
            metadata=run_metadata
        )
        
        result = graph.invoke({
            "messages": [{"role": "user", "content": topic}],
            "user_id": user_id,
            "jwt_token": jwt_token,
            "model": model,
            "image_style_context": image_style_context,
            "num_chapters": num_chapters,
            "story_type": story_type,
            "metadata": run_metadata,
            "language": run_metadata.get("language")
        }, config=config)
        
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
        logger.info(f" [Task {task_id}] Story Preview: {json.dumps(story_json, indent=2)[:500]}...")
        
        @traceable(run_type="chain", name="postprocessing", tags=["postprocessing"])
        def process_post_generation(story_output, user_id_str, task_id_str, topic_str, story_type_str, meta):
            pdf_url = None
            try:
                from api.services.pdf_service import generate_story_pdf
                logger.info(f" [Task {task_id_str}] Generando PDF del cuento...")
                pdf_bytes = generate_story_pdf(story_output)
                
                logger.info(f" [Task {task_id_str}] PDF generado. Tipo: {type(pdf_bytes)}, Tamaño: {len(pdf_bytes)} bytes")
                
                pdf_filename = f"{user_id_str}/{task_id_str}.pdf"
                bucket_name = "cuentee_pdfs"

                if supabase_admin:
                    logger.info(f" [Task {task_id_str}] Subiendo PDF a bucket '{bucket_name}' como '{pdf_filename}'...")
                    
                    res = supabase_admin.storage.from_(bucket_name).upload(
                        path=pdf_filename,
                        file=pdf_bytes,
                        file_options={"content-type": "application/pdf", "upsert": "true"}
                    )
                    
                    public_url_resp = supabase_admin.storage.from_(bucket_name).get_public_url(pdf_filename)
                    pdf_url = public_url_resp
                    
                    logger.info(f" [Task {task_id_str}] PDF subido exitosamente. URL: {pdf_url}")
                    story_output["pdf_url"] = pdf_url
                else:
                    logger.warning(f" [Task {task_id_str}] No se pudo subir PDF (Supabase client missing).")

            except Exception as pdf_err:
                logger.error(f" [Task {task_id_str}] ERROR Generando/Subiendo PDF: {pdf_err}", exc_info=True)

            # 2. Guardar en Base de Datos
            db_res = None
            if supabase_admin:
                logger.info(f"💾 [Task {task_id_str}] Saving to Supabase 'stories' table...")
                try:
                    db_response = supabase_admin.table("stories").insert({
                        "user_id": user_id_str,
                        "title": story_output.get("title", "Untitled"),
                        "content": json.dumps(story_output),
                        "prompt": topic_str,
                        "story_type": story_type_str,
                        "metadata": meta or {}
                    }).execute()
                    
                    logger.info(f" [Task {task_id_str}] Story saved to DB. ID: {db_response.data[0].get('id') if db_response.data else 'Unknown'}")
                    db_res = db_response.data[0] if db_response.data else None
                    
                    # 3. Descontar Créditos
                    logger.info(f" [Task {task_id_str}] Checking user credits...")
                    resp = supabase_admin.table("profiles").select("credits").eq("id", user_id_str).single().execute()
                    
                    if resp.data:
                        current_credits = resp.data.get("credits", 0)
                        logger.info(f" [Task {task_id_str}] Current credits: {current_credits}")
                        
                        if current_credits > 0:
                            new_credits = current_credits - 1
                            supabase_admin.table("profiles").update({"credits": new_credits}).eq("id", user_id_str).execute()
                            logger.info(f" [Task {task_id_str}] Credits deducted. New balance: {new_credits}")
                        else:
                            logger.warning(f" [Task {task_id_str}] User has 0 credits but task ran (Check API validation).")
                    else:
                        logger.warning(f" [Task {task_id_str}] User profile not found for credits deduction.")
                    
                except Exception as db_err:
                    logger.error(f" [Task {task_id_str}] DATABASE ERROR: {str(db_err)}")
                    raise db_err
            else:
                logger.error(f" [Task {task_id_str}] Skipping DB save (Supabase client not initialized)")
            
            return {"pdf_url": pdf_url, "db_response": db_res}

        # Ejecutar postprocessing
        post_result = process_post_generation(story_json, user_id, task_id, topic, story_type, run_metadata)
        
        logger.info(f"🏁 [Task {task_id}] FINISHED successfully. PDF URL: {post_result.get('pdf_url')}")
        return story_json
        
    except Exception as e:
        logger.error(f"🔥 [Task {task_id}] CRITICAL FAILURE: {str(e)}", exc_info=True)
        raise self.retry(exc=e, countdown=60, max_retries=3)

