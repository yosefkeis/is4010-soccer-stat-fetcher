import os

import pytest

from main import API_URL, fetch_pl_standings, load_api_token, print_standings


class DummyResponse:
    def __init__(self, status_code, json_data=None, reason="OK"):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.reason = reason

    def json(self):
        return self._json_data


def test_load_api_token_missing(monkeypatch):
    monkeypatch.delenv("FOOTBALL_DATA_API_TOKEN", raising=False)

    with pytest.raises(ValueError, match="API token not found"):
        load_api_token()


def test_load_api_token_present(monkeypatch):
    monkeypatch.setenv("FOOTBALL_DATA_API_TOKEN", "test-token")
    assert load_api_token() == "test-token"


def test_fetch_pl_standings_success(monkeypatch):
    dummy_data = {"standings": [{"table": [{"position": 1, "team": {"name": "Team A"}, "playedGames": 1, "won": 1, "draw": 0, "lost": 0, "points": 3}]}]}

    def fake_get(url, headers, timeout):
        assert url == API_URL
        assert headers == {"X-Auth-Token": "test-token"}
        assert timeout == 10
        return DummyResponse(200, dummy_data)

    monkeypatch.setattr("requests.get", fake_get)
    assert fetch_pl_standings("test-token") == dummy_data


def test_fetch_pl_standings_unauthorized(monkeypatch):
    def fake_get(url, headers, timeout):
        return DummyResponse(401, reason="Unauthorized")

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(PermissionError, match="Invalid API token"):
        fetch_pl_standings("bad-token")


def test_print_standings_outputs_expected_lines(capsys):
    data = {
        "standings": [
            {
                "table": [
                    {
                        "position": 1,
                        "team": {"name": "Team A"},
                        "playedGames": 1,
                        "won": 1,
                        "draw": 0,
                        "lost": 0,
                        "points": 3,
                    }
                ]
            }
        ]
    }

    print_standings(data, top=1)
    captured = capsys.readouterr()
    assert "Premier League Standings" in captured.out
    assert "Team A" in captured.out
