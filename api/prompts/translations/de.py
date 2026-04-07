VISUAL_STYLE_PROMPTS = {
    "cartoons": (
        "Moderner und hochwertiger Vektor-Cartoon-Stil. "
        "Flache und lebendige Farben, saubere und kräftige Umrisse. "
        "Expressives und 'süßes' Charakterdesign, abgerundete und freundliche Formen. "
        "Keine komplexen Texturen, minimalistische, aber detaillierte Komposition. "
        "Weiche und gleichmäßige Beleuchtung, visueller Stil ähnlich wie bei modernen Lern-Apps."
    ),
    "watercolor": (
        "Künstlerischer Aquarellstil auf strukturiertem, grobkörnigem Papier. "
        "Sichtbare Pinselstriche, verlaufende Farben (Color Bleeding) und feuchte Ränder. "
        "Weiche, durchscheinende und ätherische Farben. "
        "Keine harten schwarzen Linien, Formen werden durch Farbe und Licht definiert. "
        "Magische und nostalgische Atmosphäre, klassischer und zeitloser Bilderbuch-Illustrationsstil."
    ),
    "3d_animation": (
        "3D-Rendering-Stil von hochbudgetierten Familienanimationsfilmen. "
        "Weiche globale Beleuchtung, Subsurface Scattering auf Haut und Materialien. "
        "Haptische und realistische Texturen (weiches Fell, Stoff, poliertes Holz), aber mit stilisierten und cartoonhaften Proportionen. "
        "Reiche und filmische Farben, leichte Tiefenschärfe (Bokeh). "
        "Aussehen eines hochwertigen Spielzeugs oder einer Vinylfigur, perfektes 'RenderMan'-Finish."
    ),
    "anime": (
        "Klassischer 90er-Jahre-Anime-Stil, saubere und definierte Linien. "
        "Große und ausdrucksstarke Augen, weiches Cell-Shading. "
        "Retro-Ästhetik, weiche und harmonische Farben. "
        "Handgemalte Hintergründe, weiche und atmosphärische Beleuchtung. "
        "VHS-Anime-Qualität, traditionelle Schattierung, klassischer japanischer Animationslook."
    ),
    "child_crayons": (
        "Gezeichnet von einem 6-jährigen Kind mit Buntstiften. "
        "Krumme, dicke und unregelmäßige Striche. "
        "Gesättigte Farben, die manchmal über die Linien hinausgehen. "
        "Kindlicher, naiver und lustiger Stil. "
        "Weißer Papierhintergrund, einfache Formen, unvollkommene Proportionen. "
        "Falsche Perspektive, echt handgemachtes Aussehen."
    ),
    "illustratio": (
        "Hochwertiger redaktioneller Illustrations- und Kunststil. "
        "Dicke und expressive Linien mit hohem Kontrast. "
        "Sophistizierte und lebendige Farbpalette. "
        "Dynamische Komposition und reiche Texturen. "
        "Moderner Stil, aber mit handwerklichem Charakter, ideal für Premium-Bilderbücher."
    )
}

TOPIC_PROMPTS = {
    "shapes_sizes": "Grundgeometrie: Identifizierung von Formen (Kreis, Quadrat, Dreieck) und Vergleich von Größen (groß, mittel, klein).",
    "human_body": "Körperteile und die fünf Sinne. Grundlegendes Erkennen einfacher Körperfunktionen.",
    "sound": "Physik des Schalls: Vibrationen, Echo, Arten von Tönen (Bass/Höhen) und Stille.",
    "water_changes": "Wasserkreislauf und Aggregatzustände (fest, flüssig, gasförmig) als Einführung.",
    "feelings": "Emotionale Intelligenz: Erkennen und Benennen von Basisemotionen (Freude, Traurigkeit, Wut, Angst) und einfache Strategien zu deren Bewältigung.",
    "animals": "Grundbiologie: Tierarten, Lebensräume (Wald, Meer, Bauernhof) und grundlegende Pflege.",
    "superheroes": "Werte und Bürgersinn: Anderen helfen, Empathie und wie kleine tägliche Taten uns zu Helden machen.",
    "technology": "Technologie und Logik: Wie einfache Maschinen funktionieren, grundlegende Roboter und Internet der Dinge in vereinfachter Form.",
    "space": "Grundastronomie: Planeten des Sonnensystems, der Mond, die Sterne und die Schwerkraft.",
    "cultures": "Kulturelle Vielfalt: Bräuche, Kleidung, Essen und Spiele aus verschiedenen Teilen der Welt.",
    "mysteries": "Kritisches Denken und Deduktion: Nutzung von Hinweisen, Beobachtung und Logik zur Lösung kleiner Rätsel."
}

