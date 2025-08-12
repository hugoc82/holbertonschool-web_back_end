#!/usr/bin/env python3
"""Tests unitaires pour utils.access_nested_map.

Ce module vérifie que access_nested_map récupère correctement
les valeurs dans des dictionnaires imbriqués à partir
d'une séquence de clés.
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


if __name__ == "__main__":
    unittest.main()
