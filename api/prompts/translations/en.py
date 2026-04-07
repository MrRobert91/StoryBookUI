VISUAL_STYLE_PROMPTS = {
    "cartoons": (
        "Modern and high-quality vector cartoon style. "
        "Flat and vibrant colors, clean and bold outlines. "
        "Expressive and 'cute' character design, rounded and friendly shapes. "
        "No complex textures, minimalist but detailed in composition. "
        "Soft and even lighting, visual style similar to modern educational apps."
    ),
    "watercolor": (
        "Artistic watercolor style on textured thick grain paper. "
        "Visible brushstrokes, color bleeding and wet edges. "
        "Soft, translucent and ethereal colors. "
        "No hard black lines, shapes are defined by color and light. "
        "Magical and nostalgic atmosphere, classic and timeless storybook illustration style."
    ),
    "3d_animation": (
        "3D rendering style of high-budget family animation films. "
        "Soft global illumination, subsurface scattering on skin and materials. "
        "Tactile and realistic textures (soft fur, fabric, polished wood) but with stylized and cartoonish proportions. "
        "Rich and cinematic colors, slight depth of field (bokeh). "
        "High-quality toy or vinyl figure look, perfect 'RenderMan' finish."
    ),
    "anime": (
        "Classic 90s anime style, clean and defined lines. "
        "Large and expressive eyes, soft cell shading. "
        "Retro aesthetic, soft and harmonious colors. "
        "Hand-painted backgrounds, soft and atmospheric lighting. "
        "VHS anime quality, traditional shading, classic Japanese animation look."
    ),
    "child_crayons": (
        "Made by a 6-year-old child with colored crayons. "
        "Crooked, thick and irregular strokes. "
        "Saturated colors, sometimes going outside the lines. "
        "Childish, naive and fun style. "
        "White paper background, simple shapes, imperfect proportions. "
        "Incorrect perspective, genuinely handmade look."
    ),
    "illustratio": (
        "High-quality editorial illustration and artistic style. "
        "Thick and expressive lines with high contrast. "
        "Sophisticated and vibrant color palette. "
        "Dynamic composition and rich textures. "
        "Modern style but with a handmade character, ideal for premium storybooks."
    )
}

TOPIC_PROMPTS = {
    "shapes_sizes": "basic geometry: identification of shapes (circle, square, triangle) and comparison of sizes (large, medium, small).",
    "human_body": "body parts and the five senses. Basic recognition of simple body functions.",
    "sound": "physics of sound: vibrations, echo, types of sounds (bass/treble) and silence.",
    "water_changes": "water cycle and states of matter (solid, liquid, gas) as an introduction.",
    "feelings": "emotional intelligence: recognizing and naming basic emotions (joy, sadness, anger, fear) and simple strategies to manage them.",
    "animals": "basic biology: types of animals, habitats (forest, sea, farm) and basic care.",
    "superheroes": "values and citizenship: helping others, empathy and how small daily actions make us heroes.",
    "technology": "technology and logic: how simple machines work, basic robots and internet of things in a simplified way.",
    "space": "basic astronomy: planets of the solar system, the moon, stars and gravity.",
    "cultures": "cultural diversity: customs, clothing, foods and games from different parts of the world.",
    "mysteries": "critical thinking and deduction: use of clues, observation and logic to solve small enigmas."
}

