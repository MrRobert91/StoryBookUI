# Más allá del prompt: cómo construí Cuentee, un generador de cuentos infantiles con IA

La primera versión de Cuentee fue un script de cuarenta líneas. Le pasabas una idea, llamaba a un LLM, y te escupía un cuento. Funcionaba. Y precisamente porque funcionaba tan rápido, tardé un par de días en darme cuenta de que no tenía nada.

Generar texto con un modelo es la parte fácil. Es casi un commodity. El problema real aparece cuando intentas convertir esa llamada en algo que una familia pueda usar: un cuento con ilustraciones coherentes, seguro para un niño, que se pueda descargar, que no haga esperar al usuario diez minutos mirando un spinner, y que no te arruine en costes de API. Ahí es donde "haz una app con IA" se convierte en "diseña un sistema".

Este artículo es sobre ese salto. Qué decisiones aparecen cuando intentas que un generador de cuentos con IA sea coherente, seguro, monetizable y agradable de usar. No es un tutorial de instalación. Es la historia de las partes que costaron de verdad.

---

## El problema que parecía sencillo

"Genera un cuento infantil." Suena trivial. Pero si lo desmenuzas, cada palabra esconde un reto:

- **Personalización**: que el cuento sea sobre *este* niño, su nombre, su animal favorito, lo que le gusta del cole.
- **Coherencia narrativa**: una historia con principio, nudo y desenlace, no un texto que se deshilacha.
- **Tono adecuado**: lenguaje apropiado para la edad, sin caer en lo soso ni en lo inquietante.
- **Seguridad del contenido**: nada de violencia, miedo gratuito o temas adultos. Esto no es negociable cuando el lector tiene seis años.
- **Ilustraciones coherentes**: y aquí está el monstruo escondido, del que hablaré en detalle más abajo.
- **Coste**: cada cuento son varias llamadas a modelos de texto e imagen. Multiplica eso por usuarios reales.
- **Experiencia**: que generar un cuento sea un par de clics, no rellenar un formulario de Hacienda.

Ninguno de estos problemas se resuelve con un prompt más largo.

---

## Qué es Cuentee

Cuentee es una aplicación web que genera cuentos infantiles personalizados con IA: texto e ilustraciones, listos para leer en pantalla o descargar en PDF. El usuario describe lo que quiere, y en uno o dos minutos tiene una historia original de varios capítulos, cada uno con su propia ilustración.

Hay dos formas de usarlo, y la diferencia entre ambas es más interesante de lo que parece:

- **Modo libre**: escribes (o dictas por voz) lo que se te ocurra. *"Un cocodrilo que se jubila del Nilo y se va a Florencia a aprender acuarela."*
- **Modo guiado**: pensado para cuentos educativos. Eliges grupo de edad, describes al protagonista, seleccionas un tema científico (el ciclo del agua, el espacio, las emociones) y una misión concreta. El resultado tiene trama *y además* enseña algo.

Lo curioso es que, por dentro, **no son dos sistemas distintos**. Es el mismo motor de generación con dos capas diferentes de preparación del contexto. El modo guiado no es más que un constructor de prompts más estructurado delante del mismo pipeline. Volveré a esto, porque es una de las decisiones de las que más me alegro.

---

## El recorrido de un cuento

Antes de entrar en arquitectura, el flujo desde fuera:

```text
1. El usuario inicia sesión.
2. Usa uno de sus créditos.
3. Describe el cuento (modo libre o guiado).
4. El sistema escribe la historia estructurada.
5. Extrae a los personajes y fija su aspecto.
6. Genera la portada y una ilustración por capítulo.
7. Compone un PDF y lo guarda en la nube.
8. El usuario lo lee o lo descarga.
```

Visto así, parece una línea recta. La gracia está en que casi nada de eso ocurre dentro de la petición HTTP del usuario.

---

## La arquitectura, sin que pese

El sistema tiene cuatro piezas, y cada una hace una sola cosa:

```text
Usuario (Next.js)
   │  POST con el JWT de Supabase
   ▼
FastAPI  ──► valida identidad y créditos, encola la tarea y responde al instante
   │
   ▼
Celery + Redis  ──► el trabajo pesado, fuera del ciclo de la petición
   │
   ▼
Grafo LangGraph  ──► historia → personajes → imágenes
   │
   ▼
Supabase  ──► Postgres (datos) + Storage (imágenes y PDFs) + Auth
```

