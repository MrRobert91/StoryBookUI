VISUAL_STYLE_PROMPTS = {
    "cartoons": (
        "Style bande dessinée vectorielle moderne et de haute qualité. "
        "Couleurs plates et vibrantes, contours nets et audacieux. "
        "Design de personnages expressif et 'mignon', formes arrondies et amicales. "
        "Pas de textures complexes, esthétique minimaliste mais détaillée dans la composition. "
        "Éclairage doux et uniforme, style visuel similaire aux applications éducatives modernes."
    ),
    "watercolor": (
        "Style aquarelle artistique sur papier à gros grain texturé. "
        "Coups de pinceau visibles, saignement de couleur (color bleeding) et bords humides. "
        "Couleurs douces, translucides et éthérées. "
        "Pas de lignes noires dures, les formes sont définies par la couleur et la lumière. "
        "Atmosphère magique et nostalgique, style d'illustration de livre de contes classique et intemporel."
    ),
    "3d_animation": (
        "Rendu 3D style cinéma d'animation familial à gros budget. "
        "Illumination globale douce, 'subsurface scattering' sur la peau et les matériaux. "
        "Textures tactiles et réalistes (fourrure douce, tissu, bois poli) mais avec des proportions stylisées et caricaturales. "
        "Couleurs riches et cinématographiques, légère profondeur de champ (bokeh). "
        "Apparence de jouet de haute qualité ou de figurine en vinyle, finition 'RenderMan' parfaite."
    ),
    "anime": (
        "Style anime classique des années 90, lignes nettes et définies. "
        "Grands yeux expressifs, ombrage celluloïd doux (cel shading). "
        "Esthétique rétro, couleurs douces et harmonieuses. "
        "Décors peints à la main, éclairage doux et atmosphérique. "
        "Qualité anime VHS, ombrage traditionnel, look d'animation japonaise classique."
    ),
    "child_crayons": (
        "Réalisé par un enfant de 6 ans avec des crayons de couleur. "
        "Traits tordus, épais et irréguliers. "
        "Couleurs saturées, dépassant parfois des lignes. "
        "Style enfantin, naïf et amusant. "
        "Fond de papier blanc, formes simples, proportions imparfaites. "
        "Perspective incorrecte, apparence véritablement faite à main."
    ),
    "illustratio": (
        "Illustration éditoriale de haute qualité et style artistique. "
        "Lignes épaisses et expressives avec beaucoup de contraste. "
        "Palette de couleurs sophistiquée et vibrante. "
        "Composition dynamique et textures riches. "
        "Style moderne mais avec un caractère artisanal, idéal pour les livres de contes haut de gamme."
    )
}

TOPIC_PROMPTS = {
    "shapes_sizes": "géométrie de base : identification des formes (cercle, carré, triangle) et comparaison des tailles (grand, moyen, petit).",
    "human_body": "parties du corps et les cinq sens. Reconnaissance de base des fonctions corporelles simples.",
    "sound": "physique du son : vibrations, écho, types de sons (graves/aigus) et silence.",
    "water_changes": "cycle de l'eau et états de la matière (solide, liquide, gaz) de manière introductive.",
    "feelings": "intelligence émotionnelle : reconnaître et nommer les émotions de base (joie, tristesse, colère, peur) et stratégies simples pour les gérer.",
    "animals": "biologie de base : types d'animaux, habitats (forêt, mer, ferme) et soins de base.",
    "superheroes": "valeurs et citoyenneté : aider les autres, empathie et comment les petites actions quotidiennes font de nous des héros.",
    "technology": "technologie et logique : comment fonctionnent les machines simples, robots de base et internet des objets de manière simplifiée.",
    "space": "astronomie de base : planètes du système solaire, la lune, les étoiles et la gravité.",
    "cultures": "diversité culturelle : coutumes, vêtements, aliments et jeux de différentes parties du monde.",
    "mysteries": "pensée critique et déduction : utilisation d'indices, observation et logique pour résoudre de petits énigmes."
}

