# ✈️ FlightHunter MCP

A Model Context Protocol (MCP) server that gives Claude the ability to search for cheap flights — including Russian airlines — and present direct booking links.

Built on top of [fli](https://github.com/punitarani/fli) with an extended fare search layer covering domestic and CIS routes.

---

## Features

- 🔍 Search flights by specific date
- 📅 Find cheapest dates across a date range
- 🇷🇺 Russian airlines included (Aeroflot, Pobeda, S7, NordStar, and more)
- 🌍 Global routes via Google Flights
- 💸 Direct booking links in results
- ⚡ Works inside Claude Desktop

---

## Requirements

- macOS or Linux
- [Claude Desktop](https://claude.ai/download)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager
- A free API token from [Travelpayouts](https://travelpayouts.com)

---

## Installation

### 1. Install `fli` via uv

```bash
uv tool install flights
```

### 2. Install the fare search extension

Download `fare_search.py` from this repo and place it here:

```bash
# Find your fli install path
SITE=$(uv tool run flights python -c "import fli; import os; print(os.path.dirname(fli.__file__))" 2>/dev/null || \
  find ~/.local -path "*/site-packages/fli" -type d | head -1)

# Copy fare_search.py into the fli search directory
cp fare_search.py "$SITE/search/fare_search.py"
```

### 3. Replace `server.py`

```bash
cp server.py "$SITE/mcp/server.py"
```

### 4. Get your API credentials

1. Register at [travelpayouts.com](https://travelpayouts.com)
2. Go to **API & Data → Data API** — copy your **Token**
3. Go to **Programs → Aviasales** — copy your **Marker**

### 5. Configure Claude Desktop

Open your Claude Desktop config:

```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
nano ~/.config/Claude/claude_desktop_config.json
```

Add the following (replace with your real credentials):

```json
{
  "mcpServers": {
    "flight-search": {
      "command": "/Users/YOUR_USERNAME/.local/bin/fli-mcp",
      "args": [],
      "env": {
        "FARE_API_TOKEN": "your_token_here",
        "AFFILIATE_MARKER": "your_marker_here"
      }
    }
  }
}
```

> **Note:** Find the exact path to `fli-mcp` by running `which fli-mcp` in your terminal.

### 6. Restart Claude Desktop

Quit and reopen Claude Desktop. The flight search tools will appear automatically.

---

## Usage

Once installed, just ask Claude naturally:

```
Find me the cheapest flights from Moscow to Antalya in April
```

```
Search for flights SVO → AYT on April 7
```

```
What are the cheapest travel dates from LED to BCN in May?
```

Claude will return results with prices and **direct booking links** where available.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FARE_API_TOKEN` | Yes | API token from Travelpayouts |
| `AFFILIATE_MARKER` | No | Your affiliate marker (enables booking links) |
| `FLI_MCP_DEFAULT_CURRENCY` | No | Default currency code, e.g. `RUB` or `USD` |
| `FLI_MCP_DEFAULT_PASSENGERS` | No | Default passenger count (default: `1`) |
| `FLI_MCP_MAX_RESULTS` | No | Limit number of results returned |
| `FLI_MCP_DEFAULT_CABIN_CLASS` | No | Default cabin class (default: `ECONOMY`) |

---

## How It Works

```
Claude
  ↓
FlightHunter MCP Server
  ↓                ↓
Google Flights    Fare Search Provider
(global routes)   (domestic + CIS routes)
  ↓                ↓
  └──── merged, sorted by price ────┘
              ↓
    Results with booking links
```

---

## License

MIT
