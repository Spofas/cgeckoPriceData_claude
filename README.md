# Crypto Price Data — Top 5,000 Coins

Auto-updated price data for the top 5,000 cryptocurrencies by market cap, sourced from [CoinGecko](https://www.coingecko.com/). Refreshed every 2 hours via GitHub Actions.

## Download

| Format | Link |
|--------|------|
| CSV | [data/prices.csv](data/prices.csv) |
| JSON | [data/prices.json](data/prices.json) |

## Google Sheets

Paste this formula into any cell:

```
=IMPORTDATA("https://raw.githubusercontent.com/spofas/cgeckopricedata_claude/main/data/prices.csv")
```

Google Sheets will auto-refresh the data periodically.

## Excel

**Option 1:** Download `data/prices.csv` and open it directly.

**Option 2 (auto-refresh):** Go to **Data → From Web** and enter:
```
https://raw.githubusercontent.com/spofas/cgeckopricedata_claude/main/data/prices.csv
```

## Raw URLs (for programmatic access)

```
https://raw.githubusercontent.com/spofas/cgeckopricedata_claude/main/data/prices.csv
https://raw.githubusercontent.com/spofas/cgeckopricedata_claude/main/data/prices.json
```

## Data Fields

| Field | Description |
|-------|-------------|
| `market_cap_rank` | Rank by market capitalization |
| `id` | CoinGecko coin identifier |
| `symbol` | Ticker symbol (e.g. btc, eth) |
| `name` | Full coin name |
| `current_price` | Current price in USD |
| `market_cap` | Market capitalization in USD |
| `total_volume` | 24h trading volume in USD |
| `price_change_24h` | Price change in USD (24h) |
| `price_change_percentage_24h` | Price change percentage (24h) |
| `market_cap_change_24h` | Market cap change in USD (24h) |
| `market_cap_change_percentage_24h` | Market cap change percentage (24h) |
| `circulating_supply` | Coins currently in circulation |
| `total_supply` | Total coins that exist |
| `max_supply` | Maximum possible supply (null if unlimited) |
| `ath` | All-time high price in USD |
| `ath_change_percentage` | Percentage from all-time high |
| `ath_date` | Date of all-time high |
| `last_updated` | When this coin's data was last updated |

## Update Schedule

Runs every 2 hours via GitHub Actions (~12 times/day). Uses the CoinGecko free API tier (20 API calls per refresh, ~7,400/month out of 10,000 limit).

## Run Locally

```bash
git clone https://github.com/spofas/cgeckopricedata_claude.git
cd cgeckopricedata_claude
pip install -r requirements.txt
python fetch_prices.py
```

Optionally set `COINGECKO_API_KEY` for faster fetching:
```bash
export COINGECKO_API_KEY=your_demo_api_key_here
python fetch_prices.py
```

Get a free Demo API key at [coingecko.com/en/api/pricing](https://www.coingecko.com/en/api/pricing).

## Fork & Set Up Your Own

1. Fork this repository
2. Go to **Settings → Secrets and variables → Actions**
3. Add `COINGECKO_API_KEY` as a repository secret (optional but recommended)
4. Enable GitHub Actions in your fork
5. To enable the landing page: go to **Settings → Pages** and set source to the `main` branch

## Landing Page

This repo includes an `index.html` that can be served via [GitHub Pages](https://pages.github.com/). Enable it in your repo settings to get a public page with download links and integration instructions.

## Data Source

All data is provided by the [CoinGecko API](https://docs.coingecko.com/). This project is not affiliated with CoinGecko.