MISSION_PROMPTS = {
    "land_of_shapes": (
        "Le protagoniste voyage au 'Pays des Formes', un endroit où tout est fait de figures géométriques. "
        "Le conflit est que le Pont des Formes est cassé et qu'il manque des pièces spécifiques. "
        "Le protagoniste doit trouver des cercles pour les roues, des carrés pour les maisons et des triangles pour le pont."
    ),
    "big_or_small": (
        "Le protagoniste trouve une loupe magique qui rend les choses grandes ou petites. "
        "Il doit l'utiliser pour aider ses amis animaux : rendre petite une roche géante qui bloque le chemin d'une fourmi, "
        "ou rendre grande une graine pour qu'elle nourrisse de nombreux oiseaux. Enseigne la relativité de la taille."
    ),
    "five_senses": (
        "Le protagoniste perd ses lunettes (ou quelque chose de similaire) et doit utiliser ses quatre autres sens pour les retrouver. "
        "Il doit écouter les indices, sentir l'arôme des biscuits là où il les a laissés, toucher des textures rugueuses, etc. "
        "Chaque chapitre se concentre sur un sens différent."
    ),
    "brave_tooth": (
        "Le protagoniste a sa première dent qui bouge et a peur. "
        "Sa mission est d'enquêter sur ce qui se passe avec les dents et de rencontrer la 'Fée des Dents' ou la 'Petite Souris'. "
        "L'histoire normalise le processus naturel de perte des dents de lait."
    ),
    "lost_orchestra": (
        "Dans la Forêt Silencieuse, les instruments ont perdu leur voix. "
        "Le protagoniste découvre que tout son naît d'une vibration. "
        "Il doit 'réveiller' les instruments en les faisant vibrer de différentes manières (frapper, souffler, gratter) "
        "pour que l'orchestre puisse rejouer."
    ),
    "mysterious_echo": (
        "Le protagoniste explore une grotte où l'écho ne répète pas, mais répond. "
        "Il découvre que le son voyage comme des ondes invisibles et rebondit sur les parois. "
        "La mission est d'utiliser l'écho pour trouver la sortie d'un labyrinthe sombre."
    ),
    "traveling_drop": (
        "Le protagoniste rétrécit à une taille microscopique et monte sur une goutte d'eau nommée 'Flu'. "
        "Ils voyagent ensemble depuis la mer (évaporation), se transforment en nuage (condensation) et tombent sous forme de pluie (précipitation) sur une montagne enneigée. "
        "C'est un voyage d'aventure à travers le cycle hydrologique."
    ),
    "melting_ice": (
        "Le Royaume de Glace fond parce que le chauffage magique est resté allumé. "
        "Le protagoniste doit comprendre comment la chaleur transforme le solide en liquide. "
        "Il doit refroidir l'environnement pour que l'eau redevienne de la glace solide et sauver le château."
    ),
    "monster_colors": (
        "Le Monstre des Émotions a fait un gâchis et a mélangé toutes ses couleurs. "
        "Le protagoniste doit l'aider à séparer chaque émotion (Rouge/Colère, Bleu/Tristesse, Jaune/Joie) "
        "et à les mettre dans leurs bocaux correspondants, en se rappelant ce qui lui fait ressentir cela."
    ),
    "grumpy_cloud": (
        "Un petit nuage gris de mauvaise humeur suit le protagoniste partout et commence à pleuvoir sur lui. "
        "Le protagoniste apprend qu'être en colère est normal, mais pour que le soleil revienne, "
        "il doit respirer profondément et parler de ce qui le dérange."
    ),
    "lost_penguin": (
        "Un petit pingouin est apparu dans le désert et a très chaud. "
        "Le protagoniste doit enquêter sur son lieu de vie (Pôle Sud/glace) et le guider vers sa maison, "
        "en rencontrant d'autres animaux et leurs habitats en chemin."
    ),
    "vet_day": (
        "Le protagoniste devient assistant vétérinaire pour une journée. "
        "Il doit découvrir ce que mangent les différents animaux et comment s'en occuper : baigner un chien sale, "
        "donner des carottes à un lapin et panser la patte d'un chaton."
    ),
    "everyday_hero": (
        "Le protagoniste reçoit une cape, mais ne vole pas et n'a pas de super-force. "
        "Il découvre que ses super-pouvoirs sont : partager ses jouets, consoler un ami triste et aider à ranger. "
        "Il sauve la journée dans le parc grâce à la gentillesse."
    ),
    "invisible_shield": (
        "Le protagoniste apprend à créer un 'bouclier de mots gentils' pour se protéger des moqueries. "
        "Il enseigne à d'autres enfants à utiliser leurs propres boucliers et à défendre les autres avec courage, "
        "transformant l'école en un lieu sûr."
    ),
    "internet_travel": (
        "Le protagoniste se 'numérise' pour entrer dans une tablette et livrer un message important qui est resté bloqué. "
        "Il voyage à travers des câbles de fibre optique à la vitesse de la lumière et apprend comment fonctionnent les routeurs et les serveurs."
    ),
    "robot_friend": (
        "Le protagoniste construit un ami robot mais oublie de lui programmer les instructions. "
        "Le robot fait tout à l'envers (lave la vaisselle avec de la terre, balaye avec de l'eau). "
        "Le protagoniste doit apprendre à donner des ordres logiques et séquentiels (algorithmes) pour le réparer."
    ),
    "gravity_boots": (
        "Le protagoniste gagne un voyage à la Station Spatiale mais perd ses bottes de gravité. "
        "Il commence à flotter sans contrôle et doit apprendre comment fonctionne la gravité zéro pour se déplacer, "
        "manger et dormir dans l'espace avant de retourner sur Terre."
    ),
    "planet_tour": (
        "Le Soleil organise une fête et a invité toutes les planètes, mais Pluton se sent exclu. "
        "Le protagoniste voyage dans une fusée pour livrer les invitations, apprenant les caractéristiques "
        "uniques de chaque planète (Géante gazeuse, Anneaux de Saturne, etc.)."
    ),
    "magic_passport": (
        "Chaque fois que le protagoniste tamponne son passeport magique, il voyage dans un pays différent pour célébrer une fête. "
        "Il célèbre le Nouvel An chinois (Dragons), le Jour des Morts au Mexique et Diwali en Inde, "
        "apprenant que même si nous sommes différents, nous aimons tous faire la fête."
    ),
    "food_explorer": (
        "Le protagoniste doit compléter le 'Livre des Saveurs du Monde'. "
        "Il voyage en goûtant des sushis au Japon, des pizzas en Italie et des tacos au Mexique. "
        "Il apprend les ingrédients locaux et l'importance de partager la nourriture dans différentes cultures."
    ),
    "museum_thief": (
        "Le bijou le plus précieux du musée a disparu, mais il n'y a pas d'empreintes sur le sol. "
        "Le protagoniste utilise des techniques d'observation et de déduction (loupe, poudre à empreintes) pour découvrir "
        "que le voleur est entré par la lucarne en utilisant un drone."
    ),
    "secret_code": (
        "Le protagoniste trouve une carte au trésor écrite dans un code étrange. "
        "Il doit utiliser la logique pour déchiffrer des schémas (lettres pour chiffres, miroirs) et trouver "
        "le trésor caché, qui s'avère être une ancienne capsule temporelle."
    )
}