MISSION_PROMPTS = {
    "land_of_shapes": (
        "The protagonist travels to 'Shape Land', a place where everything is made of geometric figures. "
        "The conflict is that the Bridge of Shapes is broken and specific pieces are missing. "
        "The protagonist must find circles for wheels, squares for houses, and triangles for the bridge."
    ),
    "big_or_small": (
        "The protagonist finds a magic magnifying glass that makes things large or small. "
        "They must use it to help their animal friends: make a giant rock that blocks an ant's path small, "
        "or make a seed large so it feeds many birds. Teaches relativity of size."
    ),
    "five_senses": (
        "The protagonist loses their glasses (or something similar) and must use their other four senses to find them. "
        "They must listen for clues, smell the aroma of cookies where they left them, touch rough textures, etc. "
        "Each chapter focuses on a different sense."
    ),
    "brave_tooth": (
        "The protagonist has their first loose tooth and is afraid. "
        "Their mission is to investigate what happens with teeth and meet the 'Tooth Fairy'. "
        "The story normalizes the natural process of losing baby teeth."
    ),
    "lost_orchestra": (
        "In the Silent Forest, the instruments have lost their voice. "
        "The protagonist discovers that all sound is born from a vibration. "
        "They must 'wake up' the instruments by making them vibrate in different ways (hitting, blowing, strumming) "
        "so the orchestra can play again."
    ),
    "mysterious_echo": (
        "The protagonist explores a cave where the echo doesn't repeat, but answers. "
        "They discover that sound travels as invisible waves and bounces off walls. "
        "The mission is to use the echo to find the way out of a dark labyrinth."
    ),
    "traveling_drop": (
        "The protagonist shrinks to microscopic size and rides on a water drop named 'Flu'. "
        "They travel together from the sea (evaporation), turn into a cloud (condensation) and fall as rain (precipitation) on a snowy mountain. "
        "It's an adventure trip through the hydrological cycle."
    ),
    "melting_ice": (
        "The Ice Kingdom is melting because the magic heater has been left on. "
        "The protagonist must understand how heat transforms solid into liquid. "
        "They must cool the environment so the water becomes solid ice again and save the castle."
    ),
    "monster_colors": (
        "The Emotion Monster has made a mess and mixed all his colors. "
        "The protagonist must help him separate each emotion (Red/Anger, Blue/Sadness, Yellow/Joy) "
        "and put them in their corresponding jars, remembering what things make him feel that way."
    ),
    "grumpy_cloud": (
        "A small grumpy gray cloud follows the protagonist everywhere and starts raining on him. "
        "The protagonist learns that being angry is okay, but for the sun to come out again, "
        "he needs to take a deep breath and talk about what's bothering him."
    ),
    "lost_penguin": (
        "A small penguin has appeared in the desert and is very hot. "
        "The protagonist must investigate where he lives (South Pole/ice) and guide him back home, "
        "meeting other animals and their habitats along the way."
    ),
    "vet_day": (
        "The protagonist becomes a vet's assistant for a day. "
        "They must figure out what different animals eat and how to care for them: bathe a dirty dog, "
        "give carrots to a rabbit and bandage a kitten's paw."
    ),
    "everyday_hero": (
        "The protagonist receives a cape, but doesn't fly or have super strength. "
        "He discovers his super powers are: sharing his toys, comforting a sad friend and helping to clean up. "
        "He saves the day in the park using kindness."
    ),
    "invisible_shield": (
        "The protagonist learns to create a 'kind words shield' to protect himself from teasing. "
        "He teaches other children to use their own shields and to defend others with courage, "
        "turning the school into a safe place."
    ),
    "internet_travel": (
        "The protagonist 'digitalizes' to go inside a tablet and deliver an important message that got stuck. "
        "He travels through fiber optic cables at the speed of light and learns how routers and servers work."
    ),
    "robot_friend": (
        "The protagonist builds a robot friend but forgets to program the instructions for him. "
        "The robot does everything backwards (washes dishes with dirt, sweeps with water). "
        "The protagonist must learn to give logical and sequential orders (algorithms) to fix it."
    ),
    "gravity_boots": (
        "The protagonist wins a trip to the Space Station but loses his gravity boots. "
        "He starts floating uncontrollably and must learn how zero gravity works to move, "
        "eat and sleep in space before returning to Earth."
    ),
    "planet_tour": (
        "The Sun is organizing a party and has invited all the planets, but Pluto feels excluded. "
        "The protagonist travels in a rocket to deliver the invitations, learning the unique "
        "characteristics of each planet (Gas giant, Saturn's rings, etc.)."
    ),
    "magic_passport": (
        "Every time the protagonist stamps his magic passport, he travels to a different country to celebrate a party. "
        "He celebrates Chinese New Year (Dragons), Day of the Dead in Mexico and Diwali in India, "
        "learning that although we are different, we all like to celebrate."
    ),
    "food_explorer": (
        "The protagonist must complete the 'Flavors of the World Book'. "
        "He travels tasting sushi in Japan, pizza in Italy and tacos in Mexico. "
        "He learns about local ingredients and the importance of sharing food in different cultures."
    ),
    "museum_thief": (
        "The museum's most valuable jewel has disappeared, but there are no footprints on the floor. "
        "The protagonist uses observation and deduction techniques (magnifying glass, fingerprint powder) to discover "
        "that the thief entered through the skylight using a drone."
    ),
    "secret_code": (
        "The protagonist finds a treasure map written in a strange code. "
        "They must use logic to decipher patterns (letters for numbers, mirrors) and find "
        "the hidden treasure, which turns out to be an ancient time capsule."
    )
}

STORY_SYSTEM_PROMPTS = {
    "system": "Generate creative fantasy stories for children with exactly {num_chapters} chapters.",
    "guidelines": (
        "IMPORTANT GUIDELINES:\n"
        "- Each chapter must have approximately {words_per_chapter} words\n"
        "- Content must be family-friendly and appropriate for children\n"
        "- Use colorful, imaginative descriptions\n"
        "- Include positive messages and friendly characters\n"
        "- Return structured JSON with 'title' and 'chapters' array\n"
        "- Each chapter must have 'title' and 'content' fields"
    ),
    "image_system": (
        "Create a concise image prompt suitable for children's books. "
        "The result MUST describe an illustration consistent with the requested visual style. "
        "Focus on describing the scene, characters, and emotions clearly for a young audience. "
        "AVOID any scary, violent, dark, or realistic/photorealistic imagery. "
        "Do not mention cameras, lenses, or photographic terms. "
        "Return ONLY the prompt text."
    ),
    "character_extraction": (
        "You are a visual character designer for children's book illustrations.\n"
        "Read the complete story below and extract EVERY named character.\n"
        "For each character, provide a consistent visual description that an illustrator must follow "
        "across all chapters.\n\n"
        "For each character output EXACTLY this format:\n"
        "- [Name]: [species/type], [age appearance], [hair color and style], "
        "[eye color], [skin tone or fur color], [clothing/outfit], [distinguishing features], [body type/size]\n\n"
        "Rules:\n"
        "- If the story does not explicitly describe a feature, invent one that fits the character and story tone.\n"
        "- Keep descriptions concise but specific enough for visual consistency.\n"
        "- Include ALL characters, even minor ones.\n"
        "- Do NOT include any other text, only the character list.\n"
        "- Write descriptions in English regardless of story language."
    )
}

GUIDED_STORY_FORMAT = {
    "system": "You are an expert children's story writer. Write an educational story for children for children aged {age_group}.",
    "data_labels": {
        "protagonist": "Protagonist",
        "topic": "Scientific Topic",
        "mission": "Plot/Mission"
    },
    "structure": (
        "MANDATORY STRUCTURE:\n"
        "1. Title: Creative and related to the mission.\n"
        "2. Chapters: Divide the story into {num_chapters} short chapters.\n"
        "3. Content: The tone should be fun, safe and easy to read. "
        "Make sure to explain the scientific concept naturally within the narrative.\n"
        "Return ONLY the JSON with the established format."
    )
}
