"""Fare search provider integration for international and domestic routes."""

import os
import httpx
from datetime import datetime

_FARE_API_TOKEN = os.getenv("FARE_API_TOKEN", "8a6e17e30be4d6944e14869e891b5cd2")
_AFFILIATE_MARKER = 715246
_AFFILIATE_TRS = 516093
_FARE_API_BASE = "https://api.travelpayouts.com/aviasales/v3"
_PARTNER_LINKS_API = "https://api.travelpayouts.com/links/v1/create"


def _build_booking_url(origin: str, destination: str, departure_date: str, passengers: int = 1) -> str:
    """Generate correct Travelpayouts affiliate link via Partner Links API."""
    try:
        dt = datetime.fromisoformat(departure_date[:10])
        date_str = dt.strftime("%d%m")
    except Exception:
        date_str = "0101"

    direct_url = f"https://www.aviasales.ru/search/{origin}{date_str}{destination}{passengers}"

    try:
        response = httpx.post(
            _PARTNER_LINKS_API,
            headers={"X-Access-Token": _FARE_API_TOKEN},
            json={
                "trs": _AFFILIATE_TRS,
                "marker": _AFFILIATE_MARKER,
                "shorten": False,
                "links": [{"url": direct_url}]
            },
            timeout=5
        )
        data = response.json()
        partner_url = data.get("result", {}).get("links", [{}])[0].get("partner_url")
        if partner_url:
            return partner_url
    except Exception:
        pass

    return f"{direct_url}?marker={_AFFILIATE_MARKER}"


class SearchFares:
    """Search for cheap flights across global and domestic routes."""

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        currency: str = "RUB",
        direct: bool = False,
        limit: int = 30,
        passengers: int = 1,
    ) -> list[dict]:
        """Search for flights on a specific date."""
        if not _FARE_API_TOKEN:
            return []

        month = departure_date[:7]
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": month,
            "currency": currency.lower(),
            "sorting": "price",
            "direct": str(direct).lower(),
            "limit": limit,
            "token": _FARE_API_TOKEN,
        }

        try:
            r = httpx.get(f"{_FARE_API_BASE}/prices_for_dates", params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception:
            return []

        results = []
        for t in data.get("data", []):
            dep_at = t.get("departure_at", "")
            if not dep_at.startswith(departure_date):
                continue

            results.append({
                "price": t.get("price", 0),
                "currency": currency.upper(),
                "stops": t.get("transfers", 0),
                "booking_url": _build_booking_url(origin, destination, dep_at, passengers),
                "legs": [{
                    "departure_airport": t.get("origin", origin),
                    "arrival_airport": t.get("destination", destination),
                    "departure_time": dep_at,
                    "arrival_time": None,
                    "duration": t.get("duration", 0),
                    "airline": t.get("airline", ""),
                    "flight_number": t.get("flight_number", ""),
                }],
            })

        return results

    def search_dates(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str,
        currency: str = "RUB",
        direct: bool = False,
        limit: int = 30,
        passengers: int = 1,
    ) -> list[dict]:
        """Find cheapest available dates in a range."""
        if not _FARE_API_TOKEN:
            return []

        month = start_date[:7]
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": month,
            "currency": currency.lower(),
            "sorting": "price",
            "direct": str(direct).lower(),
            "limit": limit,
            "token": _FARE_API_TOKEN,
        }

        try:
            r = httpx.get(f"{_FARE_API_BASE}/prices_for_dates", params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception:
            return []

        results = []
        for t in data.get("data", []):
            dep_at = t.get("departure_at", "")
            date_only = dep_at[:10]
            if date_only < start_date or date_only > end_date:
                continue

            results.append({
                "date": dep_at,
                "price": t.get("price", 0),
                "currency": currency.upper(),
                "airline": t.get("airline", ""),
                "flight_number": t.get("flight_number", ""),
                "stops": t.get("transfers", 0),
                "return_date": None,
                "booking_url": _build_booking_url(origin, destination, dep_at, passengers),
            })

        return results
