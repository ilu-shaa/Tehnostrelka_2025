# search_service/synonyms.py

"""
Здесь храним словарь синонимов (SYNONYMS), 
а также функцию expand_query, которая 
по входной строке возвращает список слов (с учётом синонимов).
"""

SYNONYMS = {
    # Примеры — заменяйте на любые нужные
    "инопланетяне": ["пришельцы", "aliens", "внеземные"],
    "роботы": ["андроиды", "robots"],
    "love": ["любовь", "романтика", "relationship"],
    "superhero": ["super-hero", "супергерой"],
    "ghost": ["призрак", "дух", "привидение"]
    # и т.д.
}

def expand_query(query: str) -> list:
    """
    Принимает строку запроса, разбивает по пробелам,
    для каждого слова пытается найти синонимы в словаре 
    и возвращает полный список (слово + синонимы).
    """
    if not query:
        return []

    words = query.lower().split()
    expanded = []

    for w in words:
        expanded.append(w)
        if w in SYNONYMS:
            expanded.extend(SYNONYMS[w])
    
    # Уберём дубликаты
    expanded = list(set(expanded))
    return expanded