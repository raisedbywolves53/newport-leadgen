"""SAM.gov API client for federal contract opportunities.

Wraps the SAM.gov Opportunities API for active solicitations, pre-solicitations,
and sources sought. This is the ONLY public REST API SAM.gov exposes.

Historical contract award data (FPDS) is available through USASpending.gov,
NOT through SAM.gov. See usaspending_client.py for award queries.

Rate limits: 1,000 requests/day with a free API key.
Key mitigations:
  - Opportunities only takes 1 NAICS at a time, so iterate + deduplicate
  - Cache layer in contract_scanner.py prevents redundant calls within 24hrs

Usage:
    from enrichment.sam_client import SAMClient
    client = SAMClient(api_key="...")
    opps = client.search_opportunities(naics_code="424410", ptype="o")
"""

import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

SAM_BASE_URL = "https://api.sam.gov"

# Contract Opportunities endpoint
OPPORTUNITIES_URL = "https://api.sam.gov/opportunities/v2/search"


class SAMClient:
    """Thin wrapper around SAM.gov Opportunities API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("SAM_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "SAM_API_KEY not set. Get a free key at https://sam.gov/content/entity-registration"
            )
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })
        self._request_count = 0
        self._daily_count = 0
        self._daily_limit = 1000

    # --- low-level helpers ---

    def _request(self, method: str, url: str, **kwargs) -> dict:
        """Make an API request with retry on 429 and API key as query param."""
        # SAM.gov expects API key as query parameter, not header
        params = kwargs.pop("params", {}) or {}
        params["api_key"] = self.api_key
        kwargs["params"] = params

        if self._daily_count >= 900:
            log.warning(
                f"Approaching SAM.gov daily limit: {self._daily_count}/{self._daily_limit} requests used"
            )
        if self._daily_count >= self._daily_limit:
            raise RuntimeError(
                f"SAM.gov daily limit reached ({self._daily_limit} requests). "
                "Wait until tomorrow or use cached data."
            )

        for attempt in range(4):
            resp = self.session.request(method, url, timeout=30, **kwargs)
            if resp.status_code == 429:
                wait = min(2 ** attempt * 5, 60)
                log.warning(f"Rate limited by SAM.gov, retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            self._request_count += 1
            self._daily_count += 1
            return resp.json()

        resp.raise_for_status()
        return {}

    @property
    def stats(self) -> dict:
        return {
            "requests": self._request_count,
            "daily_usage": f"{self._daily_count}/{self._daily_limit}",
        }

    # =========================================================================
    # Opportunities API (active solicitations)
    # =========================================================================

    def search_opportunities(
        self,
        naics_code: str = "",
        posted_from: str = "",
        posted_to: str = "",
        ptype: str = "",
        keyword: str = "",
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Search contract opportunities. Single NAICS code per request (API limitation).

        ptype values:
            p = pre-solicitation
            o = solicitation
            r = sources sought
            k = combined synopsis/solicitation
            a = award notice
            s = special notice
            i = intent to bundle
        """
        params: dict = {
            "limit": limit,
            "offset": offset,
        }

        if naics_code:
            params["ncode"] = naics_code
        if posted_from:
            params["postedFrom"] = posted_from
        if posted_to:
            params["postedTo"] = posted_to
        if ptype:
            params["ptype"] = ptype
        if keyword:
            params["title"] = keyword

        try:
            data = self._request("GET", OPPORTUNITIES_URL, params=params)
        except requests.HTTPError as e:
            log.warning(f"Opportunities search failed: {e}")
            return {"opportunitiesData": [], "totalRecords": 0}

        return data

    def search_opportunities_all_naics(
        self,
        naics_codes: list[str],
        ptypes: list[str] | None = None,
        posted_from: str = "",
        posted_to: str = "",
        max_per_query: int = 100,
    ) -> list[dict]:
        """Iterate across all NAICS codes and ptypes, deduplicating by noticeId.

        This is the most expensive operation — 1 request per NAICS x ptype combo.
        With 10 NAICS codes and 7 ptypes = 70 requests.
        """
        if ptypes is None:
            ptypes = ["p", "o", "r", "k", "a", "s", "i"]

        all_results = []
        seen_notice_ids = set()
        total_requests = len(naics_codes) * len(ptypes)
        request_num = 0

        for naics in naics_codes:
            for ptype in ptypes:
                request_num += 1
                print(
                    f"  [{request_num}/{total_requests}] NAICS {naics}, type={ptype}...",
                    end=" ",
                    flush=True,
                )

                data = self.search_opportunities(
                    naics_code=naics,
                    posted_from=posted_from,
                    posted_to=posted_to,
                    ptype=ptype,
                    limit=max_per_query,
                )
                records = data.get("opportunitiesData", [])
                new_count = 0
                for record in records:
                    notice_id = record.get("noticeId", "")
                    if notice_id and notice_id not in seen_notice_ids:
                        seen_notice_ids.add(notice_id)
                        all_results.append(record)
                        new_count += 1

                print(f"{len(records)} results, {new_count} new")
                time.sleep(1)  # rate limit courtesy

        return all_results

    @staticmethod
    def flatten_opportunity(opp: dict) -> dict:
        """Flatten opportunity into flat dict for CSV output."""
        # Point of contact extraction
        poc = {}
        poc_list = opp.get("pointOfContact", [])
        if isinstance(poc_list, list) and poc_list:
            poc = poc_list[0] if isinstance(poc_list[0], dict) else {}

        # Office address
        office = opp.get("officeAddress", {}) or {}

        # Place of performance (feeds geography scoring)
        pop = opp.get("placeOfPerformance", {}) or {}

        # Award value (feeds contract size scoring)
        award = opp.get("award", {}) or {}

        return {
            "notice_id": opp.get("noticeId", ""),
            "title": opp.get("title", ""),
            "solicitation_number": opp.get("solicitationNumber", ""),
            "type": opp.get("type", ""),
            "posted_date": opp.get("postedDate", ""),
            "response_deadline": opp.get("responseDeadLine", ""),
            "archive_date": opp.get("archiveDate", ""),
            "agency": opp.get("fullParentPathName", ""),
            "sub_agency": opp.get("subtierAgency", ""),
            "office": opp.get("officeAddress", {}).get("city", "") if isinstance(opp.get("officeAddress"), dict) else "",
            "naics_code": opp.get("naicsCode", ""),
            "classification_code": opp.get("classificationCode", ""),
            "set_aside": opp.get("typeOfSetAside", ""),
            "set_aside_description": opp.get("typeOfSetAsideDescription", ""),
            "pop_state": pop.get("state", {}).get("code", "") if isinstance(pop.get("state"), dict) else str(pop.get("state", "") or ""),
            "pop_city": pop.get("city", {}).get("name", "") if isinstance(pop.get("city"), dict) else str(pop.get("city", "") or ""),
            "pop_county": pop.get("county", {}).get("name", "") if isinstance(pop.get("county"), dict) else str(pop.get("county", "") or ""),
            "award_floor": award.get("floor", ""),
            "award_ceiling": award.get("ceiling", ""),
            "poc_name": poc.get("fullName", ""),
            "poc_email": poc.get("email", ""),
            "poc_phone": poc.get("phone", ""),
            "poc_type": poc.get("type", ""),
            "description": (opp.get("description", "") or "")[:500],
            "ui_link": opp.get("uiLink", ""),
        }
