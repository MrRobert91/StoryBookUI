# Cómo funciona Cuentee por dentro: arquitectura de una plataforma de cuentos infantiles con IA

Cuentee es una aplicación full stack para generar cuentos infantiles personalizados con texto, ilustraciones, PDF final y persistencia en la nube. En esta rama, el sistema está construido sobre una separación bastante clara entre frontend, API, procesamiento asíncrono y almacenamiento, con Supabase como pieza transversal para autenticación, base de datos y ficheros.

La idea de producto es simple: un usuario autenticado describe una historia o completa un formulario guiado, el backend orquesta la generación con LLMs e imágenes, el resultado se guarda, se convierte a PDF y vuelve al frontend cuando el trabajo asíncrono termina. Lo interesante está en cómo se encadenan esas piezas.

## 1. Vista general de la arquitectura

El repositorio se divide en cuatro bloques principales:

- `frontend/`: aplicación Next.js 15 con App Router.
- `api/`: backend FastAPI con endpoints HTTP y WebSocket.
- `api/celery_tasks/`: workers de Celery para trabajos largos.
- `db/`: esquema SQL para Supabase/Postgres.

El flujo principal es este:

1. El usuario entra en la UI y se autentica con Supabase.
2. El frontend envía una petición al backend FastAPI con el JWT del usuario.
3. FastAPI valida identidad y créditos.
4. La API encola un trabajo en Celery.
5. El worker ejecuta un grafo de LangGraph:
   - genera la historia estructurada con Groq,
   - genera portada e ilustraciones con OpenAI,
   - sube imágenes a Supabase Storage.
6. Tras la generación, el worker:
   - compone un PDF,
   - lo sube a otro bucket de Supabase,
   - guarda la historia en la tabla `stories`,
   - descuenta un crédito del usuario.
7. Mientras tanto, el frontend hace polling del estado de la tarea hasta recibir el resultado final.

## 2. Frontend: Next.js como capa de experiencia

La aplicación web usa Next.js 15 con React 19 y App Router. No es un frontend “thin client”: además de renderizar páginas, controla sesión, estado de generación, internacionalización y algunas capacidades interactivas como entrada por voz.

### Layout y providers globales

En `frontend/app/layout.tsx` el árbol de la app se envuelve con dos providers:

- `AuthProvider`: hidrata la sesión de Supabase en cliente.
- `LanguageProvider`: resuelve traducciones desde JSON locales.

Eso hace que toda la UI pueda consultar:

- el usuario autenticado,
- el token de sesión,
- el idioma actual.

### Navegación del producto

La página principal (`frontend/app/page.tsx`) vende el producto como plataforma de creación de cuentos. La ruta `frontend/app/make-tale/page.tsx` actúa como selector de modo y obliga a estar autenticado antes de continuar.

Desde ahí hay dos experiencias:

- `open`: el usuario escribe un prompt libre.
- `guided`: el usuario rellena un formulario guiado con edad, protagonista, tema científico, misión y estilo visual.

Este detalle es importante porque en backend no existen dos sistemas completamente distintos. Lo que cambia es la forma de construir el prompt de entrada.

## 3. Autenticación y sesión con Supabase

El frontend usa `@supabase/ssr` para crear el cliente browser-side. La sesión se obtiene en cliente mediante `supabase.auth.getSession()` y el `access_token` se reenvía al backend en la cabecera:

```http
Authorization: Bearer <jwt>
```

En el backend, FastAPI extrae ese JWT en `api/core/dependencies.py` y delega la validación en `api/services/user_service.py`.

La verificación sigue este patrón:

1. Se crea un cliente Supabase “de usuario” con la anon key.
2. Se aplica el JWT al cliente PostgREST.
3. Se llama a `supabase.auth.get_user(token)`.
4. Se consulta la tabla `profiles` para obtener `credits` y `plan`.

De ahí sale el objeto `UserProfile`, que es la pieza con la que FastAPI ya trabaja en los endpoints protegidos.

En otras palabras, el backend no confía en datos enviados por el frontend sobre plan o créditos: siempre reconsulta Supabase.

## 4. El modelo de datos: historias, perfiles y RLS

El esquema en `db/schema.sql` define dos tablas principales:

- `stories`
- `profiles`

### Tabla `profiles`

Guarda:

- `id`
- `credits`
- `plan`
- `plus_since`
- `last_credited_at`

Además hay un trigger `handle_new_user()` que crea automáticamente el perfil cuando entra un nuevo usuario en `auth.users`.

### Tabla `stories`

Guarda:

- `user_id`
- `title`
- `content`
- `prompt`
- `story_type`
- `metadata`
- timestamps

La decisión relevante aquí es que `content` se almacena como texto, pero en la práctica contiene JSON serializado con la historia completa: título, portada, capítulos, imágenes y metadatos. Es una solución pragmática para prototipado rápido porque evita normalizar capítulos e imágenes en tablas separadas.

