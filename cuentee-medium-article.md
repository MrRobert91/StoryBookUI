# Construí una IA que genera cuentos personalizados para niños — y quiero que la pruebes

*De una idea suelta a un cuento ilustrado y personalizado: pruébalo y cuentame que te parece*

---

Hay una idea que tengo dando vueltas en la cabeza desde hace tiempo: ¿y si pudiera generarle a un niño un cuento completamente personalizado, con su nombre, su animal favorito, el tema que más le gusta del colegio, y con ilustraciones que mantienen coherencia visual de principio a fin? No un cuento de plantilla, sino uno que de verdad sienta que fue escrito *para él*.

Eso es **[Cuentee](https://www.cuentee.com)**.

*(Si prefieres curiosear antes de leer: está en [www.cuentee.com](https://www.cuentee.com).)*

Lo construí en mi tiempo libre, con muchas ganas y bastante café. No es un producto de una startup respaldada por millones, es algo que hice yo solo porque quería ver si era posible. Te cuento qué puede hacer, cómo funciona, y si tienes hijos, sobrinos o simplemente curiosidad, te invito a que lo pruebes y me digas qué piensas.

---

## ¿Qué es Cuentee?

Cuentee genera cuentos infantiles con IA, con texto e ilustraciones. Describes lo que quieres y normalmente en uno o dos minutos tienes un cuento original de varios capítulos con imágenes generadas para cada escena. Cada cuento que creas se guarda en tu cuenta, así que no se pierde: tienes una galería donde puedes volver a leerlos o descargarlos cuando quieras.

![Un cuento generado en Cuentee: portada y un par de páginas con sus ilustraciones](docs/screenshots/story-viewer.png)
*Un cuento real generado con Cuentee. (Sustituye esta imagen por una captura o GIF de un cuento tuyo — es lo que más anima a probarlo.)*

Hay dos formas de usarlo. El **modo libre** es exactamente lo que parece: escribes (o dictas por voz) lo que se te ocurra. El **modo guiado** está pensado para cuentos educativos: eliges el grupo de edad, describes al protagonista, seleccionas un tema científico (el espacio, el ciclo del agua, las emociones, los animales...) y una misión concreta. El resultado es una historia que tiene trama y que además explica algo.

Lo que sí me costó resolver fue la coherencia visual entre capítulos. Cuando generas ilustraciones con IA una a una, el personaje cambia de aspecto en cada imagen. Sofía puede tener el pelo rojo en el capítulo 1 y rubio en el capítulo 3. Para evitarlo, el sistema extrae una descripción visual precisa de cada personaje después de generar el texto ("niña humana, 8 años, pelo largo y rizado de color rojo intenso, ojos verdes, piel clara, peto vaquero azul...") y la inyecta literalmente en cada ilustración, sin que ningún modelo la reescriba ni la interprete. No es un truco especialmente elegante, pero funciona: la niña se parece a sí misma de la primera página a la última.

En cuanto a estilos, puedes elegir entre dibujos animados, acuarela, animación 3D, anime, crayones de niño e ilustración editorial. Y los cuentos se pueden generar en seis idiomas: español, inglés, francés, alemán, italiano y portugués. No cambia solo el texto, también los temas y las instrucciones internas están adaptados a cada idioma. Una cosa más: el PDF que puedes descargar usa la fuente OpenDyslexic, diseñada para lectores con dislexia. Es un detalle pequeño, pero me importa.

---

## Qué tipo de cuentos puedes crear

Algunos de los que he probado:

- *"Un cocodrilo de mediana edad que se jubila del río Nilo y decide aprender a pintar acuarelas en Florencia"*
- *"Tres hermanas que encuentran un mapa del tesoro dentro de una enciclopedia de 1987 y tienen que descifrarlo sin que se entere su abuela"*
- *"Cuento educativo sobre el ciclo del agua: Noa, 6 años, mochila amarilla, pelo afro y ganas de mojarse los pies, tiene que guiar a una gota de lluvia de vuelta al mar"*
- *"Un pulpo llamado Ramón que tiene miedo a la oscuridad y vive en el fondo del océano"*
- *"La historia de Kai, un robot de cocina que sueña con ser chef estrella Michelin pero solo sabe hacer tostadas"*

El resultado son entre 3 y 9 capítulos, con portada e ilustración propia para cada escena.

---

## Cómo funciona (sin entrar en la fontanería)

No quiero aburrirte con la arquitectura, pero sí contarte la idea, porque explica por qué los cuentos salen como salen.

Cada cuento se construye en tres pasos. Primero, un modelo de IA escribe la historia completa, capítulo a capítulo. Después, otro paso vuelve a leer esa historia y "ficha" a cada personaje con una descripción visual muy concreta, sin florituras: especie, edad, color de pelo, color de ojos, ropa. Y por último, esa ficha se usa tal cual para generar cada ilustración. Ese segundo paso es el que mantiene a los personajes coherentes de principio a fin, y es la parte que más me costó afinar.

La seguridad infantil me la tomo en serio. Las instrucciones con las que se escriben los cuentos ya están pensadas para mantener un tono apropiado, y además he montado un control de calidad que revisa tandas de cuentos con criterios de idoneidad —violencia, contenido adulto, elementos perturbadores— usando otro modelo de IA como "juez": si demasiados no pasan el listón, salta la alarma y me toca mirar qué está fallando. Funciona por detrás, como un termómetro del sistema, no como un censor que apruebe cada cuento en el instante de generarlo. No es infalible, pero me permite detectar pronto si algo se desvía, y prefiero tener esa red a no tenerla.

Por debajo hay bastante más fontanería —generación de texto, ilustraciones, PDFs, todo orquestado para que no esperes mirando una pantalla bloqueada—, pero eso es tema para otro artículo más técnico.

---

## El modelo (de momento, gratuito)

Cuentee funciona con un sistema de créditos: cada cuento generado cuesta uno. Ahora mismo el plan gratuito da 3 créditos para empezar y no hay ningún plan de pago. Quiero primero ver si esto le resulta útil a alguien antes de complicarlo. Los costes de las APIs de IA son reales, pero de momento los asumo yo.

---

## Dónde está ahora

Para que sepas qué esperar: Cuentee funciona y es gratis (esos 3 créditos para empezar, sin plan de pago). Es un proyecto en activo de una sola persona, así que verás cosas por pulir y algún detalle áspero. Si algo no funciona como esperabas, quiero saberlo: es justo el tipo de feedback que necesito ahora mismo.

---

## Qué viene después (y dónde entras tú)

Tengo más ideas que tiempo, así que tendré que decidir qué construir primero. Estas son las que más me rondan:

- narración en audio, para escuchar el cuento como un audiolibro
- personajes persistentes que puedas reutilizar en varios cuentos
- un modo donde el niño elige qué pasa en cada capítulo
- impresión física, para que el cuento acabe siendo un libro de verdad

Pero no quiero decidirlo yo solo. ¿Cuál de estas te interesa más? ¿Hay algo que no está en la lista y que para ti sería lo primero? Dímelo, porque antes de construir nada nuevo me interesa saber si lo que ya hay le sirve a alguien.

---

## Pruébalo y cuéntame

Si tienes hijos, sobrinos, alumnos, o simplemente quieres ver qué pasa cuando le pides a una IA la historia de un capibara filósofo en estilo acuarela, pruébalo:

**[www.cuentee.com](https://www.cuentee.com)**

**¿Tienes alguna duda sobre cómo funciona? ¿Se te ocurre algo que lo haría mejor?** Tírate a lo loco: un cuento donde el propio niño aparezca dibujado como protagonista a partir de una foto, meter a la mascota de casa en la historia, sagas que continúan capítulo a capítulo con los mismos personajes, un cuento nuevo cada noche antes de dormir, o que sean los padres quienes pongan la voz al audiolibro. **Déjalo en los comentarios** — leo absolutamente todo y es lo que me ayuda a decidir qué construir después. Y si pruebas a generar un cuento, cuéntame qué tal te quedó: si la historia engancha, si las ilustraciones encajaban con lo que imaginabas, o si hay algo que claramente falta. Las críticas valen, quizá más que los aplausos.

---

*Si te ha gustado, dale al aplauso (Medium te deja hasta 50). Y si conoces a alguien a quien pueda interesarle, compártelo.*
