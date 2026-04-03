# ✈️ FlightHunter MCP

A Model Context Protocol (MCP) server that gives Claude the ability to search for cheap flights — including Russian airlines — and present direct booking links.

---

## Features

- 🔍 Search flights by specific date
- 📅 Find cheapest dates across a date range
- 🇷🇺 Russian airlines included (Aeroflot, Pobeda, S7, NordStar, and more)
- 🌍 Global routes via Google Flights
- 💸 Direct booking links in results
- ⚡ Works inside Claude Desktop — just ask naturally

---
## Preview

![FlightHunter в Claude](images/screenshot1.png)

## Requirements

- macOS or Linux
- [Claude Desktop](https://claude.ai/download)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

---

## Installation

### 1. Install FlightHunter via uv
```bash
uv tool install flighthunter-mcp
```

### 2. Configure Claude Desktop

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
      "command": "flighthunter-mcp",
      "args": []
    }
  }
}
```

### 3. Restart Claude Desktop

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
| `FLIGHTHUNTER_CURRENCY` | Currency code for results | `USD` |
| `FLIGHTHUNTER_PASSENGERS` | Default passenger count | `1` |
| `FLIGHTHUNTER_MAX_RESULTS` | Max results returned | unlimited |
| `FLIGHTHUNTER_CABIN_CLASS` | Default cabin class | `ECONOMY` |

Example:

```json
{
  "mcpServers": {
    "FlightHunter": {
      "command": "/Users/YOUR_USERNAME/.local/bin/flighthunter-mcp",
      "args": [],
      "env": {
        "FLIGHTHUNTER_CURRENCY": "RUB",
        "FLIGHTHUNTER_MAX_RESULTS": "20"
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
