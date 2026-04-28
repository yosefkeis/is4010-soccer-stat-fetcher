import os
import requests

import pytest

from main import API_URL_STANDINGS, fetch_pl_standings, load_api_token, print_standings, validate_top


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
        assert url == API_URL_STANDINGS
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


def test_fetch_pl_standings_network_error(monkeypatch):
    def fake_get(url, headers, timeout):
        raise requests.RequestException("timeout")

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ConnectionError, match="Failed to connect"):
        fetch_pl_standings("test-token")


def test_validate_top_invalid():
    with pytest.raises(ValueError, match="--top must be a positive integer"):
        validate_top(0)


def test_validate_top_valid():
    assert validate_top(3) == 3


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


def test_print_standings_no_data(capsys):
    print_standings({}, top=3)
    captured = capsys.readouterr()
    assert "No standings data was returned by the API." in captured.out


def test_print_standings_invalid_table(capsys):
    print_standings({"standings": [{}]}, top=3)
    captured = capsys.readouterr()
    assert "The standings format is not what was expected." in captured.out
