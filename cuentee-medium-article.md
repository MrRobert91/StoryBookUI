# Construí una IA que genera cuentos personalizados para niños — y quiero que la pruebes

*Un proyecto de fin de semana que se fue de las manos (de la mejor manera posible)*

---

Hay una idea que tengo dando vueltas en la cabeza desde hace tiempo: ¿y si pudiera generarle a un niño un cuento completamente personalizado, con su nombre, su animal favorito, el tema que más le gusta del colegio, y con ilustraciones que mantienen coherencia visual de principio a fin? No un cuento de plantilla, sino uno que de verdad sienta que fue escrito *para él*.

Eso es **[Cuentee](https://www.cuentee.com)**.

Lo construí en mi tiempo libre, con muchas ganas y bastante café. No es un producto de una startup respaldada por millones, es algo que hice yo solo porque quería ver si era posible. Te cuento qué puede hacer, cómo funciona, y si tienes hijos, sobrinos o simplemente curiosidad, te invito a que lo pruebes y me digas qué piensas.

---

## ¿Qué es Cuentee?

Cuentee genera cuentos infantiles con IA, con texto e ilustraciones. Describes lo que quieres y en un par de minutos tienes un cuento original de varios capítulos con imágenes generadas para cada escena.

Hay dos formas de usarlo. El **modo libre** es exactamente lo que parece: escribes (o dictás por voz) lo que se te ocurra. El **modo guiado** está pensado para cuentos educativos: eliges el grupo de edad, describes al protagonista, seleccionas un tema científico (el espacio, el ciclo del agua, las emociones, los animales...) y una misión concreta. El resultado es una historia que tiene trama y que además explica algo.

Lo que sí me costó resolver fue la coherencia visual entre capítulos. Cuando generas ilustraciones con IA una a una, el personaje cambia de aspecto en cada imagen. Sofía puede tener el pelo rojo en el capítulo 1 y rubio en el capítulo 3. Para evitarlo, el sistema extrae una descripción visual precisa de cada personaje después de generar el texto ("niña humana, 8 años, pelo largo y rizado de color rojo intenso, ojos verdes, piel clara, peto vaquero azul...") y la inyecta literalmente en cada prompt de imagen, sin que ningún modelo la reescriba ni la interprete. No es un truco especialmente elegante, pero funciona.

En cuanto a estilos, puedes elegir entre dibujos animados, acuarela, animación 3D, anime, crayones de niño e ilustración editorial. Y los cuentos se pueden generar en seis idiomas: español, inglés, francés, alemán, italiano y portugués. No cambia solo el texto, las instrucciones del sistema y los temas educativos están localizados en cada idioma. Una cosa más: el PDF exportable usa la fuente OpenDyslexic, diseñada para lectores con dislexia. Es un detalle pequeño, pero me importa.

---

## Qué tipo de cuentos puedes crear

Algunos de los que he probado:

- *"Un cocodrilo de mediana edad que se jubila del río Nilo y decide aprender a pintar acuarelas en Florencia"*
- *"Tres hermanas que encuentran un mapa del tesoro dentro de una enciclopedia de 1987 y tienen que descifrarlo sin que se entere su abuela"*
- *"Cuento educativo sobre el ciclo del agua: Noa, 6 años, mochila amarilla, pelo afro y ganas de mojarse los pies, tiene que guiar a una gota de lluvia de vuelta al mar"*
- *"Un pulpo llamado Ramón que tiene miedo a la oscuridad y vive en el fondo del océano — estilo anime, 7 capítulos"*
- *"La historia de Kai, un robot de cocina que sueña con ser chef estrella Michelin pero solo sabe hacer tostadas"*

El resultado son entre 3 y 10 capítulos, con portada e ilustración propia para cada escena.

---

## Cómo funciona por dentro

El backend está en Python con FastAPI, y las generaciones se procesan de forma asíncrona con Celery y Redis. Generar un cuento con ilustraciones puede tardar entre 30 segundos y un par de minutos, así que no puedes tener al usuario mirando una pantalla bloqueada. El frontend es Next.js con TypeScript y TailwindCSS. Para persistencia, autenticación y almacenamiento de imágenes uso Supabase, que me ahorró bastante trabajo en infraestructura.

La generación de cada cuento pasa por tres fases encadenadas con LangGraph. Primero, un LLM escribe la historia completa en formato estructurado: título más capítulos. Luego, el mismo modelo lee el texto recién generado y extrae una descripción visual objetiva de cada personaje, sin adjetivos subjetivos, solo atributos observables: especie, edad, color de pelo, color de ojos, ropa. Por último, para cada capítulo se construye un prompt de escena con los bloques de personajes añadidos literalmente, y ese prompt va a la API de imágenes de OpenAI.

También hay un sistema de revisión de seguridad infantil: un LLM independiente evalúa cada historia según criterios de idoneidad (violencia, contenido adulto, elementos perturbadores). Si el porcentaje de historias que superan el umbral cae demasiado, el sistema avisa. No es infalible, pero es mejor que no tener nada.

---

## Las herramientas que me ayudaron

Cuentee lo construí yo, pero con una cantidad absurda de ayuda de IAs de código.

El que más usé fue **Claude Code**, sobre todo cuando necesitaba razonar sobre la arquitectura. No solo completa líneas, entiende el proyecto entero y puedes preguntarle cosas como "¿tiene sentido modelarlo así o me estoy complicando?". Útil de verdad.

Para arrancar rápido y generar boilerplate en las fases iniciales usé **OpenAI Codex**. **GitHub Copilot** dentro de VS Code fue el compañero del día a día, para lo más mecánico. Y **Jules de Google** lo probé para tareas más autónomas, del tipo "trabaja en esta rama y refactoriza este módulo". Funciona de forma asíncrona, lo dejas trabajar y vuelves después.

La sensación general es que ya no estás solo en el proyecto, aunque seas el único que lo trabaja.

---

## El modelo (de momento, gratuito)

Cuentee funciona con un sistema de créditos: cada cuento generado cuesta uno. Ahora mismo el plan gratuito da 3 créditos para empezar y no hay ningún plan de pago. Quiero primero ver si esto le resulta útil a alguien antes de complicarlo. Los costes de API de OpenAI y Groq son reales, pero de momento los asumo yo.

---

## Qué viene después

Tengo más ideas que tiempo, así que en algún momento tendré que decidir qué tiene sentido construir. Las que más me rondan:

- narración en audio, para escuchar el cuento como un audiolibro
- personajes persistentes que puedas reutilizar en varios cuentos
- un modo donde el niño elige qué pasa en cada capítulo
- impresión física, para que el cuento acabe siendo un libro de verdad

Pero antes de construir cualquiera de esas cosas, me interesa saber si lo que hay ahora es útil para alguien.

---

## Una última cosa

Si tienes hijos, sobrinos, alumnos, o simplemente quieres ver qué pasa cuando le pides a una IA la historia de un cocodrilo filósofo en estilo acuarela, pruébalo:

**[www.cuentee.com](https://www.cuentee.com)**

Cualquier comentario es bienvenido, aquí en Medium, por email, por LinkedIn. Me interesa especialmente saber si el cuento tiene calidad, si las ilustraciones encajan con lo que esperabas, o si hay algo que claramente falta. Las críticas también sirven, quizá más que los aplausos.

---

*Si te ha gustado, dale al aplauso (Medium te deja hasta 50). Y si conoces a alguien a quien pueda interesarle, compártelo.*
