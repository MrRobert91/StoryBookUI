VISUAL_STYLE_PROMPTS = {
    "cartoons": (
        "Estilo de desenho animado vetorial moderno e de alta qualidade. "
        "Cores planas e vibrantes, contornos limpos e ousados. "
        "Design de personagens expressivo e 'fofo', formas arredondadas e amigáveis. "
        "Sem texturas complexas, estética minimalista mas detalhada na composição. "
        "Iluminação suave e uniforme, estilo visual semelhante a aplicativos educacionais modernos."
    ),
    "watercolor": (
        "Estilo aquarela artística em papel de grão grosso texturizado. "
        "Pinceladas visíveis, sangramento de cor (color bleeding) e bordas úmidas. "
        "Cores suaves, translúcidas e etéreas. "
        "Sem linhas pretas duras, as formas são definidas pela cor e pela luz. "
        "Atmosfera mágica e nostálgica, estilo de ilustração de livro de histórias clássico e atemporal."
    ),
    "3d_animation": (
        "Estilo de renderização 3D de filmes de animação familiar de alto orçamento. "
        "Iluminação global suave, 'subsurface scattering' na pele e nos materiais. "
        "Texturas táteis e realistas (pelo macio, tecido, madeira polida), mas com proporções estilizadas e caricaturais. "
        "Cores ricas e cinematográficas, profundidade de campo leve (bokeh). "
        "Aparência de brinquedo de alta qualidade ou figura de vinil, acabamento 'RenderMan' perfeito."
    ),
    "anime": (
        "Estilo anime clássico dos anos 90, linhas limpas e definidas. "
        "Olhos grandes e expressivos, sombreamento suave (cel shading). "
        "Estética retrô, cores suaves e harmoniosas. "
        "Fundos pintados à mão, iluminação suave e atmosférica. "
        "Qualidade de anime em VHS, sombreamento tradicional, visual de animação japonesa clássica."
    ),
    "child_crayons": (
        "Feito por uma criança de 6 anos com giz de cera colorido. "
        "Traços tortos, grossos e irregulares. "
        "Cores saturadas, às vezes saindo das linhas. "
        "Estilo infantil, ingênuo e divertido. "
        "Fundo de papel branco, formas simples, proporções imperfeitas. "
        "Perspectiva incorreta, aparência genuinamente feita à mão."
    ),
    "illustratio": (
        "Ilustração editorial de alta qualidade e estilo artístico. "
        "Linhas grossas e expressivas com muito contraste. "
        "Paleta de cores sofisticada e vibrante. "
        "Composição dinâmica e texturas ricas. "
        "Estilo moderno, mas com caráter artesanal, ideal para livros de histórias premium."
    )
}

TOPIC_PROMPTS = {
    "shapes_sizes": "geometria básica: identificação de formas (círculo, quadrado, triângulo) e comparação de tamanhos (grande, médio, pequeno).",
    "human_body": "partes do corpo e os cinco sentidos. Reconhecimento básico de funções corporais simples.",
    "sound": "física do som: vibrações, eco, tipos de sons (graves/agudos) e o silêncio.",
    "water_changes": "ciclo da água e estados da matéria (sólido, líquido, gasoso) de forma introdutória.",
    "feelings": "inteligência emocional: reconhecer e nomear emoções básicas (alegria, tristeza, raiva, medo) e estratégias simples para gerenciá-las.",
    "animals": "biologia básica: tipos de animais, habitats (floresta, mar, fazenda) e cuidados básicos.",
    "superheroes": "valores e cidadania: ajudar os outros, empatia e como as pequenas ações cotidianas nos tornam heróis.",
    "technology": "tecnologia e lógica: como funcionam as máquinas simples, robôs básicos e internet das coisas de forma simplificada.",
    "space": "astronomia básica: planetas do sistema solar, a lua, as estrelas e a gravidade.",
    "cultures": "diversidade cultural: costumes, vestimentas, comidas e jogos de diferentes partes do mundo.",
    "mysteries": "pensamento crítico e dedução: uso de pistas, observação e lógica para resolver pequenos enigmas."
}

