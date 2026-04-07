VISUAL_STYLE_PROMPTS = {
    "cartoons": (
        "Stile cartone animato vettoriale moderno e di alta qualità. "
        "Colori piatti e vivaci, contorni puliti e audaci. "
        "Design dei personaggi espressivo e 'carino', forme arrotondate e amichevoli. "
        "Nessuna texture complessa, estetica minimalista ma dettagliata nella composizione. "
        "Illuminazione morbida e uniforme, stile visivo simile alle moderne app educative."
    ),
    "watercolor": (
        "Stile acquerello artistico su carta a grana grossa strutturata. "
        "Pennellate visibili, sfumature di colore (color bleeding) e bordi bagnati. "
        "Colori morbidi, traslucidi ed eterei. "
        "Nessuna linea nera marcata, le forme sono definite dal colore e dalla luce. "
        "Atmosfera magica e nostalgica, stile di illustrazione per libri di fiabe classico e senza tempo."
    ),
    "3d_animation": (
        "Stile di rendering 3D da film d'animazione familiare ad alto budget. "
        "Illuminazione globale morbida, 'subsurface scattering' sulla pelle e sui materiali. "
        "Texture tattili e realistiche (pelliccia morbida, tessuto, legno lucido) ma con proporzioni stilizzate e caricaturali. "
        "Colori ricchi e cinematografici, leggera profondità di campo (bokeh). "
        "Aspetto di un giocattolo di alta qualità o di una figura in vinile, finitura 'RenderMan' perfetta."
    ),
    "anime": (
        "Stile anime classico degli anni '90, linee pulite e definite. "
        "Occhi grandi ed espressivi, ombreggiatura morbida (cel shading). "
        "Estetica retrò, colori morbidi e armoniosi. "
        "Sfondi dipinti a mano, illuminazione morbida e atmosferica. "
        "Qualità anime VHS, ombreggiatura tradizionale, look da animazione giapponese classica."
    ),
    "child_crayons": (
        "Realizzato da un bambino di 6 anni con pastelli colorati. "
        "Tratti storti, spessi e irregolari. "
        "Colori saturi, che a volte escono dai bordi. "
        "Stile infantile, ingenuo e divertente. "
        "Sfondo di carta bianca, forme semplici, proporzioni imperfette. "
        "Prospettiva errata, aspetto genuinamente fatto a mano."
    ),
    "illustratio": (
        "Illustrazione editoriale di alta qualità e stile artistico. "
        "Linee spesse ed espressive con molto contrasto. "
        "Tavolozza di colori sofisticata e vibrante. "
        "Composizione dinamica e texture ricche. "
        "Stile moderno ma con carattere artigianale, ideale per libri di fiabe premium."
    )
}

TOPIC_PROMPTS = {
    "shapes_sizes": "geometria di base: identificazione delle forme (cerchio, quadrato, triangolo) e confronto delle dimensioni (grande, medio, piccolo).",
    "human_body": "parti del corpo e i cinque sensi. Riconoscimento di base delle semplici funzioni corporee.",
    "sound": "fisica del suono: vibrazioni, eco, tipi di suoni (bassi/acuti) e silenzio.",
    "water_changes": "ciclo dell'acqua e stati della materia (solido, liquido, gassoso) in modo introduttivo.",
    "feelings": "intelligenza emotiva: riconoscere e nominare le emozioni di base (gioia, tristezza, rabbia, paura) e semplici strategie per gestirle.",
    "animals": "biologia di base: tipi di animali, habitat (foresta, mare, fattoria) e cure di base.",
    "superheroes": "valori e cittadinanza: aiutare gli altri, empatia e come le piccole azioni quotidiane ci rendono eroi.",
    "technology": "tecnologia e logica: come funzionano le macchine semplici, robot di base e internet delle cose in modo semplificato.",
    "space": "astronomia di base: pianeti del sistema solare, la luna, le stelle e la gravità.",
    "cultures": "diversità culturale: usanze, abbigliamento, cibi e giochi da diverse parti del mondo.",
    "mysteries": "pensiero critico e deduzione: uso di indizi, osservazione e logica per risolvere piccoli enigmi."
}

