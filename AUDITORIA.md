# Informe de Auditoría y Mejoras de Código

Este documento detalla un análisis del repositorio con el objetivo de identificar áreas de mejora en cuanto a simplicidad, mantenibilidad, seguridad y estructura del código.

## 1. API (Backend - FastAPI)

La API presenta varias oportunidades de mejora para hacerla más robusta, segura y mantenible.

### 1.1. Complejidad y Duplicación de Código

-   **Causa**: Existe una considerable duplicación de lógica en los endpoints de `api/main.py` (`/generate-story-ai-jwt`, `/generate-story-ai-images-jwt`, etc.). La autenticación de usuarios, la verificación de créditos y la inicialización del cliente de Groq se repiten en cada endpoint protegido.
-   **Solución Propuesta**:
    -   **Centralizar la lógica de negocio**: Crear una capa de "servicios" que abstraiga la lógica de negocio (ej. `services/user_service.py` para gestionar créditos, `services/story_service.py` para la generación de cuentos).
    -   **Usar Dependencias de FastAPI**: Refactorizar la lógica de autenticación y obtención del usuario en una dependencia de FastAPI. Esto permite inyectar el usuario autenticado y verificado directamente en los endpoints, eliminando código repetido.

    ```python
    # Ejemplo de dependencia en un nuevo archivo (ej. api/dependencies.py)
    from fastapi import Depends, HTTPException, Header
    from .services import user_service

    async def get_current_user(authorization: str = Header(...)):
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")
        token = authorization.split(" ")[1]
        user_id = user_service.verify_jwt(token) # Asumiendo que movemos la lógica de JWT a un servicio
        # ... (lógica para obtener el perfil del usuario)
        return user_profile
    ```

### 1.2. Estructura y Modularidad

-   **Causa**: Toda la lógica de la API reside en un único archivo, `api/main.py`. Esto dificulta la navegación y el mantenimiento a medida que la aplicación crece.
-   **Solución Propuesta**:
    -   **Utilizar APIRouter**: Dividir los endpoints en routers lógicos. Por ejemplo, crear `api/routers/stories.py` para todo lo relacionado con la generación de cuentos y `api/routers/tasks.py` para la gestión de tareas de Celery.
    -   **Organizar por carpetas**: Crear una estructura de carpetas clara:
        ```
        api/
        ├── routers/
        │   ├── stories.py
        │   └── tasks.py
        ├── services/
        │   ├── user_service.py
        │   └── story_service.py
        ├── core/
        │   └── config.py  # Para gestionar la configuración y variables de entorno
        └── main.py       # Punto de entrada principal que incluye los routers
        ```

### 1.3. Seguridad

-   **Causa**: Las dependencias en `api/requirements.txt` no tienen versiones fijadas. Esto introduce riesgos de seguridad ("supply chain attacks") y problemas de reproducibilidad, ya que `pip install` podría instalar una versión con una vulnerabilidad o un "breaking change".
-   **Solución Propuesta**:
    -   **Fijar Versiones**: Generar un `requirements.txt` con versiones exactas (ej. `fastapi==0.110.0`). Se puede generar con `pip freeze > requirements.txt`.
    -   **Auditoría de Dependencias**: Integrar herramientas de auditoría como `pip-audit` o Snyk en el flujo de CI/CD para escanear dependencias en busca de vulnerabilidades conocidas.

-   **Causa**: El endpoint `/generate-story` es un endpoint de prueba que no requiere autenticación y devuelve datos predecibles. Podría ser eliminado para reducir la superficie de ataque.
-   **Solución Propuesta**: Eliminar el endpoint `/generate-story` de `api/main.py`.

-   **Causa**: Algunos mensajes de error devuelven información interna que podría ser explotada por un atacante.
-   **Solución Propuesta**: Estandarizar el manejo de errores para devolver mensajes genéricos al cliente mientras se registran los detalles completos en el servidor.

## 2. Frontend (Next.js)

El frontend también tiene puntos clave de mejora, especialmente en la calidad del código y la seguridad.

