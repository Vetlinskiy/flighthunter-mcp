# ✈️ FlightHunter MCP

A Model Context Protocol (MCP) server that gives Claude the ability to search for cheap flights — including Russian airlines — and present direct booking links.

---

## Preview

![Search example](images/screenshot1.png)

---

## Features

- 🔍 Search flights by specific date
- 📅 Find cheapest dates across a date range
- 🇷🇺 Russian airlines included (Aeroflot, Pobeda, S7, NordStar, and more)
- 🌍 Global routes via Google Flights
- 💸 Direct booking links in results
- ⚡ Works inside Claude Desktop — just ask naturally

---

## Requirements

- macOS or Linux
- [Claude Desktop](https://claude.ai/download)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

---

## Installation

### 1. Install the base flight engine

```bash
uv tool install git+https://github.com/punitarani/fli.git
```

### 2. Install FlightHunter files

Find your install path:

```bash
SITE=$(find ~/.local -path "*/site-packages/fli" -type d | head -1)
echo $SITE
```

Download `fare_search.py` and `server.py` from this repo, then copy them:

```bash
cp fare_search.py "$SITE/search/fare_search.py"
cp server.py "$SITE/mcp/server.py"
```

### 3. Install the FlightHunter launcher

```bash
cp flighthunter-mcp ~/.local/bin/flighthunter-mcp
chmod +x ~/.local/bin/flighthunter-mcp
```

### 4. Configure Claude Desktop

Open your Claude Desktop config:

```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
nano ~/.config/Claude/claude_desktop_config.json
```

Add the following:

```json
{
  "mcpServers": {
    "FlightHunter": {
      "command": "/Users/YOUR_USERNAME/.local/bin/flighthunter-mcp",
      "args": []
    }
  }
}
```

> **Tip:** Find the exact path by running `which flighthunter-mcp` in your terminal.

### 5. Restart Claude Desktop

That's it! Just ask Claude to find flights.

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

```
Find round-trip flights from JFK to LHR next month
```

Claude will return results sorted by price with direct booking links.

---

## How It Works

```
Claude
  ↓
FlightHunter MCP Server
  ↓                ↓
Google Flights    Fare Search Engine
(global routes)   (domestic + CIS routes)
  ↓                ↓
  └──── merged, sorted by price ────┘
              ↓
    Results with booking links
```

---

## Optional Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `FLI_MCP_DEFAULT_CURRENCY` | Currency code for results | `USD` |
| `FLI_MCP_DEFAULT_PASSENGERS` | Default passenger count | `1` |
| `FLI_MCP_MAX_RESULTS` | Max results returned | unlimited |
| `FLI_MCP_DEFAULT_CABIN_CLASS` | Default cabin class | `ECONOMY` |

Example:

```json
{
  "mcpServers": {
    "FlightHunter": {
      "command": "/Users/YOUR_USERNAME/.local/bin/flighthunter-mcp",
      "args": [],
      "env": {
        "FLI_MCP_DEFAULT_CURRENCY": "RUB",
        "FLI_MCP_MAX_RESULTS": "10"
      }
    }
  }
}
```

---

## Built on

FlightHunter is built on top of [fli](https://github.com/punitarani/fli) by [@punitarani](https://github.com/punitarani) — an excellent open-source MCP server for Google Flights search.

We extended it with:
- 🇷🇺 Support for Russian and CIS airlines
- 🔗 Direct booking links in search results
- 🔀 Merged results from multiple flight data sources

A big thank you to the original author for the solid foundation! ⭐

---

## License

MIT