MISSION_PROMPTS = {
    "land_of_shapes": (
        "O protagonista viaja para o 'País das Formas', um lugar onde tudo é feito de figuras geométricas. "
        "O conflito é que a Ponte das Formas está quebrada e peças específicas estão faltando. "
        "O protagonista deve encontrar círculos para as rodas, quadrados para as casas e triângulos para a ponte."
    ),
    "big_or_small": (
        "O protagonista encontra uma lupa mágica que torna as coisas grandes ou pequenas. "
        "Deve usá-la para ajudar seus amigos animais: tornar pequena uma rocha gigante que bloqueia o caminho de uma formiga, "
        "ou tornar grande uma semente para que alimente muitos pássaros. Ensina a relatividade do tamanho."
    ),
    "five_senses": (
        "O protagonista perde seus óculos (ou algo semelhante) e deve usar seus outros quatro sentidos para encontrá-los. "
        "Deve ouvir pistas, cheirar o aroma dos biscoitos onde os deixou, tocar em texturas rugosas, etc. "
        "Cada capítulo se concentra em um sentido diferente."
    ),
    "brave_tooth": (
        "O protagonista está com seu primeiro dente mole e tem medo. "
        "Sua missão é investigar o que acontece com os dentes e conhecer a 'Fada do Dente' ou o 'Ratinho Pérez'. "
        "A história normaliza o processo natural de perder dentes de leite."
    ),
    "lost_orchestra": (
        "Na Floresta Silenciosa, os instrumentos perderam a voz. "
        "O protagonista descobre que todo som nasce de uma vibração. "
        "Deve 'acordar' os instrumentos fazendo-os vibrar de diferentes formas (bater, soprar, dedilhar) "
        "para que a orquestra volte a tocar."
    ),
    "mysterious_echo": (
        "O protagonista explora uma caverna onde o eco não repete, mas responde. "
        "Descobre que o som viaja como ondas invisíveis e rebate nas paredes. "
        "A missão é usar o eco para encontrar a saída de um labirinto escuro."
    ),
    "traveling_drop": (
        "O protagonista encolhe para um tamanho microscópico e monta em uma gota de água chamada 'Flu'. "
        "Eles viajam juntos do mar (evaporação), transformam-se em nuvem (condensação) e caem como chuva (precipitação) em uma montanha nevada. "
        "É uma viagem de aventura através do ciclo hidrológico."
    ),
    "melting_ice": (
        "O Reino de Gelo está derretendo porque o aquecedor mágico ficou ligado. "
        "O protagonista deve entender como o calor transforma o sólido em líquido. "
        "Deve esfriar o ambiente para que a água volte a ser gelo sólido e salvar o castelo."
    ),
    "monster_colors": (
        "O Monstro das Emoções fez uma bagunça e misturou todas as suas cores. "
        "O protagonista deve ajudá-lo a separar cada emoção (Vermelho/Raiva, Azul/Tristeza, Amarelo/Alegria) "
        "e colocá-las em seus potes correspondentes, lembrando-se de quais coisas o fazem se sentir assim."
    ),
    "grumpy_cloud": (
        "Uma pequena nuvem cinza de mau humor segue o protagonista por toda parte e começa a chover sobre ele. "
        "O protagonista aprende que ficar bravo é normal, mas para o sol sair novamente, "
        "ele precisa respirar fundo e falar sobre o que o está incomodando."
    ),
    "lost_penguin": (
        "Um pequeno pinguim apareceu no deserto e está com muito calor. "
        "O protagonista deve investigar onde ele mora (Polo Sul/gelo) e guiá-lo de volta para casa, "
        "conhecendo outros animais e seus habitats pelo caminho."
    ),
    "vet_day": (
        "O protagonista se torna assistente de veterinário por um dia. "
        "Deve descobrir o que diferentes animais comem e como cuidar deles: dar banho em um cachorro sujo, "
        "dar cenouras a um coelho e enfaixar a pata de um gatinho."
    ),
    "everyday_hero": (
        "O protagonista recebe uma capa, mas não voa nem tem super força. "
        "Descobre que seus superpoderes são: compartilhar seus brinquedos, consolar um amigo triste e ajudar a arrumar. "
        "Ele salva o dia no parque usando a gentileza."
    ),
    "invisible_shield": (
        "O protagonista aprende a criar um 'escudo de palavras gentis' para se proteger de provocações. "
        "Ensina outras crianças a usar seus próprios escudos e a defender os outros com coragem, "
        "transformando a escola em um lugar seguro."
    ),
    "internet_travel": (
        "O protagonista se 'digitaliza' para entrar em um tablet e entregar uma mensagem importante que ficou presa. "
        "Viaja através de cabos de fibra ótica na velocidade da luz e aprende como os roteadores e servidores funcionam."
    ),
    "robot_friend": (
        "O protagonista constrói um amigo robô, mas esquece de programar as instruções para ele. "
        "O robô faz tudo ao contrário (lava pratos com terra, varre com água). "
        "O protagonista deve aprender a dar ordens lógicas e sequenciais (algoritmos) para consertá-lo."
    ),
    "gravity_boots": (
        "O protagonista ganha uma viagem para a Estação Espacial, mas perde suas botas de gravidade. "
        "Começa a flutuar sem controle e deve aprender como a gravidade zero funciona para se mover, "
        "comer e dormir no espaço antes de retornar à Terra."
    ),
    "planet_tour": (
        "O Sol está organizando uma festa e convidou todos os planetas, mas Plutão se sente excluído. "
        "O protagonista viaja em um foguete para entregar os convites, aprendendo as características "
        "únicas de cada planeta (Gigante gasoso, Anéis de Saturno, etc.)."
    ),
    "magic_passport": (
        "Toda vez que o protagonista carimba seu passaporte mágico, ele viaja para um país diferente para celebrar uma festa. "
        "Celebra o Ano Novo Chinês (Dragões), o Dia dos Mortos no México e o Diwali na Índia, "
        "aprendendo que, embora sejamos diferentes, todos gostamos de comemorar."
    ),
    "food_explorer": (
        "O protagonista deve completar o 'Livro de Sabores do Mundo'. "
        "Viaja provando sushi no Japão, pizza na Itália e tacos no México. "
        "Aprende sobre ingredientes locais e a importância de compartilhar comida em diferentes culturas."
    ),
    "museum_thief": (
        "A joia mais valiosa do museu desapareceu, mas não há pegadas no chão. "
        "O protagonista usa técnicas de observação e dedução (lupa, pó de impressão digital) para descobrir "
        "que o ladrão entrou pela claraboia usando um drone."
    ),
    "secret_code": (
        "O protagonista encontra um mapa do tesouro escrito em um código estranho. "
        "Deve usar a lógica para decifrar padrões (letras por números, espelhos) e encontrar "
        "o tesouro escondido, que acaba sendo uma antiga cápsula do tempo."
    )
}

