# is4010-soccer-stat-fetcher
A Python-based CLI tool that fetches Premier League standings using the Football-Data API.

## Setup
1. Copy `.env.example` to `.env`.
2. Add your API token to `.env`:

   ```text
   FOOTBALL_DATA_API_TOKEN=your_api_token_here
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python main.py
```

You can show fewer or more top teams with `--top`:

```bash
python main.py --top 5
```

## Notes
- The API token is kept secret in `.env`, which is ignored by Git.
- The code uses `main()` for organization and handles HTTP errors and missing configuration.

## Tests

```bash
pytest
```

The repository also includes a GitHub Actions workflow at `.github/workflows/tests.yml` that runs `pytest` on every push and pull request to `main`.