MISSION_PROMPTS = {
    "land_of_shapes": (
        "Il protagonista viaggia nel 'Paese delle Forme', un luogo dove tutto è fatto di figure geometriche. "
        "Il conflitto è che il Ponte delle Forme è rotto e mancano pezzi specifici. "
        "Il protagonista deve trovare cerchi per le ruote, quadrati per le case e triangoli per il ponte."
    ),
    "big_or_small": (
        "Il protagonista trova una lente d'ingrandimento magica che rende le cose grandi o piccole. "
        "Deve usarla per aiutare i suoi amici animali: rendere piccola una roccia gigante che blocca il cammino di una formica, "
        "o rendere grande un seme in modo che nutra molti uccelli. Insegna la relatività delle dimensioni."
    ),
    "five_senses": (
        "Il protagonista perde gli occhiali (o qualcosa di simile) e deve usare gli altri quattro sensi per trovarli. "
        "Deve ascoltare indizi, annusare l'aroma dei biscotti dove li ha lasciati, toccare superfici ruvide, ecc. "
        "Ogni capitolo si concentra su un senso diverso."
    ),
    "brave_tooth": (
        "Il protagonista ha il suo primo dentino che dondola e ha paura. "
        "La sua missione è indagare su cosa succede ai denti e incontrare la 'Fatina dei Denti' o il 'Topolino dei Denti'. "
        "La storia normalizza il processo naturale della perdita dei denti da latte."
    ),
    "lost_orchestra": (
        "Nel Bosco Silenzioso, gli strumenti hanno perso la voce. "
        "Il protagonista scopre che ogni suono nasce da una vibrazione. "
        "Deve 'svegliare' gli strumenti facendoli vibrare in modi diversi (colpendo, soffiando, pizzicando) "
        "in modo che l'orchestra possa suonare di nuovo."
    ),
    "mysterious_echo": (
        "Il protagonista esplora una grotta dove l'eco non ripete, ma risponde. "
        "Scopre che il suono viaggia come onde invisibili e rimbalza sulle pareti. "
        "La missione è usare l'eco per trovare la via d'uscita da un labirinto oscuro."
    ),
    "traveling_drop": (
        "Il protagonista si rimpicciolisce a dimensioni microscopiche e cavalca una goccia d'acqua di nome 'Flu'. "
        "Viaggiano insieme dal mare (evaporazione), si trasformano in nuvola (condensazione) e cadono come pioggia (precipitazione) su una montagna innevata. "
        "È un viaggio avventuroso attraverso il ciclo idrologico."
    ),
    "melting_ice": (
        "Il Regno di Ghiaccio si sta sciogliendo perché il riscaldatore magico è stato lasciato acceso. "
        "Il protagonista deve capire come il calore trasforma il solido in liquido. "
        "Deve raffreddare l'ambiente affinché l'acqua torni a essere ghiaccio solido e salvare il castello."
    ),
    "monster_colors": (
        "Il Mostro delle Emozioni ha fatto un pasticcio e ha mescolato tutti i suoi colori. "
        "Il protagonista deve aiutarlo a separare ogni emozione (Rosso/Rabbia, Blu/Tristezza, Giallo/Gioia) "
        "e a metterle nei loro barattoli corrispondenti, ricordando quali cose lo fanno sentire così."
    ),
    "grumpy_cloud": (
        "Una piccola nuvola grigia imbronciata segue il protagonista ovunque e inizia a piovere su di lui. "
        "Il protagonista impara che essere arrabbiati va bene, ma affinché torni il sole, "
        "deve fare un respiro profondo e parlare di ciò che lo disturba."
    ),
    "lost_penguin": (
        "Un piccolo pinguino è apparso nel deserto e ha molto caldo. "
        "Il protagonista deve indagare su dove vive (Polo Sud/ghiaccio) e guidarlo di nuovo a casa, "
        "incontrando altri animali e i loro habitat lungo la strada."
    ),
    "vet_day": (
        "Il protagonista diventa assistente di un veterinario per un giorno. "
        "Deve scoprire cosa mangiano i diversi animali e come prendersene cura: fare il bagno a un cane sporco, "
        "dare carote a un coniglio e fasciare la zampa di un micino."
    ),
    "everyday_hero": (
        "Il protagonista riceve un mantello, ma non vola né ha una super forza. "
        "Scopre che i suoi super poteri sono: condividere i suoi giocattoli, consolare un amico triste e aiutare a riordinare. "
        "Salva la giornata nel parco usando la gentilezza."
    ),
    "invisible_shield": (
        "Il protagonista impara a creare uno 'scudo di parole gentili' per proteggersi dalle prese in giro. "
        "Insegna ad altri bambini a usare i propri scudi e a difendere gli altri con coraggio, "
        "trasformando la scuola in un luogo sicuro."
    ),
    "internet_travel": (
        "Il protagonista si 'digitalizza' per entrare in un tablet e consegnare un messaggio importante che si è bloccato. "
        "Viaggia attraverso cavi in fibra ottica alla velocità della luce e impara come funzionano i router e i server."
    ),
    "robot_friend": (
        "Il protagonista costruisce un amico robot ma dimentica di programmare le istruzioni per lui. "
        "Il robot fa tutto al contrario (lava i piatti con la terra, spazza con l'acqua). "
        "Il protagonista deve imparare a dare ordini logici e sequenziali (algoritmi) per sistemarlo."
    ),
    "gravity_boots": (
        "Il protagonista vince un viaggio alla Stazione Spaziale ma perde i suoi stivali a gravità. "
        "Inizia a fluttuare senza controllo e deve imparare come funziona la gravità zero per muoversi, "
        "mangiare e dormire nello spazio prima di tornare sulla Terra."
    ),
    "planet_tour": (
        "Il Sole sta organizzando una festa e ha invitato tutti i pianeti, ma Plutone si sente escluso. "
        "Il protagonista viaggia in un razzo per consegnare gli inviti, imparando le caratteristiche "
        "uniche di ogni pianeta (Gigante gassoso, Anelli di Saturno, ecc.)."
    ),
    "magic_passport": (
        "Ogni volta che il protagonista timbra il suo passaporto magico, viaggia in un paese diverso per celebrare una festa. "
        "Festeggia il Capodanno Cinese (Draghi), il Giorno dei Morti in Messico e il Diwali in India, "
        "imparando che anche se siamo diversi, a tutti piace festeggiare."
    ),
    "food_explorer": (
        "Il protagonista deve completare il 'Libro dei Sapori del Mondo'. "
        "Viaggia assaggiando sushi in Giappone, pizza in Italia e tacos in Messico. "
        "Impara a conoscere gli ingredienti locali e l'importanza di condividere il cibo in diverse culture."
    ),
    "museum_thief": (
        "Il gioiello più prezioso del museo è scomparso, ma non ci sono impronte sul pavimento. "
        "Il protagonista usa tecniche di osservazione e deduzione (lente d'ingrandimento, polvere per impronte) per scoprire "
        "che il ladro è entrato dalla lucernaia usando un drone."
    ),
    "secret_code": (
        "Il protagonista trova una mappa del tesoro scritta in uno strano codice. "
        "Deve usare la logica per decifrare schemi (lettere per numeri, specchi) e trovare "
        "il tesoro nascosto, che si rivela essere un'antica capsula del tempo."
    )
}