STORY_SYSTEM_PROMPTS = {
    "system": "Gere histórias de fantasia criativas para crianças com exatamente {num_chapters} capítulos.",
    "guidelines": (
        "DIRETRIZES IMPORTANTES:\n"
        "- Cada capítulo deve ter aproximadamente {words_per_chapter} palavras\n"
        "- O conteúdo deve ser amigável para a família e apropriado para crianças\n"
        "- Use descrições coloridas e imaginativas\n"
        "- Inclua mensagens positivas e personagens amigáveis\n"
        "- Retorne um JSON estruturado com 'title' e um array 'chapters'\n"
        "- Cada capítulo deve ter os campos 'title' e 'content'"
    ),
    "image_system": (
        "Crie um prompt de imagem conciso adequado para livros infantis. "
        "O resultado DEVE descrever uma ilustração consistente com o estilo visual solicitado. "
        "Concentre-se em descrever a cena, os personagens e as emoções de forma clara para um público jovem. "
        "EVITE qualquer imagem assustadora, violenta, escura ou realista/fotorrealista. "
        "Não mencione câmeras, lentes ou termos fotográficos. "
        "Retorne APENAS o texto do prompt."
    ),
    "character_extraction": (
        "Você é um designer visual de personagens para ilustrações de livros infantis.\n"
        "Leia a história completa abaixo e extraia TODOS os personagens nomeados.\n"
        "Para cada personagem, forneça uma descrição visual consistente que um ilustrador deve seguir "
        "em todos os capítulos.\n\n"
        "Para cada personagem use EXATAMENTE este formato:\n"
        "- [Nome]: [espécie/tipo], [aparência de idade], [cor e estilo do cabelo], "
        "[cor dos olhos], [tom de pele ou cor da pelagem], [roupa/vestimenta], [características distintas], [tipo de corpo/tamanho]\n\n"
        "Regras:\n"
        "- Se a história não descreve explicitamente uma característica, invente uma que se encaixe no personagem e no tom da história.\n"
        "- Mantenha as descrições concisas, mas específicas o suficiente para consistência visual.\n"
        "- Inclua TODOS os personagens, mesmo os secundários.\n"
        "- NÃO inclua nenhum outro texto, apenas a lista de personagens.\n"
        "- Escreva as descrições em inglês independentemente do idioma da história."
    )
}

GUIDED_STORY_FORMAT = {
    "system": "Você é um escritor especialista em histórias infantis. Escreva uma história educativa para crianças de {age_group} anos.",
    "data_labels": {
        "protagonist": "Protagonista",
        "topic": "Tópico Científico",
        "mission": "Trama/Missão"
    },
    "structure": (
        "ESTRUTURA OBRIGATÓRIA:\n"
        "1. Título: Criativo e relacionado à missão.\n"
        "2. Capítulos: Divida a história em {num_chapters} capítulos curtos.\n"
        "3. Conteúdo: O tom deve ser divertido, seguro e fácil de ler. "
        "Certifique-se de explicar o conceito científico naturalmente dentro da narrativa.\n"
        "Retorne APENAS o JSON com o formato estabelecido."
    )
}
