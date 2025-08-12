#!/usr/bin/env python3
"""Tests unitaires pour client.GithubOrgClient (exos 4 à 7)."""

import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """Vérifie _public_repos_url à partir d'un payload mocké."""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=payload
        ) as mock_org:
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])
            mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """Vérifie public_repos avec mocks de l'URL et de get_json."""
        repos_payload = [
            {"name": "episodes.dart"},
            {"name": "cpp-netlib"},
        ]
        mock_get_json.return_value = repos_payload

        url = "http://example.com/orgs/google/repos"
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value=url
        ) as mock_url:
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(),
                ["episodes.dart", "cpp-netlib"]
            )
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: dict,
        license_key: str,
        expected: bool
    ) -> None:
        """Vérifie has_license avec plusieurs valeurs paramétrées."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


if __name__ == "__main__":
    unittest.main()
