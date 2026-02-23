"""Grants.gov API client for USDA food grant monitoring.

No API key required. All endpoints are POST with JSON body or GET with params.
Monitors federal grant opportunities for USDA food programs: LFPA, TEFAP,
CSFP, FDPIR, Farm to School, DoD Fresh.

Usage:
    from enrichment.grants_client import GrantsClient
    client = GrantsClient()
    grants = client.search_food_grants()
"""

import logging
import time

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://api.grants.gov/v1/api"


class GrantsClient:
    """Wrapper around Grants.gov REST API. No API key needed."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._request_count = 0

    def _request(self, path: str, body: dict | None = None, method: str = "POST") -> dict:
        """HTTP request with retry on server errors."""
        url = f"{BASE_URL}/{path.lstrip('/')}"

        for attempt in range(3):
            if method == "GET" or body is None:
                resp = self.session.get(url, timeout=60)
            else:
                resp = self.session.post(url, json=body, timeout=60)
            if resp.status_code in (429, 500, 502, 503):
                wait = min(2 ** attempt * 2, 30)
                log.warning(f"Grants.gov {resp.status_code}, retrying in {wait}s...")
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

    def search_grants(
        self,
        keyword: str = "",
        funding_categories: str = "",
        agencies: str = "",
        opp_statuses: str = "posted|forecasted",
        rows: int = 100,
        start_record: int = 0,
    ) -> dict:
        """Search grant opportunities.

        Args:
            keyword: Free text search
            funding_categories: Category code (e.g., "AR" for Agriculture)
            agencies: Agency code filter
            opp_statuses: Status filter (pipe-separated: "posted|forecasted")
            rows: Results per page
            start_record: Pagination start
        """
        body: dict = {
            "oppStatuses": opp_statuses,
            "rows": rows,
            "startRecordNum": start_record,
            "sortBy": "openDate|desc",
        }

        if keyword:
            body["keyword"] = keyword
        if funding_categories:
            body["fundingCategories"] = funding_categories
        if agencies:
            body["agencies"] = agencies

        try:
            data = self._request("search2", body)
        except requests.HTTPError as e:
            log.warning(f"Grants.gov search failed: {e}")
            return {"oppHits": [], "hitCount": 0}

        # Response wraps results under "data" key
        inner = data.get("data", data)
        return inner

    def fetch_opportunity(self, opp_id: str) -> dict:
        """Fetch full details for a specific grant opportunity."""
        try:
            return self._request(f"fetchOpportunity?oppId={opp_id}", method="GET")
        except requests.HTTPError as e:
            log.warning(f"Grants.gov fetch failed for {opp_id}: {e}")
            return {}

    def search_food_grants(
        self,
        keywords: list[str] | None = None,
        max_per_keyword: int = 100,
    ) -> list[dict]:
        """Search for USDA food-related grants across multiple keywords.

        Deduplicates by opportunity ID across keyword searches.
        """
        if keywords is None:
            keywords = [
                "food distribution",
                "food commodity",
                "school nutrition",
                "TEFAP",
                "LFPA",
                "CSFP",
                "FDPIR",
                "farm to school",
                "food purchase assistance",
                "emergency food",
                "child nutrition",
                "school lunch",
                "food bank",
                "commodity supplemental",
            ]

        all_grants = []
        seen_ids = set()

        print(f"Searching Grants.gov for food-related grants...")
        print(f"  Keywords: {len(keywords)}")
        print(f"  Funding category: AR (Agriculture)")

        for i, kw in enumerate(keywords):
            print(f"  [{i + 1}/{len(keywords)}] '{kw}'...", end=" ", flush=True)

            data = self.search_grants(
                keyword=kw,
                funding_categories="AR",
                rows=max_per_keyword,
            )

            hits = data.get("oppHits", [])
            new_count = 0
            for hit in hits:
                opp_id = str(hit.get("id", ""))
                if opp_id and opp_id not in seen_ids:
                    seen_ids.add(opp_id)
                    all_grants.append(hit)
                    new_count += 1

            print(f"{len(hits)} results, {new_count} new")
            time.sleep(0.5)

        # Also search without category filter for broader coverage
        broad_keywords = ["USDA food", "subsistence", "meal program"]
        for kw in broad_keywords:
            print(f"  [broad] '{kw}'...", end=" ", flush=True)
            data = self.search_grants(keyword=kw, rows=max_per_keyword)
            hits = data.get("oppHits", [])
            new_count = 0
            for hit in hits:
                opp_id = str(hit.get("id", ""))
                if opp_id and opp_id not in seen_ids:
                    seen_ids.add(opp_id)
                    all_grants.append(hit)
                    new_count += 1
            print(f"{len(hits)} results, {new_count} new")
            time.sleep(0.5)

        print(f"\n  Total unique grants: {len(all_grants)}")
        return all_grants

    @staticmethod
    def flatten_grant(grant: dict) -> dict:
        """Flatten grant hit into flat dict for CSV output."""
        # Handle both search hit format and full opportunity format
        return {
            "opportunity_id": grant.get("id", grant.get("opportunityId", "")),
            "opportunity_number": grant.get("number", grant.get("opportunityNumber", "")),
            "title": grant.get("title", grant.get("opportunityTitle", "")),
            "agency_code": grant.get("agencyCode", ""),
            "agency_name": grant.get("agencyName", grant.get("owningAgencyName", "")),
            "open_date": grant.get("openDate", ""),
            "close_date": grant.get("closeDate", ""),
            "status": grant.get("oppStatus", ""),
            "doc_type": grant.get("docType", ""),
            "funding_category": "Agriculture",
            "aln_list": grant.get("alnList", ""),
            "award_ceiling": grant.get("awardCeiling", ""),
            "award_floor": grant.get("awardFloor", ""),
            "estimated_funding": grant.get("estimatedFunding", ""),
        }
