import asyncio
import threading
import queue
import logging
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from speechmatics.client import WebsocketClient
from speechmatics.models import (
    ConnectionSettings, 
    TranscriptionConfig, 
    AudioSettings, 
    ServerMessageType
)
from api.core.dependencies import get_authenticated_socket_user
from api.services.user_service import UserProfile

router = APIRouter()
logger = logging.getLogger(__name__)

# Generator para pasar el stream de audio al cliente de Speechmatics de forma síncrona
class StreamGenerator:
    """
    Puente entre la entrada asíncrona del WebSocket (escritor de cola)
    y el cliente síncrono de Speechmatics (lector iterador).
    """
    def __init__(self):
        self._queue = queue.Queue()
        self._ended = False

    def add_chunk(self, chunk: bytes):
        self._queue.put(chunk)

    def close(self):
        self._ended = True
        self._queue.put(None)  # Sentinel to unblock

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self._queue.get()
        if chunk is None:
            raise StopIteration
        return chunk

@router.websocket("/transcribe")
async def websocket_transcription(
    websocket: WebSocket,
    user: UserProfile = Depends(get_authenticated_socket_user)
):
    await websocket.accept()
    logger.info(f"Usuario {user.id} conectado al servicio de transcripción")
    
    API_KEY = os.getenv("SPEECHMATICS_API_KEY")
    if not API_KEY:
        logger.error("SPEECHMATICS_API_KEY no configurada")
        await websocket.close(code=1011)
        return

    CONNECTION_URL = "wss://eu.rt.speechmatics.com/v2"
    LANGUAGE = "en" 

    # Configuración del puente y loop principal
    stream = StreamGenerator()
    loop = asyncio.get_event_loop()
    
    # Handlers de Speechmatics (se ejecutan en otro thread)
    def on_text(msg):
        """Handler para transcripciones finales"""
        try:
            text = msg['metadata']['transcript']
            payload = {"type": "final", "text": text}
            asyncio.run_coroutine_threadsafe(websocket.send_json(payload), loop)
        except Exception as e:
            logger.error(f"Error en on_text: {e}")

    def on_partial(msg):
        """Handler para transcripciones parciales"""
        try:
            text = msg['metadata']['transcript']
            payload = {"type": "partial", "text": text}
            asyncio.run_coroutine_threadsafe(websocket.send_json(payload), loop)
        except Exception as e:
            logger.error(f"Error en on_partial: {e}")

    def on_error(msg):
        logger.error(f"Speechmatics Error: {msg}")

    # Configuración del cliente Speechmatics
    settings = ConnectionSettings(
        url=CONNECTION_URL,
        auth_token=API_KEY,
    )

    # Configuración optimizada para "Open Story"
    # operating_point="enhanced" para mejor calidad
    # enable_partials=True para feedback en tiempo real
    conf = TranscriptionConfig(
        language=LANGUAGE,
        operating_point="enhanced", 
        enable_partials=True, 
        max_delay=2 
    )
    
    # Speechmatics maneja raw streams si vienen correctamente codificados, 
    # pero webm/ogg suele funcionar bien si se envía el stream completo con header.
    audio_conf = AudioSettings() 

    sm_client = WebsocketClient(settings)
    sm_client.add_event_handler(ServerMessageType.AddTranscript, on_text)
    sm_client.add_event_handler(ServerMessageType.AddPartialTranscript, on_partial)
    sm_client.add_event_handler(ServerMessageType.Error, on_error)

    # Ejecutar cliente en un thread separado (bloqueante)
    def run_sm_client():
        try:
            sm_client.run_synchronously(stream, conf, audio_conf)
        except Exception as e:
            logger.error(f"Transcription thread failed: {e}")

    thread = threading.Thread(target=run_sm_client)
    thread.start()

    # Loop principal async (Recibir audio del cliente)
    try:
        while True:
            data = await websocket.receive_bytes()
            stream.add_chunk(data)
    except WebSocketDisconnect:
        logger.info(f"Cliente {user.id} desconectado")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        stream.close()
        thread.join(timeout=2.0)