STORY_SYSTEM_PROMPTS = {
    "system": "Générez des histoires fantastiques créatives pour enfants avec exactement {num_chapters} chapitres.",
    "guidelines": (
        "DIRECTIVES IMPORTANTES :\n"
        "- Chaque chapitre doit comporter environ {words_per_chapter} mots\n"
        "- Le contenu doit être adapté aux familles et approprié pour les enfants\n"
        "- Utilisez des descriptions colorées et imaginatives\n"
        "- Incluez des messages positifs et des personnages sympathiques\n"
        "- Renvoyez un JSON structuré avec un titre et un tableau de chapitres\n"
        "- Chaque chapitre doit avoir un titre et un champ de contenu"
    ),
    "image_system": (
        "Créez une invite d'image concise adaptée aux livres pour enfants. "
        "Le résultat DOIT décrire une illustration cohérente avec le style visuel demandé. "
        "Concentrez-vous sur la description de la scène, des personnages et des émotions de manière claire pour un jeune public. "
        "ÉVITEZ toute imagerie effrayante, violente, sombre ou réaliste/photoréaliste. "
        "Ne mentionnez pas d'appareils photo, d'objectifs ou de termes photographiques. "
        "Renvoyez UNIQUEMENT le texte de l'invite."
    )
}

GUIDED_STORY_FORMAT = {
    "system": "Vous êtes un écrivain expert en histoires pour enfants. Écrivez une histoire éducative pour les enfants de {age_group} ans.",
    "data_labels": {
        "protagonist": "Protagoniste",
        "topic": "Sujet Scientifique",
        "mission": "Trame/Mission"
    },
    "structure": (
        "STRUCTURE OBLIGATOIRE :\n"
        "1. Titre : Créatif et lié à la mission.\n"
        "2. Chapitres : Divisez l'histoire en {num_chapters} chapitres courts.\n"
        "3. Contenu : Le ton doit être amusant, sûr et facile à lire. "
        "Assurez-vous d'expliquer le concept scientifique naturellement dans le récit.\n"
        "Renvoyez UNIQUEMENT le JSON avec le format établi."
    )
}
