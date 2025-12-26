from typing import Dict

# --- VISUAL STYLES ---
# Detailed visual instructions for the Image Generation Model.
VISUAL_STYLE_PROMPTS: Dict[str, str] = {
    "cartoons": (
        "Estilo de dibujos animados modernos, vibrantes y coloridos. "
        "Líneas limpias, colores saturados y expresiones exageradas pero amigables. "
        "Similar a las series de animación infantil actuales (tipo Bluey o Peppa Pig pero con más detalle). "
        "Iluminación plana o con sombreado suave cel-shading."
    ),
    "watercolor": (
        "Estilo de acuarela suave y soñador. "
        "Colores pastel, bordes difuminados y texturas de papel visible. "
        "Un toque artístico y delicado, como los libros de cuentos clásicos ilustrados a mano (tipo Beatrix Potter). "
        "Atmósfera cálida y acogedora."
    ),
    "3d_animation": (
        "Estilo de animación 3D renderizada (tipo Pixar o Disney moderno). "
        "Iluminación volumétrica, texturas detalladas (pelo, tela), profundidad de campo suave. "
        "Personajes con proporciones agradables, ojos grandes y expresivos. "
        "Acabado pulido y cinematográfico."
    )
}

# --- SCIENTIFIC TOPICS ---
# Detailed educational context for the Story LLM.
TOPIC_PROMPTS: Dict[str, str] = {
    # 3-5 Years
    "shapes_sizes": "geometría básica: identificación de formas (círculo, cuadrado, triángulo) y comparación de tamaños (grande, mediano, pequeño).",
    "human_body": "partes del cuerpo y los cinco sentidos. Reconocimiento básico de funciones corporales simmples.",
    
    # 5-8 Years
    "sound": "física del sonido: vibraciones, eco, tipos de sonidos (graves/agudos) y el silencio.",
    "water_changes": "ciclo del agua y estados de la materia (sólido, líquido, gas) de forma introductoria."
}

# --- MISSIONS ---
# Specific plot outlines for the Story LLM.
MISSION_PROMPTS: Dict[str, str] = {
    # 3-5 Years: Shapes & Sizes
    "land_of_shapes": (
        "El protagonista viaja al 'País de las Formas', un lugar donde todo está hecho de figuras geométricas. "
        "El conflicto es que el Puente de las Formas se ha roto y faltan piezas específicas. "
        "El protagonista debe encontrar círculos para las ruedas, cuadrados para las casas y triángulos para el puente."
    ),
    "big_or_small": (
        "El protagonista encuentra una lupa mágica que hace las cosas grandes o pequeñas. "
        "Debe usarla para ayudar a sus amigos animales: hacer pequeña una roca gigante que bloquea el camino de una hormiga, "
        "o hacer grande una semilla para que alimente a muchos pájaros. "
        "Enseña la relatividad del tamaño."
    ),

    # 3-5 Years: Human Body
    "five_senses": (
        "El protagonista pierde sus gafas (o algo similar) y debe usar sus otros cuatro sentidos para encontrarlas. "
        "Debe escuchar pistas, oler el aroma de las galletas donde las dejó, tocar texturas rugosas, etc. "
        "Cada capítulo se centra en un sentido diferente."
    ),
    "brave_tooth": (
        "Al protagonista se le mueve su primer diente y tiene miedo. "
        "Su misión es investigar qué pasa con los dientes y conocer al 'Hada de los Dientes' o 'Ratoncito Pérez'. "
        "La historia normaliza el proceso natural de perder dientes de leche."
    ),

    # 5-8 Years: Sound
    "lost_orchestra": (
        "En el Bosque Silencioso, los instrumentos han perdido su voz. "
        "El protagonista descubre que todo sonido nace de una vibración. "
        "Debe 'despertar' a los instrumentos haciéndolos vibrar de diferentes formas (golpear, soplar, rasguear) "
        "para que la orquesta vuelva a tocar."
    ),
    "mysterious_echo": (
        "El protagonista explora una cueva donde el eco no repite, sino que responde. "
        "Descubre que el sonido viaja como ondas invisibles y rebota en las paredes. "
        "La misión es usar el eco para encontrar la salida de un laberinto oscuro."
    ),

    # 5-8 Years: Water Changes
    "traveling_drop": (
        "El protagonista se encoge al tamaño microscópico y monta sobre una gota de agua llamada 'Flu'. "
        "Viajan juntos desde el mar (evaporación), se convierten en nube (condensación) y caen como lluvia (precipitación) en una montaña nevada. "
        "Es un viaje de aventura a través del ciclo hidrológico."
    ),
    "melting_ice": (
        "El Reino de Hielo se está derritiendo porque el calentador mágico se ha quedado encendido. "
        "El protagonista debe entender cómo el calor transforma el sólido en líquido. "
        "Debe enfriar el ambiente para que el agua vuelva a ser hielo sólido y salvar el castillo."
    )
}
