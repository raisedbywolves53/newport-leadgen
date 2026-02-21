"""USASpending.gov API client for federal spending market sizing.

No API key required. All endpoints are POST with JSON body.
No daily rate limits — offloads market sizing entirely from SAM.gov.

Usage:
    from enrichment.usaspending_client import USASpendingClient
    client = USASpendingClient()
    data = client.spending_by_naics(naics_require=["4244"], time_period_start="2023-10-01", time_period_end="2024-09-30")
"""

import logging
import time

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://api.usaspending.gov/api/v2"


class USASpendingClient:
    """Thin wrapper around USASpending.gov REST API. No API key needed."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })
        self._request_count = 0

    def _request(self, path: str, body: dict) -> dict:
        """POST request with retry on server errors."""
        url = f"{BASE_URL}/{path.lstrip('/')}"

        for attempt in range(3):
            resp = self.session.post(url, json=body, timeout=60)
            if resp.status_code in (429, 500, 502, 503):
                wait = min(2 ** attempt * 2, 30)
                log.warning(f"USASpending {resp.status_code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            self._request_count += 1
            return resp.json()

        resp.raise_for_status()
        return {}

    @property
    def stats(self) -> dict:
        return {"requests": self._request_count}

    @staticmethod
    def fiscal_year_range(fy: int) -> tuple[str, str]:
        """Convert fiscal year to date range. FY2024 = 2023-10-01 to 2024-09-30."""
        return (f"{fy - 1}-10-01", f"{fy}-09-30")

    def spending_by_naics(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        limit: int = 50,
    ) -> list[dict]:
        """Aggregate federal spending by NAICS code.

        naics_require: list of NAICS prefixes (e.g., ["4244"] matches all 4244xx codes)
        """
        body = {
            "category": "naics",
            "filters": {
                "time_period": [
                    {"start_date": time_period_start, "end_date": time_period_end}
                ],
                "naics_codes": {"require": naics_require},
            },
            "limit": limit,
            "page": 1,
        }

        try:
            data = self._request("search/spending_by_category/naics", body)
        except requests.HTTPError as e:
            log.warning(f"Spending by NAICS failed: {e}")
            return []

        return data.get("results", [])

    def spending_by_agency(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        limit: int = 50,
    ) -> list[dict]:
        """Aggregate federal spending by awarding agency for given NAICS codes."""
        body = {
            "category": "awarding_agency",
            "filters": {
                "time_period": [
                    {"start_date": time_period_start, "end_date": time_period_end}
                ],
                "naics_codes": {"require": naics_require},
            },
            "limit": limit,
            "page": 1,
        }

        try:
            data = self._request("search/spending_by_category/awarding_agency", body)
        except requests.HTTPError as e:
            log.warning(f"Spending by agency failed: {e}")
            return []

        return data.get("results", [])

    def search_awards(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        recipient_search_text: str = "",
        limit: int = 100,
        page: int = 1,
    ) -> dict:
        """Search individual awards with NAICS and date filters."""
        filters: dict = {
            "time_period": [
                {"start_date": time_period_start, "end_date": time_period_end}
            ],
            "naics_codes": {"require": naics_require},
        }
        if recipient_search_text:
            filters["recipient_search_text"] = [recipient_search_text]

        body = {
            "filters": filters,
            "fields": [
                "Award ID",
                "Recipient Name",
                "Awarding Agency",
                "Awarding Sub Agency",
                "Award Amount",
                "Total Outlays",
                "Description",
                "NAICS Code",
                "NAICS Description",
                "Period of Performance Start Date",
                "Period of Performance Current End Date",
                "Contract Award Type",
                "recipient_id",
            ],
            "limit": limit,
            "page": page,
            "sort": "Award Amount",
            "order": "desc",
        }

        try:
            data = self._request("search/spending_by_award", body)
        except requests.HTTPError as e:
            log.warning(f"Award search failed: {e}")
            return {"results": [], "page_metadata": {"total": 0}}

        return data