### Seguridad con RLS

Las políticas de Row Level Security limitan acceso a los propios datos del usuario:

- cada usuario puede leer sus historias,
- insertar las suyas,
- actualizarlas,
- borrarlas.

Eso convierte a Supabase en algo más que una base de datos: es también la frontera de seguridad de la aplicación.

## 5. La entrada al backend: FastAPI como fachada síncrona de un sistema asíncrono

El backend expone tres grupos de rutas:

- `/stories`
- `/tasks`
- `/transcription`

### Generación de historias

Los endpoints más importantes están en `api/routers/stories.py`:

- `POST /stories/generate-story-async`
- `POST /stories/generate_guided_story_async`

Ambos hacen lo mismo a alto nivel:

1. validan autenticación y créditos,
2. transforman la entrada en un prompt,
3. llaman a `generate_story_task.delay(...)`,
4. devuelven `task_id`.

La respuesta inmediata no contiene la historia. Solo devuelve algo como:

```json
{
  "task_id": "abc123",
  "status": "processing"
}
```

Esto evita mantener la conexión abierta durante generación de texto, imágenes, PDF y escritura en base de datos.

### Consulta de estado

El endpoint `GET /tasks/{task_id}` envuelve `AsyncResult(task_id)` de Celery y traduce el estado a una respuesta simple para el frontend.

Este diseño separa correctamente:

- la aceptación rápida del trabajo,
- de la recuperación posterior del resultado.

## 6. El hook del frontend que gobierna el flujo asíncrono

En `frontend/hooks/use-story-generation.ts` está una de las piezas más importantes del frontend.

Ese hook:

1. lanza la petición inicial de generación,
2. recibe el `task_id`,
3. hace polling cada 2 segundos contra `/tasks/{task_id}`,
4. actualiza el estado local:
   - `queued`
   - `processing`
   - `completed`
   - `failed`

La lógica es simple, pero efectiva para un prototipo productivo. No introduce WebSockets para el resultado del cuento, lo que reduce complejidad en frontend y backend.

El precio es conocido:

- más tráfico por polling,
- menor inmediatez que un canal push,
- y necesidad de límites de timeout.

En este caso, el hook corta a los 300 polls, es decir, unos 10 minutos.

## 7. Dos experiencias de creación, un mismo pipeline

### Modo abierto

En `frontend/components/tale-generator.tsx`, el usuario:

- escribe un prompt,
- elige longitud,
- elige estilo visual,
- opcionalmente dicta texto por micrófono.

Después el frontend envía un payload con:

- `topic`
- `num_chapters`
- `visual_style`
- `lang`

### Modo guiado

En `frontend/components/guided-tale-generator.tsx`, el usuario no redacta libremente. Selecciona:

- grupo de edad,
- nombre y descripción del protagonista,
- tema científico,
- misión,
- estilo visual,
- número de capítulos.

El backend convierte esos campos estructurados en un prompt rico usando `api/prompts/guided_story_prompts.py`.

La conclusión técnica es interesante: Cuentee no tiene dos motores narrativos distintos. Tiene un mismo motor generativo con dos capas distintas de preparación de contexto.

## 8. Ingeniería de prompts e internacionalización

La parte de prompts está bastante modularizada:

- `api/prompts/utils.py`
- `api/prompts/story_prompts.py`
- `api/prompts/guided_story_prompts.py`
- `api/prompts/translations/*.py`

### Localización de prompts

`get_localized_prompts(lang)` carga módulos por idioma y devuelve varios bloques:

- prompts de estilo visual,
- prompts de temas,
- prompts de misiones,
- prompt de sistema,
- formato guiado.

Eso permite que no solo cambie el idioma de la interfaz, sino también la instrucción real que recibe el modelo.

### Prompt de historia

`get_story_system_prompt()` construye el system prompt final con:

- número de capítulos,
- pautas de longitud por capítulo.

### Prompt de imagen

`get_image_prompt_system()` entrega el prompt base para que otro LLM transforme fragmentos narrativos en prompts visuales aptos para ilustración infantil.

Esta separación es buena práctica. El modelo que escribe la historia no es exactamente el mismo que “traduce” historia a prompt visual.

## 9. LangGraph como núcleo de orquestación

La lógica central vive en `api/agents/story_agent.py`.

Aquí el proyecto define:

- un modelo estructurado `Story`,
- un estado tipado `StoryState`,
- un `StateGraph`,
- dos nodos:
  - `generate_story`
  - `generate_images`

### Nodo 1: generación de texto

`story_generation_node()`:

1. toma `messages`, idioma y número de capítulos,
2. construye el system prompt,
3. llama a `story_agent.invoke(...)`.