El **frontend** es Next.js 15 con React 19. No es un cliente tonto: gobierna sesión, internacionalización, el estado de la generación e incluso la entrada por voz.

El **backend** es FastAPI, y su trabajo principal es decir que no. Valida el JWT contra Supabase, comprueba créditos, y —esto es importante— **nunca confía en lo que el frontend le cuenta sobre el plan o el saldo del usuario**: siempre reconsulta la base de datos. Si todo cuadra, encola una tarea en Celery y devuelve un `task_id` de inmediato. No genera nada él mismo.

```json
{ "task_id": "abc123", "status": "processing" }
```

Esa respuesta vacía es deliberada. Generar texto, varias imágenes, un PDF y escribir en base de datos puede tardar minuto y medio. Mantener una conexión HTTP abierta todo ese tiempo es frágil y no escala. Así que el backend acepta el encargo y se desentiende; **Celery** y un broker de **Redis** se encargan del resto en segundo plano. El frontend, mientras tanto, hace *polling* cada dos segundos contra `GET /tasks/{id}` hasta que el estado pasa a `completed`.

¿Es elegante el polling? No. ¿Es simple y suficiente para esta fase? Sí. Y esa es exactamente la clase de trade-off del que va este proyecto.

**Supabase** es el pegamento de todo: autenticación, base de datos Postgres y almacenamiento de objetos, las tres cosas detrás de una sola plataforma. Con Row Level Security activado, la propia base de datos es la frontera de seguridad: cada usuario solo puede ver sus historias, sin que yo tenga que escribir esa lógica en el backend. Para un proyecto de una sola persona, reducir el número de piezas operativas no es comodidad, es supervivencia.

---

## La parte difícil no era llamar a la API

Aquí es donde el proyecto se puso interesante.

Cuando generas ilustraciones con IA una a una, **los personajes mutan**. Sofía tiene el pelo rojo y un peto vaquero en el capítulo 1; en el capítulo 3 es rubia y lleva vestido. El modelo de imagen no tiene memoria entre llamadas: cada ilustración es un universo nuevo. Para un cuento, eso lo rompe todo. Un niño nota al instante que "esa no es la misma niña".

Mi primer instinto fue el obvio: pasar la descripción del personaje por el LLM en cada capítulo para que "adaptara" el prompt a la escena. Fue un error. El modelo, por su naturaleza, reescribe. "Pelo rojo intenso" se convierte en "pelo pelirrojo", luego en "tonos cobrizos", y dos capítulos después el personaje ha derivado. Cada reformulación introduce ruido, y el ruido acumulado es justo el problema que intentaba resolver.

La solución a la que llegué es casi anticlimática de lo simple que es: **el aspecto de un personaje nunca debe pasar por un LLM más de una vez.**

Esto convirtió el grafo de generación de dos nodos en tres:

```text
START → generar_historia → extraer_personajes → generar_imágenes → END
```

El nodo del medio es el truco. Después de escribir la historia, un segundo paso lee el texto completo y extrae una *ficha visual objetiva* de cada personaje, con un formato rígido y deliberadamente antipoético:

```text
You are a visual character specification extractor for children's book illustration.
Output EXACTLY one bullet line per character with this format:
- [Name]: [species/type], [apparent age], [hair/fur style and color],
  [eye color], [skin color], [clothing items and colors],
  [distinctive markers], [body build]

Rules:
- Use only observable, concrete attributes.
- Avoid subjective wording (e.g. "warm smile", "lively look").
- Colors must be explicit (dark brown, light blue), not vague (colorful, pastel).
```

El resultado es una línea por personaje, fea a propósito:

```text
- Luna: human girl, 8 years old, long curly red hair, green eyes, fair skin,
  blue denim overalls with a yellow star patch, freckles, slim build
```

Y entonces viene la regla de oro. Cuando se genera la ilustración de un capítulo, el LLM escribe la *escena*, pero la ficha del personaje se **pega tal cual, byte a byte, sin que el modelo la toque**:

```python
# El LLM genera la descripción de la escena...
response = image_llm.invoke([...])
prompt = response.content.strip()

# ...y el bloque de personajes se antepone VERBATIM, nunca reescrito.
if character_block:
    prompt = f"{character_block}\n\n{prompt}"
```

Esos bytes son idénticos en el capítulo 1, en el 5 y en la portada. Luna es exactamente la misma Luna en todas las imágenes porque la cadena de texto que la describe literalmente no cambia.