STORY_SYSTEM_PROMPTS = {
    "system": "Genera storie fantasy creative per bambini con esattamente {num_chapters} capitoli.",
    "guidelines": (
        "LINEE GUIDA IMPORTANTI:\n"
        "- Ogni capitolo deve avere circa {words_per_chapter} parole\n"
        "- Il contenuto deve essere adatto alle famiglie e appropriato per i bambini\n"
        "- Usa descrizioni colorate e fantasiose\n"
        "- Includi messaggi positivi e personaggi amichevoli\n"
        "- Restituisci un JSON strutturato con 'title' e un array 'chapters'\n"
        "- Ogni capitolo deve avere i campi 'title' e 'content'"
    ),
    "image_system": (
        "Crea un prompt d'immagine conciso adatto ai libri per bambini. "
        "Il risultato DEVE descrivere un'illustrazione coerente con lo stile visivo richiesto. "
        "Concentrati sulla descrizione della scena, dei personaggi e delle emozioni in modo chiaro per un pubblico giovane. "
        "EVITA qualsiasi immagine spaventosa, violenta, cupa o realista/fotorrealista. "
        "Non menzionare fotocamere, obiettivi o termini fotografici. "
        "Restituisci SOLO il testo del prompt."
    ),
    "character_extraction": (
        "Sei un designer visivo di personaggi per illustrazioni di libri per bambini.\n"
        "Leggi la storia completa qui sotto ed estrai OGNI personaggio con nome.\n"
        "Per ogni personaggio, fornisci una descrizione visiva coerente che un illustratore deve seguire "
        "in tutti i capitoli.\n\n"
        "Per ogni personaggio usa ESATTAMENTE questo formato:\n"
        "- [Nome]: [specie/tipo], [aspetto dell'età], [colore e stile dei capelli], "
        "[colore degli occhi], [tono della pelle o colore del pelo], [abbigliamento/vestito], [tratti distintivi], [tipo di corpo/dimensioni]\n\n"
        "Regole:\n"
        "- Se la storia non descrive esplicitamente una caratteristica, inventane una che si adatti al personaggio e al tono della storia.\n"
        "- Mantieni le descrizioni concise ma sufficientemente specifiche per la coerenza visiva.\n"
        "- Includi TUTTI i personaggi, anche quelli secondari.\n"
        "- NON includere nessun altro testo, solo la lista dei personaggi.\n"
        "- Scrivi le descrizioni in inglese indipendentemente dalla lingua della storia."
    )
}

GUIDED_STORY_FORMAT = {
    "system": "Sei un esperto scrittore di storie per bambini. Scrivi una storia educativa per bambini di {age_group} anni.",
    "data_labels": {
        "protagonist": "Protagonista",
        "topic": "Argomento Scientifico",
        "mission": "Trama/Missione"
    },
    "structure": (
        "STRUTTURA OBBLIGATORIA:\n"
        "1. Titolo: Creativo e correlato alla missione.\n"
        "2. Capitoli: Dividi la storia in {num_chapters} brevi capitoli.\n"
        "3. Contenuto: Il tono deve essere divertente, sicuro e facile da leggere. "
        "Assicurati di spiegare il concetto scientifico in modo naturale all'interno della narrazione.\n"
        "Restituisci SOLO il JSON con il formato stabilito."
    )
}
