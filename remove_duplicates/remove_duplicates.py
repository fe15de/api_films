from rapidfuzz import fuzz
import unicodedata
import re

def normalize(text):
    text = text.lower()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def group_similar_films(movies, cutoff=90):
    grouped = {}

    for title, slugs in movies.items():
        if isinstance(slugs, str):
            slugs = [slugs]

        title_norm = normalize(title)
        added = False

        for rep in list(grouped.keys()):
            rep_norm = normalize(rep)
            score = fuzz.token_set_ratio(title_norm, rep_norm)

            if score >= cutoff:
                grouped[rep].extend(slugs)
                added = True
                break

        if not added:
            grouped[title] = list(slugs)  

    return grouped


""" {   'Camina o Muere': ['Camina-o-Muere'], 
    'El Gran Viaje De Tu Vida': ['A-Big-Bold-Beautiful-Journey', 'El-Gran-viaje-De-Tu-Vida'], 
    'El Conjuro 4: Ultimos Ritos': ['The-Conjuring-Last-Rites', 'El-Conjuro-4'], 
    'Un Poeta': ['Un-Poeta'], 
    'Demon Slayer: Kimetsu no Yaiba - Castillo infinito': ['Demon-Slayer-Kimetsu-no-Yaiba-The-Movie-Infinity-Castle', 'Demon-Slayer-Castillo-Inf'], 
    'Una Velada con Dua Lipa': ['An-Evening-with-Dua-Lipa'], 
    'Hamilton': ['Hamilton'], 'Nadie Sabe Quien Soy Yo': ['Nadie-Sabe-Quién-Soy-Yo', 'Nadie-sabe-quien-soy-yo'], 
    'Mascotas al Rescate': ['Pets-on-a-Train'], 
    'BTS 2016 Live The Most Beautiful Moment in Life On Stage: Epilogue Remastered': ['BTS-2016-Live-The-Most-Beautiful-Moment-in-Life-On-Stage-Epilogue-Remastered', 'BTS-Epilogue-Remastered'],
    'BTS 2017 Live Trilogy EPISODE III THE WINGS TOUR THE FINAL Remastered': ['BTS-2017-Live-Trilogy-EPISODE-III-THE-WINGS-TOUR-THE-FINAL-Remastered'], 
    'BTS 2019 WORLD TOUR ‘LOVE YOURSELF: SPEAK YOURSELF’ LONDON Remastered': ['BTS-2019-WORLD-TOUR-LOVE-YOURSELF-SPEAK-YOURSELF-LONDON-Remastered', 'BTS-Love-Yourself-London'], 
    'BTS 2021 MUSTER SOWOOZOO Remastered': ['BTS-2021-MUSTER-SOWOOZOO-Remastered', 'BTS-Muster-Sowoozoo'], 
    'Raqa: Guerra Secreta': ['Raqa', 'Raqa'], 
    'La Infiltrada': ['La-Infiltrada'], 'Otro Viernes de Locos': ['Freakier-Friday'], 
    'Batman Azteca: Choque De Imperios': ['Aztec-Batman-Clash-Of-Empires', 'Batman-Azteca'], 
    '200% Lobo': ['200%-Wolf', '200-%-lobo'], 
    'Amores Materialistas': ['Materialists'], 
    'Los Roses': ['The-Roses'], 
    'Dracula': ['Dracula-A-Love-Tale'], 
    'F1 La Pelicula': ['F1'], 
    'Mistura': ['Mistura'], 
    'Depeche Mode: M': ['Depeche-Mode-M'], 
    'Toy Story Reestreno': ['Toy-Story-Reestreno'], 
    'Paranorman RE': ['Paranorman-RE'], 
    'BTS: The Wing Tour': ['BTS-The-Wing-Tour'], 
    'David Gilmour Live': ['David-Gilmour-Live'], 
    'Diario de un pasion': ['Diario-de-un-pasion'], 
    'Antes del Atardecer': ['Antes-del-Atardecer'], 
    'Antes del amanecer': ['Antes-del-amanecer'], 
    'Loco y estupido amor': ['Loco-y-estupido-amor'], 
    'Yo antes de ti': ['Yo-antes-de-ti'], 
    'La Novicia Rebelde': ['La-Novicia-Rebelde']
} """