Hay un último detalle que me gustó resolver: a cada capítulo solo se le inyectan los personajes que **realmente aparecen en él**, detectados buscando sus nombres (y variantes) en el texto del capítulo. Así, el modelo de imagen no se distrae dibujando en la escena a un personaje que no pinta nada ahí.

No es una técnica sofisticada. No usa embeddings, ni fine-tuning, ni nada que quede bien en un paper. Es una decisión de ingeniería pragmática: *identifica qué información no puede degradarse y blíndala de la no-determinación del modelo.* Esa idea —saber qué partes del sistema deben ser deterministas y cuáles pueden ser creativas— es probablemente lo más transferible que me llevo de todo el proyecto.

---

## Un contrato, no un texto

Otra decisión temprana que pagó dividendos: la historia nunca viaja como texto libre. El modelo de Groq (LLaMA 3.3 70B) está configurado para devolver directamente un objeto validado por Pydantic.

```python
story_agent = story_llm.with_structured_output(Story, method="json_mode")
```

`Story` es un contrato: título, lista de capítulos, URLs de imagen, tipo, metadatos. Si el modelo se sale del esquema, falla ruidosamente en el sitio correcto, en lugar de colarse como un JSON malformado que reventará tres pasos más adelante, en el generador de PDF, donde es imposible de depurar. En sistemas generativos, donde la salida es inherentemente impredecible, tener un contrato fuerte en el borde no es burocracia: es lo que evita que el caos se propague.

Por cierto, el texto y los prompts de imagen los genera Groq; las imágenes en sí, OpenAI (DALL·E 3 / GPT-Image). Mezclar proveedores por especialidad —Groq por latencia y coste en texto, OpenAI por calidad de imagen— es de las pocas decisiones que tomé sin dudar. Y una vez generada, cada imagen se sube a mi propio Supabase Storage en lugar de servirla desde la URL efímera del proveedor. Si generas activos, necesitas una estrategia de activos; depender de un enlace temporal de OpenAI es pedir que tus cuentos se queden sin ilustraciones en 24 horas.

---

## Dos experiencias, un solo motor

Vuelvo a la promesa de antes. El modo libre y el modo guiado comparten *exactamente* el mismo grafo, la misma tarea de Celery, el mismo postproceso. Lo único que cambia es cómo se construye el prompt antes de entrar al pipeline.

Esto fue una decisión consciente y, en retrospectiva, la correcta. Significó que cada mejora en el motor —la consistencia de personajes, la trazabilidad, los reintentos— beneficiaba a las dos experiencias sin escribir nada dos veces. La lección de producto es contraintuitiva: a veces la mejor UX no es "escribe lo que quieras". Un formulario bien diseñado (edad, protagonista, tema, misión) produce mejores cuentos y reduce la ambigüedad que el modelo tendría que adivinar. La libertad total es una gran demo y un mal default.

---

## Seguridad infantil como ciudadano de primera

Un cuento generado por IA para un niño tiene un fallo de seguridad inaceptable por defecto: a veces se sale del carril. Por eso Cuentee tiene un evaluador de seguridad como *LLM-as-a-judge*. Un modelo independiente puntúa cada historia en una escala de 0 a 3 y la clasifica como apta o no apta, marcando categorías como violencia, contenido adulto o elementos inquietantes.

Lo monté como un flujo offline que puede correr en CI: genera un lote de cuentos directamente por el grafo (sin Celery, sin API, sin coste de imágenes) y los puntúa. La puerta de calidad es explícita: **al menos el 90% de los cuentos deben sacar un 2 o más**, o el script sale con código de error. No es infalible —ningún filtro lo es—, pero convierte "creo que es seguro" en un número que puedo vigilar y que rompe el build si empeora.

---

## Trazabilidad: porque "falló algo" no sirve

En cuanto hay usuarios reales, seis idiomas, varios modelos y créditos de por medio, "ha fallado la generación" es inútil como diagnóstico. Necesitas saber *con qué prompt, qué configuración, qué usuario, qué idioma y qué modelo*.

Cada generación se instrumenta con LangSmith y arrastra metadatos ricos:

```python
run_metadata = {
    "agent_name": "story_agent",
    "story_type": story_type,
    "topic": topic,
    "user_id": user_id,
    "language": metadata.get("language", "en"),
    "model": model or "llama-3.3-70b-versatile",
    "story_id": str(task_id),
}
```

