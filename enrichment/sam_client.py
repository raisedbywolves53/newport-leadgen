"""SAM.gov API client for federal contract intelligence.

Wraps two SAM.gov APIs behind a single client:
  - Contract Awards API — historical and active contract data
  - Opportunities API — active solicitations, pre-solicitations, sources sought

Rate limits: 1,000 requests/day with a free API key.
Key mitigations:
  - Contract Awards batches up to 100 NAICS codes per request (tilde-delimited)
  - Opportunities only takes 1 NAICS at a time, so iterate + deduplicate
  - Cache layer in contract_scanner.py prevents redundant calls within 24hrs

Usage:
    from enrichment.sam_client import SAMClient
    client = SAMClient(api_key="...")
    awards = client.search_contract_awards(naics_codes=["424410", "424420"])
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

# Contract Awards (FPDS) endpoint
AWARDS_URL = "https://api.sam.gov/opportunities/v1/search"

# Contract Opportunities endpoint
OPPORTUNITIES_URL = "https://api.sam.gov/opportunities/v2/search"


class SAMClient:
    """Thin wrapper around SAM.gov Contract Awards and Opportunities APIs."""

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
    # Contract Awards API (FPDS data via SAM.gov)
    # =========================================================================

    def search_contract_awards(
        self,
        naics_codes: list[str] | None = None,
        date_signed_from: str = "",
        date_signed_to: str = "",
        current_completion_from: str = "",
        current_completion_to: str = "",
        awardee_name: str = "",
        modification_number: str | None = None,
        dollars_obligated_min: float | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """Search contract awards (FPDS). Returns one page of results.

        SAM accepts up to 100 NAICS codes tilde-delimited in one request,
        so we batch all food wholesale codes together.

        Date format: MM/dd/yyyy
        """
        params: dict = {
            "limit": limit,
            "offset": offset,
        }

        if naics_codes:
            # Tilde-delimited list — SAM.gov supports up to 100 per request
            params["ncode"] = "~".join(naics_codes)

        if date_signed_from:
            params["postedFrom"] = date_signed_from
        if date_signed_to:
            params["postedTo"] = date_signed_to
        if current_completion_from:
            params["rdlfrom"] = current_completion_from
        if current_completion_to:
            params["rdlto"] = current_completion_to
        if awardee_name:
            params["dba"] = awardee_name
        if modification_number is not None:
            params["modNumber"] = modification_number
        if dollars_obligated_min is not None:
            params["dollarAmount"] = str(int(dollars_obligated_min))

        try:
            data = self._request("GET", AWARDS_URL, params=params)
        except requests.HTTPError as e:
            log.warning(f"Contract awards search failed: {e}")
            return {"opportunitiesData": [], "totalRecords": 0}

        return data

    def search_contract_awards_all_pages(
        self,
        max_pages: int = 10,
        **kwargs,
    ) -> list[dict]:
        """Paginate through contract awards, merging results across pages."""
        all_results = []
        limit = kwargs.pop("limit", 100)

        for page in range(max_pages):
            offset = page * limit
            data = self.search_contract_awards(limit=limit, offset=offset, **kwargs)
            records = data.get("opportunitiesData", [])

            if not records:
                break

            all_results.extend(records)
            total = data.get("totalRecords", 0)

            if page == 0:
                print(f"  SAM Awards: {len(records)} results, ~{total} total available")
            else:
                print(f"  Page {page + 1}: {len(records)} results (cumulative: {len(all_results)})")

            if len(all_results) >= total or len(records) < limit:
                break

            time.sleep(1)  # rate limit courtesy

        return all_results

    @staticmethod
    def flatten_award(award: dict) -> dict:
        """Flatten nested SAM award response into a flat dict for CSV output."""
        # SAM.gov opportunity/award fields vary — extract safely
        return {
            "piid": award.get("solicitationNumber", "") or award.get("noticeId", ""),
            "title": award.get("title", ""),
            "vendor_name": award.get("awardee", {}).get("name", "") if isinstance(award.get("awardee"), dict) else "",
            "vendor_uei": award.get("awardee", {}).get("ueiSAM", "") if isinstance(award.get("awardee"), dict) else "",
            "agency": award.get("fullParentPathName", "") or award.get("department", ""),
            "sub_agency": award.get("subtierAgency", ""),
            "date_signed": award.get("postedDate", ""),
            "current_completion_date": award.get("responseDeadLine", ""),
            "ultimate_completion_date": award.get("archiveDate", ""),
            "dollars_obligated": award.get("award", {}).get("amount", "") if isinstance(award.get("award"), dict) else "",
            "base_and_all_options": award.get("award", {}).get("amount", "") if isinstance(award.get("award"), dict) else "",
            "extent_competed": award.get("typeOfSetAsideDescription", ""),
            "number_of_offers": award.get("award", {}).get("number", "") if isinstance(award.get("award"), dict) else "",
            "set_aside": award.get("typeOfSetAside", ""),
            "naics_code": award.get("naicsCode", ""),
            "naics_description": award.get("naicsDescription", ""),
            "description": (award.get("description", "") or "")[:500],
            "psc_code": award.get("classificationCode", ""),
            "modification_number": award.get("modificationNumber", ""),
            "type": award.get("type", ""),
            "notice_id": award.get("noticeId", ""),
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
            o = solicitation (combined synopsis/solicitation)
            r = sources sought
            k = combined synopsis/solicitation
            s = special notice
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
        With 10 NAICS codes and 4 ptypes = 40 requests.
        """
        if ptypes is None:
            ptypes = ["p", "o", "r", "k"]

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
            "poc_name": poc.get("fullName", ""),
            "poc_email": poc.get("email", ""),
            "poc_phone": poc.get("phone", ""),
            "poc_type": poc.get("type", ""),
            "description": (opp.get("description", "") or "")[:500],
            "ui_link": opp.get("uiLink", ""),
        }