MISSION_PROMPTS = {
    "land_of_shapes": (
        "Der Protagonist reist ins 'Land der Formen', ein Ort, an dem alles aus geometrischen Figuren besteht. "
        "Der Konflikt ist, dass die Brücke der Formen kaputt ist und bestimmte Teile fehlen. "
        "Der Protagonist muss Kreise für Räder, Quadrate für Häuser und Dreiecke für die Brücke finden."
    ),
    "big_or_small": (
        "Der Protagonist findet eine magische Lupe, die Dinge groß oder klein macht. "
        "Er muss sie benutzen, um seinen Tierfreunden zu helfen: einen riesigen Stein, der den Weg einer Ameise blockiert, klein machen, "
        "oder einen Samen groß machen, damit er viele Vögel ernährt. Lehrt die Relativität der Größe."
    ),
    "five_senses": (
        "Der Protagonist verliert seine Brille (oder etwas Ähnliches) und muss seine anderen vier Sinne nutzen, um sie zu finden. "
        "Er muss auf Hinweise hören, das Aroma von Keksen riechen, wo er sie gelassen hat, raue Texturen fühlen usw. "
        "Jedes Kapitel konzentriert sich auf einen anderen Sinn."
    ),
    "brave_tooth": (
        "Der Protagonist hat seinen ersten Wackelzahn und hat Angst. "
        "Seine Mission ist es zu untersuchen, was mit Zähnen passiert, und die 'Zahnfee' kennenzulernen. "
        "Die Geschichte normalisiert den natürlichen Prozess des Milchzahnverlusts."
    ),
    "lost_orchestra": (
        "Im Stillen Wald haben die Instrumente ihre Stimme verloren. "
        "Der Protagonist entdeckt, dass jeder Ton aus einer Vibration entsteht. "
        "Er muss die Instrumente 'aufwecken', indem er sie auf verschiedene Weise zum Vibrieren bringt (schlagen, blasen, zupfen), "
        "damit das Orchester wieder spielen kann."
    ),
    "mysterious_echo": (
        "Der Protagonist erkundet eine Höhle, in der das Echo nicht wiederholt, sondern antwortet. "
        "Er entdeckt, dass Schall in unsichtbaren Wellen reist und von Wänden abprallt. "
        "Die Mission ist es, das Echo zu nutzen, um den Weg aus einem dunklen Labyrinth zu finden."
    ),
    "traveling_drop": (
        "Der Protagonist schrumpft auf mikroskopische Größe und reitet auf einem Wassertropfen namens 'Flu'. "
        "Sie reisen gemeinsam vom Meer (Verdunstung), bilden eine Wolke (Kondensation) und fallen als Regen (Niederschlag) auf einen verschneiten Berg. "
        "Es ist eine Abenteuerreise durch den Wasserkreislauf."
    ),
    "melting_ice": (
        "Das Eisreich schmilzt, weil die magische Heizung angelassen wurde. "
        "Der Protagonist muss verstehen, wie Hitze Festes in Flüssiges verwandelt. "
        "Er muss die Umgebung abkühlen, damit das Wasser wieder zu festem Eis wird, und das Schloss retten."
    ),
    "monster_colors": (
        "Das Emotionsmonster hat ein Chaos angerichtet und alle seine Farben gemischt. "
        "Der Protagonist muss ihm helfen, jede Emotion (Rot/Wut, Blau/Traurigkeit, Gelb/Freude) zu trennen "
        "und in die entsprechenden Gläser zu füllen, indem er sich daran erinnert, welche Dinge ihn so fühlen lassen."
    ),
    "grumpy_cloud": (
        "Eine kleine mürrische graue Wolke folgt dem Protagonisten überallhin und fängt an, auf ihn zu regnen. "
        "Der Protagonist lernt, dass es okay ist, wütend zu sein, aber damit die Sonne wieder herauskommt, "
        "muss er tief durchatmen und darüber sprechen, was ihn stört."
    ),
    "lost_penguin": (
        "Ein kleiner Pinguin ist in der Wüste aufgetaucht und ihm ist sehr heiß. "
        "Der Protagonist muss untersuchen, wo er lebt (Südpol/Eis) und ihn zurück nach Hause führen, "
        "wobei er unterwegs andere Tiere und ihre Lebensräume kennenlernt."
    ),
    "vet_day": (
        "Der Protagonist wird für einen Tag Assistent eines Tierarztes. "
        "Er muss herausfinden, was verschiedene Tiere fressen und wie man sie pflegt: einen schmutzigen Hund baden, "
        "einem Hasen Karotten geben und die Pfote eines Kätzchens verbinden."
    ),
    "everyday_hero": (
        "Der Protagonist erhält einen Umhang, kann aber weder fliegen noch hat er Superkräfte. "
        "Er entdeckt, dass seine Superkräfte darin bestehen: seine Spielzeuge zu teilen, einen traurigen Freund zu trösten und beim Aufräumen zu helfen. "
        "Er rettet den Tag im Park durch Freundlichkeit."
    ),
    "invisible_shield": (
        "Der Protagonist lernt, ein 'Schild aus netten Worten' zu erschaffen, um sich vor Spott zu schützen. "
        "Er lehrt andere Kinder, ihre eigenen Schilde zu benutzen und andere mit Mut zu verteidigen, "
        "wodurch die Schule zu einem sicheren Ort wird."
    ),
    "internet_travel": (
        "Der Protagonist 'digitalisiert' sich, um in ein Tablet zu gelangen und eine wichtige Nachricht zu überbringen, die steckengeblieben ist. "
        "Er reist mit Lichtgeschwindigkeit durch Glasfaserkabel und lernt, wie Router und Server funktionieren."
    ),
    "robot_friend": (
        "Der Protagonist baut einen Roboterfreund, vergisst aber, Anweisungen für ihn zu programmieren. "
        "Der Roboter macht alles rückwärts (wäscht Geschirr mit Dreck, fegt mit Wasser). "
        "Der Protagonist muss lernen, logische und sequentielle Befehle (Algorithmen) zu geben, um ihn zu reparieren."
    ),
    "gravity_boots": (
        "Der Protagonist gewinnt eine Reise zur Raumstation, verliert aber seine Schwerkraftstiefel. "
        "Er fängt an, unkontrolliert zu schweben, und muss lernen, wie Schwerelosigkeit funktioniert, um sich zu bewegen, "
        "zu essen und zu schlafen, bevor er zur Erde zurückkehrt."
    ),
    "planet_tour": (
        "Die Sonne organisiert eine Party und hat alle Planeten eingeladen, aber Pluto fühlt sich ausgeschlossen. "
        "Der Protagonist reist in einer Rakete, um die Einladungen zu überbringen, und lernt dabei die einzigartigen "
        "Eigenschaften jedes Planeten kennen (Gasriese, Saturnringe usw.)."
    ),
    "magic_passport": (
        "Jedes Mal, wenn der Protagonist seinen magischen Pass abstempelt, reist er in ein anderes Land, um ein Fest zu feiern. "
        "Er feiert das chinesische Neujahrsfest (Drachen), den Tag der Toten in Mexiko und Diwali in Indien "
        "und lernt dabei, dass wir zwar unterschiedlich sind, aber alle gerne feiern."
    ),
    "food_explorer": (
        "Der Protagonist muss das 'Buch der Aromen der Welt' vervollständigen. "
        "Er reist und probiert Sushi in Japan, Pizza in Italien und Tacos in Mexiko. "
        "Er lernt lokale Zutaten und die Bedeutung des gemeinsamen Essens in verschiedenen Kulturen kennen."
    ),
    "museum_thief": (
        "Das wertvollste Juwel des Museums ist verschwunden, aber es gibt keine Fußabdrücke auf dem Boden. "
        "Der Protagonist nutzt Beobachtungs- und Deduktionstechniken (Lupe, Fingerabdruckpulver), um zu entdecken, "
        "dass der Dieb mit einer Drohne durch das Oberlicht eingedrungen ist."
    ),
    "secret_code": (
        "Der Protagonist findet eine Schatzkarte, die in einem seltsamen Code geschrieben ist. "
        "Er muss Logik benutzen, um Muster zu entziffern (Buchstaben für Zahlen, Spiegel) und den "
        "verborgenen Schatz zu finden, der sich als eine alte Zeitkapsel herausstellt."
    )
}

