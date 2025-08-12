#!/usr/bin/env python3
"""Tests unitaires et d'intégration pour GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests pour la classe GithubOrgClient (exos 4 à 7)."""

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


@parameterized_class((
    "org_payload",
    "repos_payload",
    "expected_repos",
    "apache2_repos",
), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Tests d'intégration pour GithubOrgClient.public_repos (exo 8)."""

    @classmethod
    def setUpClass(cls) -> None:
        """Patch requests.get pour renvoyer les fixtures attendues."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            response = Mock()
            # Requête des infos d'org (ORG_URL) -> org_payload
            if url.startswith("https://api.github.com/orgs/") and \
               not url.endswith("/repos"):
                response.json.return_value = cls.org_payload
            # Requête des repos de l'org -> repos_payload
            elif url == cls.org_payload.get("repos_url"):
                response.json.return_value = cls.repos_payload
            else:
                response.json.return_value = {}
            return response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stoppe le patcher requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Sans filtre de licence, retourne la liste attendue."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Avec filtre 'apache-2.0', retourne la liste attendue."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
