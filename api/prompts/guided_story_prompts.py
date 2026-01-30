from typing import Dict

# --- VISUAL STYLES ---
# Detailed visual instructions for the Image Generation Model.
VISUAL_STYLE_PROMPTS: Dict[str, str] = {
    "cartoons": (
        "Estilo de dibujos animados vectoriales modernos y de alta calidad. "
        "Colores planos y vibrantes, líneas de contorno limpias y audaces. "
        "Diseño de personajes expresivo y 'cute', formas redondeadas y amigables. "
        "Sin texturas complejas, estéticaminimalista pero detallada en composición. "
        "Iluminación suave y uniforme, estilo visual similar a aplicaciones educativas modernas."
    ),
    "watercolor": (
        "Estilo acuarela artística sobre papel de grano grueso texturizado. "
        "Pinceladas visibles, sangrado de color (color bleeding) y bordes húmedos. "
        "Colores suaves, translúcidos y etéreos. "
        "Sin líneas negras duras, las formas se definen por el color y la luz. "
        "Atmósfera mágica y nostálgica, estilo ilustración de libro de cuentos clásico y atemporal."
    ),
    "3d_animation": (
        "Renderizado 3D estilo cine de animación familiar de alto presupuesto. "
        "Iluminación global suave, 'subsurface scattering' en piel y materiales. "
        "Texturas táctiles y realistas (pelo suave, tela, madera pulida) pero con proporciones estilizadas y caricaturescas. "
        "Colores ricos y cinematográficos, profundidad de campo ligera (bokeh). "
        "Aspecto de juguete de alta calidad o figura de vinilo, acabado 'RenderMan' perfecto."
    ),
    "anime": (
        "Estilo anime clásico de los años 90, líneas limpias y definidas. "
        "Ojos grandes y expresivos, sombreado suave con celdas (cel shading). "
        "Estética retro, colores suaves y armoniosos. "
        "Fondos pintados a mano con detalle, iluminación suave y atmosférica. "
        "Sombreado tradicional, apariencia de animación clásica japonesa."
    ),
    "child_crayons": (
        "Hecho por un niño de 6 años con ceras de colores (crayons). "
        "Trazos torcidos, gruesos e irregulares. "
        "Colores saturados, a veces saliéndose de las líneas. "
        "Estilo infantil, ingenuo y divertido. "
        "Fondo de papel blanco, formas simples, proporciones imperfectas. "
        "Perspectiva incorrecta, apariencia genuinamente hecha a mano."
    ),
    "illustratio": (
        "Ilustración editorial de gran calidad y estilo artístico. "
        "Líneas gordas y expresivas con mucho contraste. "
        "Paleta de colores sofisticada y vibrante. "
        "Composición dinámica y texturas ricas. "
        "Estilo moderno pero con carácter artesanal, ideal para libros de cuentos premium."
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
    "water_changes": "ciclo del agua y estados de la materia (sólido, líquido, gas) de forma introductoria.",
    
    # New Topics 3-5 Years
    "feelings": "inteligencia emocional: reconocer y nombrar emociones básicas (alegría, tristeza, enfado, miedo) y estrategias simples para gestionarlas.",
    "animals": "biología básica: tipos de animales, hábitats (bosque, mar, granja) y cuidados básicos.",
    "superheroes": "valores y civismo: la ayuda a los demás, la empatía y cómo las pequeñas acciones cotidianas nos convierten en héroes.",
    
    # New Topics 5-8 Years
    "technology": "tecnología y lógica: cómo funcionan las máquinas simples, robots básicos e internet de las cosas de forma simplificada.",
    "space": "astronomía básica: planetas del sistema solar, la luna, las estrellas y la gravedad.",
    "cultures": "diversidad cultural: costumbres, vestimentas, comidas y juegos de diferentes partes del mundo.",
    "mysteries": "pensamiento crítico y deducción: uso de pistas, observación y lógica para resolver pequeños enigmas."
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
    ),

    # 3-5 Years: Feelings
    "monster_colors": (
        "El Monstruo de las Emociones se ha hecho un lío y ha mezclado todos sus colores. "
        "El protagonista debe ayudarle a separar cada emoción (Rojo/Rabia, Azul/Tristeza, Amarillo/Alegría) "
        "y ponerlas en sus botes correspondientes, recordando qué cosas le hacen sentir asi."
    ),
    "grumpy_cloud": (
        "Una pequeña nube gris de mal humor sigue al protagonista a todas partes y empieza a llover sobre él. "
        "El protagonista aprende que enfadarse está bien, pero para que salga el sol de nuevo, "
        "necesita respirar hondo y hablar de lo que le molesta."
    ),

    # 3-5 Years: Animals
    "lost_penguin": (
        "Un pequeño pingüino ha aparecido en el desierto y tiene mucho calor. "
        "El protagonista debe investigar dónde vive (Polo Sur/hielo) y guiarlo de vuelta a casa, "
        "conociendo otros animales y sus hábitats por el camino."
    ),
    "vet_day": (
        "El protagonista se convierte en ayudante de veterinario por un día. "
        "Debe averiguar qué comen diferentes animales y cómo cuidarlos: bañar a un perro sucio, "
        "dar zanahorias a un conejo y vendar la pata de un gatito."
    ),

    # 3-5 Years: Superheroes
    "everyday_hero": (
        "El protagonista recibe una capa, pero no vuela ni tiene súper fuerza. "
        "Descubre que sus súper poderes son: compartir sus juguetes, consolar a un amigo triste y ayudar a recoger. "
        "Salva el día en el parque usando la bondad."
    ),
    "invisible_shield": (
        "El protagonista aprende a crear un 'escudo de palabras amables' para protegerse de las burlas. "
        "Enseña a otros niños a usar sus propios escudos y a defender a los demás con valentía, "
        " convirtiendo la escuela en un lugar seguro."
    ),

    # 5-8 Years: Technology
    "internet_travel": (
        "El protagonista se 'digitaliza' para entrar dentro de una tablet y entregar un mensaje importante que se ha atascado. "
        "Viaja a través de cables de fibra óptica a la velocidad de la luz y conoce cómo funcionan los routers y servidores."
    ),
    "robot_friend": (
        "El protagonista construye un robot amigo pero se olvida de programarle las instrucciones. "
        "El robot lo hace todo al revés (lava los platos con tierra, barre con agua). "
        "El protagonista debe aprender a dar órdenes lógicas y secuenciales (algoritmos) para arreglarlo."
    ),

    # 5-8 Years: Space
    "gravity_boots": (
        "El protagonista gana un viaje a la Estación Espacial pero pierde sus botas de gravedad. "
        "Empieza a flotar sin control y debe aprender cómo funciona la gravedad cero para moverse, "
        "comer y dormir en el espacio antes de regresar a la Tierra."
    ),
    "planet_tour": (
        "El Sol está organizando una fiesta y ha invitado a todos los planetas, pero Plutón se siente excluido. "
        "El protagonista viaja en un cohete para entregar las invitaciones, aprendiendo las características "
        "únicas de cada planeta (Gigante gaseoso, Anillos de Saturno, etc.)."
    ),

    # 5-8 Years: Cultures
    "magic_passport": (
        "Cada vez que el protagonista sella su pasaporte mágico, viaja a un país diferente para celebrar una fiesta. "
        "Celebra el Año Nuevo Chino (Dragones), el Día de Muertos en México y Diwali en la India, "
        "aprendiendo que aunque somos diferentes, a todos nos gusta celebrar."
    ),
    "food_explorer": (
        "El protagonista debe completar el 'Libro de Sabores del Mundo'. "
        "Viaja probando sushi en Japón, pizza en Italia y tacos en México. "
        "Aprende sobre ingredientes locales y la importancia de compartir la comida en diferentes culturas."
    ),

    # 5-8 Years: Mysteries
    "museum_thief": (
        "Ha desaparecido la joya más valiosa del museo, pero no hay huellas en el suelo. "
        "El protagonista usa técnicas de observación y deducción (lupa, polvo de huellas) para descubrir "
        "que el ladrón entró por la claraboya usando un dron."
    ),
    "secret_code": (
        "El protagonista encuentra un mapa del tesoro escrito en un código extraño. "
        "Debe usar la lógica para descifrar patrones (letras por números, espejos) y encontrar "
        "el tesoro escondido, que resulta ser una cápsula del tiempo antigua."
    )
}
