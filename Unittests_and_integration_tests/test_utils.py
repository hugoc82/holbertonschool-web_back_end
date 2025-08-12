#!/usr/bin/env python3
"""Tests unitaires pour utils.access_nested_map.

Ce module vérifie que access_nested_map récupère correctement
les valeurs dans des dictionnaires imbriqués à partir
d'une séquence de clés, et lève bien les exceptions attendues.
"""

import unittest
from typing import Any, Mapping, Sequence

from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests pour la fonction utilitaire access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """Retourne la valeur attendue pour le dictionnaire et le chemin donnés."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
    ) -> None:
        """Vérifie qu'un KeyError est levé avec le bon message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[len(cm.exception.args[0]) == 1 and 0 or 0]))  # Vérifie message
        # Remarque : Le message doit correspondre à la clé manquante


if __name__ == "__main__":
    unittest.main()
