from fastapi import APIRouter
from celery.result import AsyncResult

router = APIRouter()

@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    Devuelve el estado y el resultado de una tarea de Celery.
    """
    task_result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task_result.status,
        "result": None,
        "error": None
    }

    if task_result.successful():
        response["result"] = task_result.result
    elif task_result.failed():
        response["error"] = str(task_result.info)  # .info contiene la excepción

    return response