### 2.1. Calidad de Código y Proceso de Build

-   **Causa**: El archivo `frontend/next.config.mjs` contiene las siguientes líneas, que permiten que el proyecto se construya y despliegue incluso con errores de código:
    ```javascript
    eslint: { ignoreDuringBuilds: true },
    typescript: { ignoreBuildErrors: true },
    ```
-   **Solución Propuesta**: **Eliminar estas dos configuraciones**. Forzar la corrección de errores de ESLint y TypeScript durante el build es una práctica fundamental para mantener la calidad y evitar bugs en producción.

### 2.2. Seguridad de Dependencias

-   **Causa**: Al igual que en el backend, el archivo `frontend/package.json` usa versiones flexibles (`latest`, `^`).
-   **Solución Propuesta**:
    -   **Fijar Versiones**: Usar versiones exactas para todas las dependencias. Se puede usar un archivo `package-lock.json` o `yarn.lock` para asegurar builds deterministas.
    -   **Auditoría de Dependencias**: Ejecutar `npm audit` o `yarn audit` regularmente para detectar y corregir vulnerabilidades en el árbol de dependencias.

### 2.3. Validación de Entradas

-   **Causa**: La validación en las Server Actions (`frontend/lib/actions.ts`) es muy básica. No valida el formato del email ni la fortaleza de la contraseña.
-   **Solución Propuesta**:
    -   **Usar una librería de validación**: Integrar `zod` para definir esquemas de validación robustos para los datos de los formularios. Esto previene datos malformados y mejora la seguridad.
    ```typescript
    // Ejemplo con Zod
    import { z } from "zod";

    const loginSchema = z.object({
      email: z.string().email("Invalid email format"),
      password: z.string().min(8, "Password must be at least 8 characters long"),
    });

    // En la Server Action
    const validatedFields = loginSchema.safeParse({ email, password });
    if (!validatedFields.success) {
      return { error: "Invalid fields." };
    }
    ```

### 2.4. Código Obsoleto

-   **Causa**: La función `signOut` en `actions.ts` tiene un comentario que indica que ya no se utiliza.
-   **Solución Propuesta**: Confirmar si la función está en uso. Si no lo está, eliminarla para mantener el código limpio.

## 3. Configuración de Contenedores (Docker)

La configuración de Docker puede mejorarse significativamente para aumentar la seguridad y optimizar las imágenes.

### 3.1. Seguridad del Contenedor

-   **Causa**: El `api/Dockerfile` ejecuta la aplicación como usuario `root`. Si un atacante compromete la aplicación, obtendrá privilegios de `root` dentro del contenedor.
-   **Solución Propuesta**: Crear y usar un usuario no privilegiado en el `Dockerfile`.

    ```dockerfile
    # Al final del Dockerfile
    RUN groupadd -r appuser && useradd -r -g appuser appuser
    USER appuser

    CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

### 3.2. Optimización de la Imagen

-   **Causa**: El comando `COPY . ./api/` en el `api/Dockerfile` copia todo el contenido del directorio, lo que puede incluir archivos innecesarios (tests, configuraciones locales, etc.), aumentando el tamaño de la imagen.
-   **Solución Propuesta**:
    -   **Usar `.dockerignore`**: Crear un archivo `.dockerignore` en el directorio `api/` para excluir archivos y carpetas innecesarios.
    -   **Copiar selectivamente**: Ser más específico en los comandos `COPY` para incluir solo lo necesario para ejecutar la aplicación.

### 3.3. Seguridad de la Imagen Base

-   **Causa**: La imagen base `python:3.11-slim` se obtiene por su etiqueta, no por su `digest` (hash SHA256). Esto significa que la imagen puede cambiar sin previo aviso si la etiqueta se actualiza.
-   **Solución Propuesta**: Especificar la imagen base usando su `digest` para garantizar builds reproducibles y seguros.

    ```dockerfile
    # Ejemplo
    FROM python:3.11-slim@sha256:abcdef123456...
    ```
