"""Banque de sujets type brevet (inspire des sessions precedentes)."""

MATIERES = [
    ("Francais", "francais"),
    ("Mathematiques", "maths"),
    ("Histoire", "histoire"),
    ("Geographie", "geo"),
    ("EMC", "emc"),
    ("Physique-Chimie", "pc"),
    ("SVT", "svt"),
]

# answer = index de la bonne reponse (0-3)
SUJETS = {
    "francais": [
        {
            "annee": 2023,
            "question": "Quelle figure de style consiste a exagerer une idee ?",
            "choices": ["La metaphore", "L'hyperbole", "L'euphemisme", "La litote"],
            "answer": 1,
            "explication": "L'hyperbole est une figure de style qui consiste a exagérer une idée pour la mettre en valeur. Exemple : 'J'ai faim à mourir.'",
        },
        {
            "annee": 2022,
            "question": "Dans un recit, le point de vue interne signifie que :",
            "choices": [
                "Le narrateur sait tout",
                "On voit par les yeux d'un personnage",
                "Le narrateur est absent",
                "Le recit est au present",
            ],
            "answer": 1,
            "explication": "Le point de vue interne permet au lecteur de voir l'histoire à travers les yeux et les pensées d'un personnage spécifique.",
        },
        {
            "annee": 2024,
            "question": "Quel est le complement d'objet direct dans : « Il lit un livre » ?",
            "choices": ["Il", "lit", "un livre", "dans"],
            "answer": 2,
            "explication": "Le COD (Complément d'Objet Direct) est ce sur quoi porte l'action du verbe. Ici, 'un livre' est ce qui est lu.",
        },
        {
            "annee": 2021,
            "question": "Un alexandrin est un vers de combien de syllabes ?",
            "choices": ["8", "10", "12", "14"],
            "answer": 2,
            "explication": "L'alexandrin est un vers de 12 syllabes, très utilisé dans la poésie classique française.",
        },
        {
            "annee": 2023,
            "question": "La phrase exclamative se termine le plus souvent par :",
            "choices": ["Un point", "Des guillemets", "Un point d'exclamation", "Deux points"],
            "answer": 2,
            "explication": "La phrase exclamative exprime une émotion vive et se termine toujours par un point d'exclamation (!).",
        },
    ],
    "maths": [
        {
            "annee": 2023,
            "question": "Quelle est la valeur de 3/4 + 1/2 ?",
            "choices": ["4/6", "5/4", "1/4", "7/8"],
            "answer": 1,
            "explication": "Il faut mettre au même dénominateur : 3/4 + 2/4 = 5/4 = 1,25.",
        },
        {
            "annee": 2022,
            "question": "Un triangle rectangle a des cotes de 3 cm et 4 cm. L'hypotenuse mesure :",
            "choices": ["5 cm", "6 cm", "7 cm", "12 cm"],
            "answer": 0,
            "explication": "Théorème de Pythagore : h² = 3² + 4² = 9 + 16 = 25, donc h = 5 cm.",
        },
        {
            "annee": 2024,
            "question": "Le volume d'un cube de cote 3 cm est :",
            "choices": ["9 cm3", "18 cm3", "27 cm3", "36 cm3"],
            "answer": 2,
            "explication": "Volume d'un cube = côté³ = 3³ = 3 × 3 × 3 = 27 cm³.",
        },
        {
            "annee": 2021,
            "question": "Si x + 7 = 15, alors x vaut :",
            "choices": ["6", "7", "8", "22"],
            "answer": 2,
            "explication": "On soustrait 7 des deux côtés : x = 15 - 7 = 8.",
        },
        {
            "annee": 2023,
            "question": "Une reduction de 20 % sur 50 € donne un prix de :",
            "choices": ["30 €", "40 €", "45 €", "48 €"],
            "answer": 1,
            "explication": "20% de 50€ = 10€. Prix final = 50€ - 10€ = 40€.",
        },
    ],
    "histoire": [
        {
            "annee": 2023,
            "question": "La Revolution francaise debute en :",
            "choices": ["1789", "1815", "1848", "1914"],
            "answer": 0,
            "explication": "La Révolution française commence en 1789 avec la prise de la Bastille le 14 juillet.",
        },
        {
            "annee": 2022,
            "question": "La Premiere Guerre mondiale se termine en :",
            "choices": ["1914", "1916", "1918", "1939"],
            "answer": 2,
            "explication": "La Première Guerre mondiale s'est terminée le 11 novembre 1918 avec l'armistice.",
        },
        {
            "annee": 2024,
            "question": "La Declaration des droits de l'homme et du citoyen date de :",
            "choices": ["1789", "1792", "1804", "1870"],
            "answer": 0,
            "explication": "La Déclaration des droits de l'homme et du citoyen a été adoptée en 1789 pendant la Révolution française.",
        },
        {
            "annee": 2021,
            "question": "Qui etait le chef de l'Etat francais en 1940 (regime de Vichy) ?",
            "choices": ["De Gaulle", "Petain", "Clemenceau", "Mitterrand"],
            "answer": 1,
            "explication": "Philippe Pétain était le chef de l'État français sous le régime de Vichy pendant l'Occupation.",
        },
        {
            "annee": 2023,
            "question": "La construction europeenne debute apres :",
            "choices": ["La Revolution", "La Premiere Guerre mondiale", "La Seconde Guerre mondiale", "La Guerre froide uniquement"],
            "answer": 2,
            "explication": "La construction européenne débute après la Seconde Guerre mondiale pour éviter de nouveaux conflits.",
        },
    ],
    "geo": [
        {
            "annee": 2023,
            "question": "Quelle est la capitale de l'Allemagne ?",
            "choices": ["Munich", "Hambourg", "Berlin", "Francfort"],
            "answer": 2,
            "explication": "Berlin est la capitale et la plus grande ville de l'Allemagne depuis la réunification en 1990.",
        },
        {
            "annee": 2022,
            "question": "Le fleuve le plus long de France est :",
            "choices": ["La Seine", "Le Rhone", "La Loire", "La Garonne"],
            "answer": 2,
            "explication": "La Loire est le plus long fleuve de France avec plus de 1000 km de longueur.",
        },
        {
            "annee": 2024,
            "question": "Une metropole est :",
            "choices": [
                "Un petit village",
                "Une grande ville polarisant un territoire",
                "Un desert",
                "Une zone montagneuse",
            ],
            "answer": 1,
            "explication": "Une métropole est une grande ville qui exerce une influence économique, politique et culturelle sur son territoire.",
        },
        {
            "annee": 2021,
            "question": "La France est situee principalement en :",
            "choices": ["Asie", "Afrique", "Europe", "Amerique"],
            "answer": 2,
            "explication": "La France est située en Europe occidentale, avec également des territoires d'outre-mer.",
        },
        {
            "annee": 2023,
            "question": "Le rechauffement climatique entraine notamment :",
            "choices": [
                "Baisse du niveau des mers",
                "Fonte des glaces",
                "Disparition des cyclones",
                "Refroidissement global",
            ],
            "answer": 1,
            "explication": "Le réchauffement climatique provoque la fonte des glaciers et des banquises, ce qui augmente le niveau des mers.",
        },
    ],
    "emc": [
        {
            "annee": 2023,
            "question": "La laicite en France signifie que :",
            "choices": [
                "L'Etat impose une religion",
                "L'Etat est neutre en matiere religieuse",
                "Les religions sont interdites",
                "Seule une religion est autorisee",
            ],
            "answer": 1,
            "explication": "La laïcité signifie que l'État est neutre par rapport aux religions : il n'en favorise aucune et n'en interdit aucune.",
        },
        {
            "annee": 2022,
            "question": "A quoi sert le droit de vote ?",
            "choices": [
                "Choisir ses professeurs",
                "Participer a la vie democratique",
                "Eviter les impots",
                "Creer des lois seul",
            ],
            "answer": 1,
            "explication": "Le droit de vote permet aux citoyens de participer à la vie démocratique en élisant leurs représentants.",
        },
        {
            "annee": 2024,
            "question": "La Declaration universelle des droits de l'homme date de :",
            "choices": ["1789", "1948", "1968", "2000"],
            "answer": 1,
            "explication": "La Déclaration universelle des droits de l'homme a été adoptée par l'ONU en 1948 après la Seconde Guerre mondiale.",
        },
        {
            "annee": 2021,
            "question": "Un media libre doit :",
            "choices": [
                "Cacher l'information",
                "Informer avec independance",
                "Ne parler que du sport",
                "Etre controle par l'Etat uniquement",
            ],
            "answer": 1,
            "explication": "Un média libre doit informer avec indépendance, sans être soumis à la pression politique ou économique.",
        },
        {
            "annee": 2023,
            "question": "Le harcelement scolaire est :",
            "choices": [
                "Un jeu normal",
                "Une violence repetee a sanctionner",
                "Autorise en cours",
                "Sans consequence",
            ],
            "answer": 1,
            "explication": "Le harcèlement scolaire est une violence répétée qui doit être sanctionnée et signalée aux adultes.",
        },
    ],
    "pc": [
        {
            "annee": 2023,
            "question": "L'unite de force est le :",
            "choices": ["Joule", "Newton", "Watt", "Pascal"],
            "answer": 1,
            "explication": "Le Newton (N) est l'unité internationale de force. Le Joule est l'unité d'énergie.",
        },
        {
            "annee": 2022,
            "question": "L'eau bout a 100 °C a :",
            "choices": ["Pression normale", "Toute pression", "0 °C", "En altitude uniquement"],
            "answer": 0,
            "explication": "L'eau bout à 100°C à pression atmosphérique normale. En altitude, elle bout à une température plus basse.",
        },
        {
            "annee": 2024,
            "question": "Un atome est forme d'un noyau et de :",
            "choices": ["Protons uniquement", "Electrons", "Neutrons seulement", "Molecules"],
            "answer": 1,
            "explication": "Un atome est composé d'un noyau (protons + neutrons) autour duquel gravitent des électrons.",
        },
        {
            "annee": 2021,
            "question": "La formule chimique de l'eau est :",
            "choices": ["CO2", "H2O", "O2", "NaCl"],
            "answer": 1,
            "explication": "La formule chimique de l'eau est H2O : 2 atomes d'hydrogène pour 1 atome d'oxygène.",
        },
        {
            "annee": 2023,
            "question": "La vitesse se calcule par :",
            "choices": ["distance x temps", "distance / temps", "masse / volume", "force x distance"],
            "answer": 1,
            "explication": "La vitesse (v) = distance (d) / temps (t). Plus on parcourt de distance en peu de temps, plus on va vite.",
        },
    ],
    "svt": [
        {
            "annee": 2023,
            "question": "La photosynthese se deroule principalement dans :",
            "choices": ["Les racines", "Les feuilles", "Les fleurs", "L'ecorce"],
            "answer": 1,
            "explication": "La photosynthèse se déroule dans les feuilles, qui contiennent la chlorophylle nécessaire pour capter la lumière.",
        },
        {
            "annee": 2022,
            "question": "L'ADN est contenu dans :",
            "choices": ["Le noyau des cellules", "L'air", "L'eau pure", "Les roches"],
            "answer": 0,
            "explication": "L'ADN est contenu dans le noyau des cellules eucaryotes. C'est le support de l'information génétique.",
        },
        {
            "annee": 2024,
            "question": "Un ecosysteme comprend des etres vivants et :",
            "choices": ["Rien d'autre", "Leur milieu de vie", "Uniquement l'eau", "Des voitures"],
            "answer": 1,
            "explication": "Un écosystème comprend les êtres vivants et leur milieu de vie (biotope) avec lesquels ils interagissent.",
        },
        {
            "annee": 2021,
            "question": "La reproduction sexuee implique :",
            "choices": [
                "Un seul parent",
                "Deux cellules reproductrices",
                "Aucune cellule",
                "Uniquement des spores",
            ],
            "answer": 1,
            "explication": "La reproduction sexuée nécessite deux cellules reproductrices (spermatozoïde et ovule) qui fusionnent.",
        },
        {
            "annee": 2023,
            "question": "Le systeme digestif sert a :",
            "choices": [
                "Respirer",
                "Transformer les aliments",
                "Pomper le sang",
                "Produire des hormones uniquement",
            ],
            "answer": 1,
            "explication": "Le système digestif transforme les aliments en nutriments utilisables par l'organisme grâce à la digestion.",
        },
    ],
}


def note_matiere(reponses, questions):
    if not questions:
        return 0.0
    bonnes = sum(1 for i, q in enumerate(questions) if reponses[i] == q["answer"])
    return round((bonnes / len(questions)) * 20, 2)
