"""Fare search provider integration for international and domestic routes."""

import os
import httpx

# Все запросы идут через собственный прокси-сервер
# Токены хранятся только на сервере в .env файле
_PROXY_BASE = os.getenv("AIRJOURNEY_API", "http://2.26.84.243:8000")


class SearchFares:
    """Search for cheap flights via AirJourney proxy API."""

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        currency: str = "RUB",
        direct: bool = False,
        limit: int = 30,
        passengers: int = 1,
        return_date: str | None = None,
    ) -> list[dict]:
        """Search for flights on a specific date."""
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": departure_date[:7],
            "currency": currency.lower(),
            "direct": str(direct).lower(),
            "limit": limit,
            "one_way": "false" if return_date else "true",
        }
        if return_date:
            params["return_at"] = return_date

        try:
            r = httpx.get(f"{_PROXY_BASE}/search/flights", params=params, timeout=15)
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
                "booking_url": t.get("booking_url", ""),
                "legs": [{
                    "departure_airport": t.get("origin", origin),
                    "arrival_airport": t.get("destination", destination),
                    "departure_time": dep_at,
                    "arrival_time": t.get("return_at"),
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
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": start_date[:7],
            "currency": currency.lower(),
            "direct": str(direct).lower(),
            "limit": limit,
            "one_way": "true",
        }

        try:
            r = httpx.get(f"{_PROXY_BASE}/search/flights", params=params, timeout=15)
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
                "booking_url": t.get("booking_url", ""),
            })

        return results
