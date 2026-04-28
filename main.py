import argparse
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


API_URL_STANDINGS = "https://api.football-data.org/v4/competitions/PL/standings"
API_URL_MATCHES = "https://api.football-data.org/v4/matches"
API_URL_SCORERS = "https://api.football-data.org/v4/competitions/PL/scorers"


def load_api_token() -> str:
    token = os.getenv("FOOTBALL_DATA_API_TOKEN")
    if not token:
        raise ValueError(
            "API token not found. Create a .env file with FOOTBALL_DATA_API_TOKEN=your_token"
        )
    return token


def fetch_data(api_token: str, url: str) -> Any:
    headers = {"X-Auth-Token": api_token}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as error:
        raise ConnectionError(f"Failed to connect to Football Data API: {error}") from error

    if response.status_code == 200:
        return response.json()

    if response.status_code == 401:
        raise PermissionError("Invalid API token or unauthorized access.")
    if response.status_code == 404:
        raise FileNotFoundError("The requested endpoint was not found.")

    raise RuntimeError(
        f"Unexpected API response: {response.status_code} {response.reason}"
    )


def fetch_pl_standings(api_token: str) -> Any:
    return fetch_data(api_token, API_URL_STANDINGS)


def fetch_matches(api_token: str) -> Any:
    return fetch_data(api_token, API_URL_MATCHES)


def fetch_scorers(api_token: str) -> Any:
    return fetch_data(api_token, API_URL_SCORERS)


def format_standing_row(row: Any) -> str:
    team_name = row.get("team", {}).get("name", "Unknown")
    return (
        f"{row.get('position', 0):>8} | "
        f"{team_name[:25]:<25} | "
        f"{row.get('playedGames', 0):>6} | "
        f"{row.get('won', 0):>3} | "
        f"{row.get('draw', 0):>5} | "
        f"{row.get('lost', 0):>4} | "
        f"{row.get('points', 0):>6}"
    )


def validate_top(top: int) -> int:
    if top <= 0:
        raise ValueError("--top must be a positive integer")
    return top


def print_standings(data: Any, top: int) -> None:
    standings = data.get("standings")
    if not standings:
        print("No standings data was returned by the API.")
        return

    table = standings[0].get("table", [])
    if not table:
        print("The standings format is not what was expected.")
        return

    print("Premier League Standings")
    print("Position | Team | Played | Won | Drawn | Lost | Points")
    print("---------|------|--------|-----|-------|------|-------")
    for row in table[:top]:
        print(format_standing_row(row))


def print_matches(data: Any, limit: int) -> None:
    matches = data.get("matches", [])
    if not matches:
        print("No matches data was returned by the API.")
        return

    print("Recent Premier League Matches")
    print("Date | Home Team | Away Team | Score")
    print("-----|----------|-----------|------")
    for match in matches[:limit]:
        home_team = match.get("homeTeam", {}).get("name", "Unknown")
        away_team = match.get("awayTeam", {}).get("name", "Unknown")
        score = match.get("score", {})
        full_time = score.get("fullTime", {})
        home_score = full_time.get("home", "N/A")
        away_score = full_time.get("away", "N/A")
        score_str = f"{home_score}-{away_score}" if home_score != "N/A" else "TBD"
        utc_date = match.get("utcDate", "")
        date = utc_date[:10] if utc_date else "Unknown"
        print(f"{date} | {home_team[:20]:<20} | {away_team[:20]:<20} | {score_str}")


def print_scorers(data: Any, limit: int) -> None:
    scorers = data.get("scorers", [])
    if not scorers:
        print("No scorers data was returned by the API.")
        return

    print("Top Premier League Scorers")
    print("Player | Team | Goals | Assists")
    print("-------|------|-------|--------")
    for scorer in scorers[:limit]:
        player = scorer.get("player", {}).get("name", "Unknown")
        team = scorer.get("team", {}).get("name", "Unknown")
        goals = scorer.get("goals", 0)
        assists = scorer.get("assists", 0) or 0
        print(f"{player[:25]:<25} | {team[:20]:<20} | {goals:>5} | {assists:>6}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Premier League standings, matches, or scorers from the Football Data API."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top teams to display in standings (default: 10).",
    )
    parser.add_argument(
        "--matches",
        action="store_true",
        help="Fetch recent matches instead of standings.",
    )
    parser.add_argument(
        "--scorers",
        action="store_true",
        help="Fetch top scorers instead of standings.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of matches or scorers to display (default: 10).",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()

    try:
        api_token = load_api_token()
        if args.matches:
            limit = validate_top(args.limit)  # Reuse validation
            data = fetch_matches(api_token)
            print_matches(data, limit)
        elif args.scorers:
            limit = validate_top(args.limit)
            data = fetch_scorers(api_token)
            print_scorers(data, limit)
        else:
            top = validate_top(args.top)
            data = fetch_pl_standings(api_token)
            print_standings(data, top)
        return 0
    except ValueError as error:
        print(f"Configuration error: {error}")
    except PermissionError as error:
        print(f"Authorization error: {error}")
    except ConnectionError as error:
        print(f"Network error: {error}")
    except FileNotFoundError as error:
        print(f"API error: {error}")
    except RuntimeError as error:
        print(f"API error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
