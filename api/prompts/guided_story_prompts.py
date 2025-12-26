from typing import Dict

# Estructura:
# KEY: mission_value (ej: "land_of_shapes")
# VALUE: Prompt base
# Los placeholders {protagonist}, {age_group}, etc se formatearán en runtime.

GUIDED_PROMPTS: Dict[str, str] = {
    # --- 3-5 años: Tamaños y formas ---
    "land_of_shapes": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'El país de las formas'. "
        "Trama: El protagonista viaja a un mundo donde todo está hecho de figuras geométricas básicas (círculos, cuadrados, triángulos). "
        "Misión: Ayudar a un Círculo triste que perdió su redondez o encontrar la pieza que falta para completar un puente de triángulos. "
        "El tono debe ser amable, simple y educativo."
    ),
    "big_or_small": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'Grande o pequeño'. "
        "Trama: El protagonista encuentra un objeto mágico que cambia el tamaño de las cosas. "
        "Misión: Usar el objeto para resolver problemas simples (ej: ayudar a una hormiga a cruzar un charco haciéndola grande, o pasar por una puerta pequeña haciéndose pequeño). "
        "Enfatiza los conceptos de grande, mediano y pequeño."
    ),

    # --- 3-5 años: Cuerpo humano ---
    "five_senses": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'Los cinco súper sentidos'. "
        "Trama: El protagonista despierta con sus sentidos súper agudizados por un día. "
        "Misión: Descubrir qué sonido hace un pajarito lejano, a qué huelen las flores mágicas, etc. "
        "Debe explorar cada uno de los 5 sentidos (vista, oído, olfato, gusto, tacto) en situaciones divertidas."
    ),
    "brave_tooth": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'El diente valiente'. "
        "Trama: Al protagonista se le mueve un diente de leche. "
        "Misión: Perder el miedo a que se caiga el diente y entender que es parte de crecer. "
        "Puede aparecer el Ratoncito Pérez o un hada al final. Tono tranquilizador y valiente."
    ),

    # --- 6-8 años: Sonido ---
    "lost_orchestra": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'La orquesta perdida'. "
        "Trama: En el bosque de los sonidos, los instrumentos han dejado de sonar porque han olvidado su melodía. "
        "Misión: El protagonista debe encontrar los instrumentos y recordarles cómo suenan (viento, cuerda, percusión) para dar un gran concierto final. "
        "Introduce conceptos básicos de cómo se produce el sonido (vibración, soplido)."
    ),
    "mysterious_echo": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'El eco misterioso'. "
        "Trama: El protagonista escucha un eco extraño en una cueva que no repite lo que se dice, sino que responde preguntas. "
        "Misión: Entrar en la cueva y descubrir la ciencia detrás del eco (el rebote del sonido) y quién está al otro lado. "
        "Aventura con un toque de misterio suave."
    ),

    # --- 6-8 años: Agua y cambios ---
    "traveling_drop": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'La gota viajera'. "
        "Trama: El protagonista se hace amigo de una gota de agua. "
        "Misión: Acompañar a la gota en su ciclo: evaporarse hacia una nube, llover sobre una montaña y fluir por un río hasta el mar. "
        "Explica el ciclo del agua de forma narrativa y emocionante."
    ),
    "melting_ice": (
        "Escribe un cuento infantil para niños de {age_group} años. "
        "El estilo visual debe ser {visual_style}. "
        "El protagonista es {protagonist}. "
        "La historia se titula 'El hielo que se derrite'. "
        "Trama: El reino de hielo se está derritiendo demasiado rápido debido a un dragón de calor. "
        "Misión: El protagonista debe aprender sobre los estados de la materia (sólido a líquido) y convencer al dragón de calmar su fuego para salvar el castillo de hielo. "
        "Enfatiza la reversibilidad de los cambios de estado (congelar/derretir)."
    )
}