El `story_agent` es un `ChatGroq` configurado con `with_structured_output(Story, method="json_mode")`. Eso significa que el LLM no devuelve texto arbitrario, sino una estructura validada por Pydantic.

Este punto es clave:

- título,
- capítulos,
- URLs de imagen,
- tipo de historia,
- metadatos

quedan encapsulados en un contrato fuerte. Para aplicaciones generativas, eso reduce mucho el coste de postprocesado y parsing frágil.

### Nodo 2: generación de imágenes

`image_generation_node()` recibe la historia ya estructurada y hace:

1. prepara contexto de usuario para almacenamiento,
2. genera prompt de portada,
3. genera imagen de portada,
4. recorre capítulos,
5. genera prompt por capítulo,
6. genera una imagen por capítulo.

Después compone un `final_output` serializable que ya incluye `story_id`, `user_id`, `story_type` y `metadata`.

### El grafo

El grafo es lineal:

```text
START -> generate_story -> generate_images -> END
```

No es un workflow complejo con ramas o reintentos por nodo, pero sí introduce una ventaja importante: deja preparada la base para evolucionar el pipeline sin convertir el código en una cascada de llamadas difícil de mantener.

## 10. Texto con Groq, imágenes con OpenAI

Cuentee mezcla proveedores por especialidad.

### Generación de texto

El texto usa Groq vía `langchain_groq.ChatGroq` con el modelo:

- `llama-3.3-70b-versatile`

Groq encaja aquí por latencia y coste razonable para una experiencia conversacional o creativa.

### Generación de imágenes

Las imágenes usan OpenAI desde `api/agents/utils.py`.

El sistema soporta varios modelos:

- `dall-e-3`
- `dall-e-2`
- `gpt-image-1`
- `gpt-image-1-mini`
- `gpt-image-1.5`

Según el modelo, la respuesta se procesa como:

- URL remota,
- o base64.

Después la imagen se sube a Supabase Storage para que la aplicación no dependa de una URL efímera del proveedor original.

Esta decisión tiene bastante sentido operativo:

- centraliza activos en una infraestructura propia,
- facilita persistencia,
- simplifica permisos,
- y evita exponer directamente artefactos de proveedor.

## 11. Supabase Storage como repositorio de medios

El proyecto usa dos buckets conceptualmente distintos:

- `cuentee_images`
- `cuentee_pdfs`

En imágenes, el flujo es especialmente interesante porque no usa el service role para subir activos del cuento. El sistema construye un cliente S3-compatible autenticado con el JWT del usuario actual y lo usa para subir al storage de Supabase.

Eso implica que el contexto del usuario se propaga más allá de la base de datos y llega hasta el almacenamiento de objetos.

El naming de archivos sigue esta idea:

- usuario,
- historia,
- tipo de imagen,
- sufijo único.

Ejemplo conceptual:

```text
<user_id>/<story_id>/chapter_1_ab12cd34.png
```

## 12. Celery y Redis: desacoplar lo lento de lo interactivo

La generación de cuentos ilustrados puede tardar bastante:

- invocación al LLM,
- múltiples imágenes,
- subidas a storage,
- escritura en base de datos,
- render a PDF.

Hacer eso en la request HTTP sería un error de diseño. Por eso el proyecto usa:

- Redis como broker,
- Celery como cola,
- FastAPI como productor de tareas,
- workers como consumidores.

La tarea principal está en `api/celery_tasks/tasks.py`:

- `generate_story_task`

Esa tarea:

1. construye metadatos de trazabilidad,
2. invoca el grafo,
3. recoge `story_data`,
4. ejecuta postproceso,
5. retorna el resultado final.

Además incorpora `self.retry(..., max_retries=3)`, lo que da una política básica de resiliencia ante fallos transitorios.

## 13. LangSmith para trazabilidad

Hay varias anotaciones `@traceable` y metadatos ricos de ejecución.

Eso convierte cada generación en una unidad observable con atributos como:

- `story_type`
- `topic`
- `user_id`
- `language`
- `model`
- `story_id`

En sistemas con IA esto importa mucho. No basta con saber que “falló algo”; hay que saber:

- con qué prompt,
- con qué configuración,
- para qué usuario,
- en qué idioma,
- con qué modelo.

Cuentee ya está encaminado hacia esa observabilidad.

## 14. El postproceso: PDF, persistencia y créditos

Una vez generado el cuento, el worker entra en postproceso.

### Generación de PDF

`api/services/pdf_service.py` usa `fpdf` y `Pillow` para producir un PDF con:

- tipografía OpenDyslexic,
- portada,
- marcos decorativos,
- imágenes redondeadas,
- fondo visual,
- CTA final hacia `cuentee.com`.

No es un dump plano de texto. Intenta convertir el cuento en un artefacto presentable y descargable.

### Persistencia

Después se inserta un registro en `stories` con:

