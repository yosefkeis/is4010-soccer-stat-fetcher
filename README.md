# is4010-soccer-stat-fetcher

A Python command-line tool that fetches Premier League standings from the Football-Data API. This tool is designed for fans or analysts who want a quick way to view the current league table from the command line without opening a browser.

## What it does

`is4010-soccer-stat-fetcher` calls the Football-Data API and prints the current Premier League standings, including position, team name, games played, wins, draws, losses, and points. It keeps the API token secure in a `.env` file and handles common problems like missing configuration or invalid credentials.

## Installation

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Add your Football-Data API token to `.env`:

   ```text
   FOOTBALL_DATA_API_TOKEN=your_api_token_here
   ```

   You can request a free token by signing up at https://www.football-data.org/.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI to display the top Premier League clubs:

```bash
python main.py
```

Show only the top 5 teams:

```bash
python main.py --top 5
```

Fetch recent matches:

```bash
python main.py --matches
```

Show the last 5 matches:

```bash
python main.py --matches --limit 5
```

Fetch top scorers:

```bash
python main.py --scorers
```

Show the top 10 scorers:

```bash
python main.py --scorers --limit 10
```

## Examples

Display the default top standings:

```bash
python main.py
```

Expected output:

```text
Premier League Standings
Position | Team | Played | Won | Drawn | Lost | Points
---------|------|--------|-----|-------|------|-------
       1 | Arsenal                 |      5 |   4 |     1 |    0 |      13
       2 | Manchester City         |      5 |   4 |     0 |    1 |      12
```

Display the top 3 teams only:

```bash
python main.py --top 3
```

Display errors when the API token is missing:

```bash
python main.py
```

Expected output:

```text
Configuration error: API token not found. Create a .env file with FOOTBALL_DATA_API_TOKEN=your_token
```

Display recent matches:

```bash
python main.py --matches --limit 3
```

Expected output:

```text
Recent Premier League Matches
Date | Home Team | Away Team | Score
-----|----------|-----------|------
2024-04-28 | Arsenal | Chelsea | 2-1
```

Display top scorers:

```bash
python main.py --scorers --limit 5
```

Expected output:

```text
Top Premier League Scorers
Player | Team | Goals | Assists
-------|------|-------|--------
Erling Haaland | Manchester City |    24 |      7
Son Heung-min | Tottenham |    15 |      5
```

## Tests

Run the test suite with:

```bash
pytest
```

This repository includes a GitHub Actions workflow at `.github/workflows/tests.yml` that installs dependencies and runs `pytest` on every push and pull request to `main`.

## Limitations and future ideas

- Currently only fetches the Premier League standings.
- Future improvements could include match scores, team statistics, or support for other competitions.