STORY_SYSTEM_PROMPTS = {
    "system": "Erstelle kreative Fantasy-Geschichten für Kinder mit genau {num_chapters} Kapiteln.",
    "guidelines": (
        "WICHTIGE RICHTLINIEN:\n"
        "- Jedes Kapitel muss ungefähr {words_per_chapter} Wörter haben\n"
        "- Der Inhalt muss familienfreundlich und für Kinder angemessen sein\n"
        "- Verwende bunte, fantasievolle Beschreibungen\n"
        "- Füge positive Botschaften und freundliche Charaktere ein\n"
        "- Gib ein strukturiertes JSON mit 'title' und einem 'chapters'-Array zurück\n"
        "- Jedes Kapitel muss die Felder 'title' und 'content' haben"
    ),
    "image_system": (
        "Erstelle einen prägnanten Image-Prompt, der für Kinderbücher geeignet ist. "
        "Das Ergebnis MUSS eine Illustration beschreiben, die zum angeforderten visuellen Stil passt. "
        "Konzentriere dich darauf, die Szene, die Charaktere und die Emotionen klar für ein junges Publikum zu beschreiben. "
        "VERMEIDE jegliche gruseligen, gewalttätigen, dunklen oder realistischen/fotorealistischen Darstellungen. "
        "Erwähne keine Kameras, Objektive oder fotografischen Begriffe. "
        "Gib NUR den Prompt-Text zurück."
    ),
    "character_extraction": (
        "Du bist ein visueller Charakterdesigner für Kinderbuch-Illustrationen.\n"
        "Lies die komplette Geschichte unten und extrahiere JEDEN benannten Charakter.\n"
        "Für jeden Charakter liefere eine konsistente visuelle Beschreibung, der ein Illustrator "
        "in allen Kapiteln folgen muss.\n\n"
        "Für jeden Charakter verwende EXAKT dieses Format:\n"
        "- [Name]: [Spezies/Typ], [Alterserscheinung], [Haarfarbe und -stil], "
        "[Augenfarbe], [Hautton oder Fellfarbe], [Kleidung/Outfit], [unterscheidende Merkmale], [Körpertyp/Größe]\n\n"
        "Regeln:\n"
        "- Wenn die Geschichte ein Merkmal nicht explizit beschreibt, erfinde eines, das zum Charakter und Ton der Geschichte passt.\n"
        "- Halte die Beschreibungen prägnant, aber spezifisch genug für visuelle Konsistenz.\n"
        "- Schließe ALLE Charaktere ein, auch Nebencharaktere.\n"
        "- Füge KEINEN anderen Text ein, nur die Charakterliste.\n"
        "- Schreibe die Beschreibungen auf Englisch, unabhängig von der Sprache der Geschichte."
    )
}

GUIDED_STORY_FORMAT = {
    "system": "Du bist ein erfahrener Kinderbuchautor. Schreibe eine Bildungsgeschichte für Kinder im Alter von {age_group} Jahren.",
    "data_labels": {
        "protagonist": "Protagonist",
        "topic": "Wissenschaftliches Thema",
        "mission": "Handlung/Mission"
    },
    "structure": (
        "OBLIGATORISCHE STRUKTUR:\n"
        "1. Titel: Kreativ und bezogen auf die Mission.\n"
        "2. Kapitel: Unterteile die Geschichte in {num_chapters} kurze Kapitel.\n"
        "3. Inhalt: Der Ton sollte lustig, sicher und leicht zu lesen sein. "
        "Stelle sicher, dass das wissenschaftliche Konzept natürlich in die Erzählung eingeflochten wird.\n"
        "Gib NUR das JSON im festgelegten Format zurück."
    )
}
