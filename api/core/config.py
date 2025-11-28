import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env para desarrollo local
load_dotenv()

# URL de Redis para Celery y Health Checks
REDIS_URL = os.getenv("REDIS_URL")

# Credenciales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Credenciales de Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Podríamos añadir validaciones aquí para asegurar que las variables críticas estén definidas
# Por ejemplo:
# if not SUPABASE_URL or not SUPABASE_ANON_KEY:
#     raise ValueError("Las variables de entorno de Supabase son obligatorias")
