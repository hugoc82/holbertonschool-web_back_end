#!/usr/bin/env python3
"""Tests unitaires pour client.GithubOrgClient (exo 4)."""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests pour la classe GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Vérifie que .org renvoie la valeur attendue et appelle get_json."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()
