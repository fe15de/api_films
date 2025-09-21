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

def group_similar_films(movies, cutoff=80):
    grouped = {}

    for title, slugs in movies.items():
        # asegúrate que siempre sea lista
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
            grouped[title] = list(slugs)  # convierto en lista

    return grouped