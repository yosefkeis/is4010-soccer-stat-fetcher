import argparse
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


API_URL = "https://api.football-data.org/v4/competitions/PL/standings"


def load_api_token() -> str:
    token = os.getenv("FOOTBALL_DATA_API_TOKEN")
    if not token:
        raise ValueError(
            "API token not found. Create a .env file with FOOTBALL_DATA_API_TOKEN=your_token"
        )
    return token


def fetch_pl_standings(api_token: str) -> Any:
    headers = {"X-Auth-Token": api_token}
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
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
        print(
            f"{row.get('position'):>8} | "
            f"{row.get('team', {}).get('name', 'Unknown')[:25]:<25} | "
            f"{row.get('playedGames', 0):>6} | "
            f"{row.get('won', 0):>3} | "
            f"{row.get('draw', 0):>5} | "
            f"{row.get('lost', 0):>4} | "
            f"{row.get('points', 0):>6}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Premier League standings from the Football Data API."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top teams to display from the standings.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()

    try:
        api_token = load_api_token()
        data = fetch_pl_standings(api_token)
        print_standings(data, args.top)
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