- `title`
- `content`
- `prompt`
- `story_type`
- `metadata`

### Créditos

Al final se descuentan créditos del perfil del usuario.

Además, `api/main.py` lanza una tarea en background en startup que revisa diariamente qué usuarios `plus` deben recibir recarga periódica de créditos.

No es un scheduler distribuido sofisticado, pero sí una forma rápida de introducir lógica de suscripción sin otro servicio adicional.

## 15. Entrada por voz en tiempo real

Una parte menos obvia del sistema es `api/routers/transcription.py`.

Aquí el frontend abre un WebSocket y envía chunks de audio `webm` capturados con `MediaRecorder`. El backend crea un puente entre FastAPI asíncrono y el cliente síncrono de Speechmatics mediante:

- una cola,
- un buffer,
- un thread dedicado.

El resultado se reenvía al navegador como mensajes:

- `partial`
- `final`

El frontend, por ahora, solo incorpora el texto final al prompt para evitar una UX ruidosa con parciales. Es una decisión sensata: la complejidad del streaming se usa para mejorar entrada, no para volver inestable la edición del texto.

## 16. Qué hace bien esta arquitectura

Hay varias decisiones acertadas en esta rama.

### 1. Contrato estructurado con Pydantic

La historia no viaja como texto libre, sino como objeto validado. Eso reduce errores de parsing y hace más robusto todo el pipeline.

### 2. Asincronía bien aplicada

La UI no se bloquea esperando generación. FastAPI solo acepta el trabajo y Celery hace lo pesado.

### 3. Supabase como plataforma transversal

Supabase cubre:

- auth,
- base de datos,
- storage,
- RLS.

Eso reduce el número de piezas operativas.

### 4. Prompting localizado

No se limita a traducir la interfaz; también traduce y adapta la instrucción de generación.

### 5. Orquestación preparada para crecer

Aunque hoy el grafo es lineal, usar LangGraph facilita introducir nodos futuros como:

- moderación,
- evaluación automática,
- reintentos selectivos,
- generación de audio,
- control de calidad visual.

## 17. Dónde están las limitaciones actuales

Como prototipo avanzado, también deja ver sus siguientes cuellos de botella.

### Polling en lugar de push para tareas

Funciona, pero a medida que crezca el tráfico probablemente convenga mover el resultado de Celery a SSE o WebSocket.

### Persistencia semiestructurada en `content`

Guardar toda la historia como JSON serializado acelera el desarrollo, pero complica analytics, búsquedas y reporting.

### Lógica de créditos embebida en worker

Es práctica, pero mezcla generación con billing básico. En un sistema más maduro convendría aislar esa contabilidad.

### Task loop de recarga dentro de FastAPI

Resolver recargas mensuales con una coroutine infinita en startup no es ideal para despliegues horizontales. Lo natural sería moverlo a un scheduler externo o a Celery Beat.

## 18. Lecciones de ingeniería que deja este proyecto

Cuentee enseña varias lecciones útiles para construir productos con IA más allá del “demo prompt-in, text-out”.

### 1. La IA útil necesita pipeline, no solo modelo

El valor no está únicamente en invocar un LLM. Está en unir:

- prompt engineering,
- validación estructurada,
- assets visuales,
- persistencia,
- auth,
- billing,
- UX.

### 2. El storage importa tanto como el modelo

Si generas imágenes o PDFs, necesitas estrategia de activos. Centralizarlos en tu propia infraestructura simplifica el resto del sistema.

### 3. La trazabilidad deja de ser opcional muy rápido

En cuanto hay usuarios reales, idiomas, créditos y varios modelos, sin observabilidad es imposible depurar bien.

### 4. Los productos de IA se benefician de inputs más estructurados

El modo guiado demuestra que la mejor UX no siempre es “escribe cualquier cosa”. A veces un formulario bien diseñado produce mejores salidas y reduce ambigüedad.

## 19. Conclusión

Cuentee no es solo un generador de cuentos. Es una arquitectura bastante representativa de una nueva clase de aplicaciones AI-native:

- interfaz moderna en Next.js,
- backend ligero en FastAPI,
- orquestación asíncrona con Celery,
- generación multimodal con Groq y OpenAI,
- almacenamiento y seguridad con Supabase,
- y un producto final empaquetado como historia visual y PDF.

Lo más interesante es que el sistema ya está organizado como una cadena de producción de contenido, no como una simple llamada a un modelo. Esa diferencia es justo la que separa un experimento de una aplicación que puede evolucionar hacia producto real.

Si tuviera que resumir la arquitectura en una sola frase, sería esta:

> Cuentee convierte un prompt autenticado en un artefacto narrativo persistente mediante un pipeline multimodal, asíncrono y observable.

Y esa es, probablemente, la forma correcta de pensar muchas aplicaciones de IA actuales.
