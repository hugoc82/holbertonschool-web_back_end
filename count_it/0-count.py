#!/usr/bin/env python3
"""Count keywords in titles of 'hot' posts from a subreddit (recursively).

Usage (example driver given by the checker):
    from 0-count import count_words
    count_words("programming", ["python", "java", "javascript"])

Exigences clés implémentées :
- Appels à l'API Reddit en pagination via récursion (paramètre `after`).
- Pas de suivi des redirections (invalid subreddits → aucun affichage).
- Comptage insensible à la casse ; les doublons dans `word_list`
  s’additionnent (poids/multiplicité).
- Les mots sont délimités par des espaces : "java." ne compte pas pour "java",
  et "javascript" ne compte pas pour "java" (et inversement).
- Affichage trié par nombre décroissant puis alphabétique croissant.
"""

from typing import Dict, Iterable, Optional
import requests


def count_words(subreddit: str,
                word_list: Iterable[str],
                after: Optional[str] = None,
                counts: Optional[Dict[str, int]] = None,
                multiplicity: Optional[Dict[str, int]] = None) -> None:
    """Query Reddit API and print sorted counts of `word_list` in hot titles.

    Parameters
    ----------
    subreddit : str
        Nom du subreddit à interroger.
    word_list : Iterable[str]
        Liste de mots-clés à compter (insensible à la casse). Les doublons
        sont autorisés et augmentent la multiplicité du mot.
    after : Optional[str]
        Curseur de pagination Reddit (utilisé récursivement).
    counts : Optional[Dict[str, int]]
        Dictionnaire cumulatif des occurrences par mot (état récursif).
    multiplicity : Optional[Dict[str, int]]
        Poids/multiplicité par mot, basé sur les doublons dans `word_list`.
    """
    # Initialisation (premier appel)
    if counts is None:
        counts = {}
    if multiplicity is None:
        multiplicity = {}
        for w in word_list:
            key = str(w).lower()
            multiplicity[key] = multiplicity.get(key, 0) + 1
            # Pré-initialiser tous les mots suivis en lowercase
            if key not in counts:
                counts[key] = 0

    # Préparer la requête Reddit
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": 100}
    if after:
        params["after"] = after

    headers = {
        "User-Agent": "holberton_count_it:1.0 (by u/learning-bot)"
    }

    try:
        resp = requests.get(
            url, headers=headers, params=params, timeout=10,
            allow_redirects=False
        )
    except requests.RequestException:
        # En cas d'erreur réseau : ne rien afficher
        return

    if resp.status_code != 200:
        # Subreddit invalide (ou redirection bloquée) -> rien à afficher
        return

    data = resp.json().get("data", {})
    children = data.get("children", [])

    # Comptage des occurrences dans la page courante
    # Titre : découpe par espaces, comparaison stricte (token == mot)
    for post in children:
        title = post.get("data", {}).get("title", "")
        # Split sur espaces ; on ne nettoie pas la ponctuation pour respecter
        # la contrainte "java." ne compte pas pour "java".
        for token in title.lower().split():
            if token in counts:
                counts[token] += 1

    # Pagination récursive
    next_after = data.get("after")
    if next_after:
        count_words(subreddit, word_list, next_after, counts, multiplicity)
        return

    # Fin de pagination : calcul final et affichage
    # Appliquer la multiplicité des mots (doublons de word_list)
    final_counts: Dict[str, int] = {}
    for word, cnt in counts.items():
        mult = multiplicity.get(word, 0)
        total = cnt * mult
        if total > 0:
            final_counts[word] = total

    if not final_counts:
        # Rien à afficher (aucune occurrence ou subreddit invalide)
        return

    # Tri : d'abord par nombre décroissant, puis par ordre alphabétique
    ordered = sorted(final_counts.items(),
                     key=lambda kv: (-kv[1], kv[0]))

    for word, total in ordered:
        print(f"{word}: {total}")
