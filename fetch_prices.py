#!/usr/bin/env python3
"""Fetch price data for the top 5000 cryptocurrencies from CoinGecko."""

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone

import requests

API_BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"
TOTAL_COINS = 5000
PER_PAGE = 250
TOTAL_PAGES = TOTAL_COINS // PER_PAGE  # 20
DATA_DIR = "data"

FIELDS = [
    "market_cap_rank",
    "id",
    "symbol",
    "name",
    "current_price",
    "market_cap",
    "total_volume",
    "price_change_24h",
    "price_change_percentage_24h",
    "market_cap_change_24h",
    "market_cap_change_percentage_24h",
    "circulating_supply",
    "total_supply",
    "max_supply",
    "ath",
    "ath_change_percentage",
    "ath_date",
    "last_updated",
]


def get_delay(api_key: str | None) -> float:
    """Return delay between API calls based on whether we have an API key."""
    return 2.5 if api_key else 7.0


def fetch_page(
    session: requests.Session, page: int, api_key: str | None
) -> list[dict]:
    """Fetch a single page of coin market data with retry on rate limit."""
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": PER_PAGE,
        "page": page,
        "sparkline": "false",
    }
    if api_key:
        params["x_cg_demo_api_key"] = api_key

    backoff_times = [30, 60, 120]
    last_error = None

    for attempt in range(4):  # 1 initial + 3 retries
        try:
            resp = session.get(API_BASE_URL, params=params, timeout=30)

            if resp.status_code == 429:
                if attempt < 3:
                    wait = int(
                        resp.headers.get("Retry-After", backoff_times[attempt])
                    )
                    print(f"  Rate limited on page {page}, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()

            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            last_error = e
            if attempt < 3:
                wait = backoff_times[attempt]
                print(f"  Error on page {page}: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

    raise last_error  # Should not reach here, but just in case


def fetch_all() -> list[dict]:
    """Fetch market data for the top 5000 coins."""
    api_key = os.environ.get("COINGECKO_API_KEY", "").strip() or None
    delay = get_delay(api_key)

    if api_key:
        print(f"Using API key (delay: {delay}s between calls)")
    else:
        print(f"No API key found (delay: {delay}s between calls)")

    all_coins = []
    session = requests.Session()

    for page in range(1, TOTAL_PAGES + 1):
        print(f"Fetching page {page}/{TOTAL_PAGES}...")
        coins = fetch_page(session, page, api_key)
        all_coins.extend(coins)
        print(f"  Got {len(coins)} coins (total: {len(all_coins)})")

        if page < TOTAL_PAGES:
            time.sleep(delay)

    return all_coins


def filter_fields(coin: dict) -> dict:
    """Extract only the fields we want from a coin record."""
    return {field: coin.get(field) for field in FIELDS}


def write_csv(coins: list[dict], filepath: str) -> None:
    """Write coin data to CSV."""
    filtered = [filter_fields(c) for c in coins]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(filtered)


def write_json(coins: list[dict], filepath: str) -> None:
    """Write coin data to JSON with metadata."""
    filtered = [filter_fields(c) for c in coins]
    output = {
        "last_updated_utc": datetime.now(timezone.utc).isoformat(),
        "count": len(filtered),
        "data": filtered,
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)


def write_metadata(coins: list[dict], filepath: str) -> None:
    """Write a small metadata JSON for the landing page."""
    metadata = {
        "last_updated_utc": datetime.now(timezone.utc).isoformat(),
        "count": len(coins),
        "top_10": [
            {
                "rank": c.get("market_cap_rank"),
                "name": c.get("name"),
                "symbol": c.get("symbol"),
                "price": c.get("current_price"),
            }
            for c in coins[:10]
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def main():
    coins = fetch_all()

    os.makedirs(DATA_DIR, exist_ok=True)

    csv_path = os.path.join(DATA_DIR, "prices.csv")
    json_path = os.path.join(DATA_DIR, "prices.json")
    meta_path = os.path.join(DATA_DIR, "metadata.json")

    write_csv(coins, csv_path)
    write_json(coins, json_path)
    write_metadata(coins, meta_path)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\nDone! {len(coins)} coins written at {timestamp}")
    print(f"  CSV:  {csv_path}")
    print(f"  JSON: {json_path}")
    print(f"  Meta: {meta_path}")


if __name__ == "__main__":
    main()