Cada cuento se vuelve una unidad observable. Cuando algo sale raro, no adivino: lo miro. La trazabilidad deja de ser un lujo y pasa a ser obligatoria mucho antes de lo que uno espera.

---

## El final del viaje: PDF, persistencia y créditos

Cuando las imágenes están listas, el worker entra en el postproceso, donde ocurren tres cosas, en orden:

1. **PDF**: con `fpdf` y `Pillow` se compone un documento de verdad —portada, marcos, imágenes redondeadas, y la fuente *OpenDyslexic*, pensada para lectores con dislexia. Es un detalle pequeño que para mí importa. No es un volcado de texto plano; es un artefacto presentable.
2. **Persistencia**: se guarda la historia en Postgres. Aquí hice una concesión pragmática: el cuento entero se almacena como JSON serializado en una columna de texto, en lugar de normalizar capítulos e imágenes en tablas aparte. Acelera el desarrollo a costa de complicar las analíticas futuras. Lo sé, y lo asumo conscientemente.
3. **Créditos**: se descuenta uno del perfil del usuario. Y si la tarea falla, Celery reintenta hasta tres veces con un minuto de espera, así un fallo transitorio de un proveedor no le cuesta el cuento al usuario.

```python
except Exception as e:
    raise self.retry(exc=e, countdown=60, max_retries=3)
```

---

## Lo que cambiaría en la siguiente versión

Ningún sistema honesto está terminado. Estos son los cuellos de botella que ya veo:

- **Polling → push**. Funciona, pero a más tráfico, mover el resultado a SSE o WebSocket reduciría la latencia percibida y el tráfico inútil.
- **El `content` semiestructurado**. El JSON en una columna de texto fue genial para prototipar y será un dolor para hacer búsquedas y reporting. En algún momento toca normalizar.
- **Lógica de créditos dentro del worker**. Mezclar billing con generación es práctico hoy y querré aislarlo cuando el sistema madure.
- **El refill de créditos como bucle en el arranque de FastAPI**. Resolver las recargas mensuales con una corutina infinita no sobrevive a un despliegue horizontal. Su sitio natural es Celery Beat o un scheduler externo.

Ninguno de estos es un bug. Son deudas conscientes: el precio que pagué por avanzar rápido, anotado para cuando toque cobrarlo.

---

## Lo que me llevo

Si tuviera que destilar el proyecto en unas pocas ideas:

**Una IA útil necesita un pipeline, no un modelo.** El valor no estaba en invocar un LLM, sino en encadenar prompt engineering, validación estructurada, generación de imágenes, persistencia, auth, billing y UX en algo que no se rompa.

**Identifica qué no puede ser no-determinista, y blíndalo.** La consistencia de personajes no la resolvió un modelo mejor, sino decidir qué información no debía tocar ningún modelo. Esa frontera entre lo creativo y lo determinista es donde vive la calidad.

**Los prompts son código de producto.** Acaban versionados, localizados a seis idiomas, testeados con un evaluador de seguridad y tan críticos como cualquier función. Tratarlos como strings sueltos es subestimarlos.

**La UX importa tanto como el modelo.** Que el usuario no espere bloqueado, que un formulario guiado produzca mejores cuentos que el texto libre, que el PDF use una fuente para disléxicos: nada de eso sale del modelo, y todo eso es el producto.

---

## Cierre

Cuentee empezó como un script de cuarenta líneas que ya "funcionaba". El verdadero trabajo no fue hacer que un modelo escribiera un cuento —eso fue el primer día—, sino convertir esa chispa en algo coherente, seguro, trazable y agradable de usar.

Si tuviera que resumir la arquitectura en una frase:

> Cuentee convierte un prompt autenticado en un artefacto narrativo persistente mediante un pipeline multimodal, asíncrono y observable, en el que lo que importa de cada personaje nunca lo decide dos veces un modelo.

Y esa, sospecho, es la forma correcta de pensar la mayoría de productos de IA hoy: no como un wrapper alrededor de una API, sino como una cadena de producción donde el modelo es solo una pieza —brillante, impredecible y, por eso mismo, algo que hay que saber encuadrar.

Puedes probarlo en **[www.cuentee.com](https://www.cuentee.com)**. Si generas la historia de un cocodrilo que aprende acuarela en Florencia, cuéntame qué tal le quedó el pelo entre capítulos.
