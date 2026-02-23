"""USASpending.gov API client for federal spending data.

No API key required. All endpoints are POST with JSON body.
No daily rate limits — handles both market sizing AND individual award queries.

This is the correct source for historical contract award data (FPDS).
SAM.gov does NOT expose a contract awards REST API.

Supports:
  - Aggregate spending by NAICS / agency (market sizing)
  - Individual award search with dollar range, agency, state, award type filters
  - Period of performance filtering for expiring contract queries
  - Full pagination for large result sets

Usage:
    from enrichment.usaspending_client import USASpendingClient
    client = USASpendingClient()

    # Market sizing
    data = client.spending_by_naics(naics_require=["4244"], time_period_start="2023-10-01", time_period_end="2024-09-30")

    # Small contracts in FL
    awards = client.search_awards_all_pages(naics_require=["4244"], award_amount_min=10000, award_amount_max=350000, state="FL")
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

    def _request(self, path: str, body: dict | None = None, method: str = "POST") -> dict:
        """HTTP request with retry on server errors. POST by default, GET when body is None."""
        url = f"{BASE_URL}/{path.lstrip('/')}"

        for attempt in range(3):
            if method == "GET" or body is None:
                resp = self.session.get(url, timeout=60)
            else:
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

    # =========================================================================
    # Aggregate spending (market sizing)
    # =========================================================================

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

    # =========================================================================
    # Individual award search
    # =========================================================================

    def search_awards(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        recipient_search_text: str = "",
        award_amount_min: float | None = None,
        award_amount_max: float | None = None,
        agencies: list[str] | None = None,
        state: str = "",
        award_type_codes: list[str] | None = None,
        limit: int = 100,
        page: int = 1,
    ) -> dict:
        """Search individual awards with NAICS, dollar range, agency, and state filters.

        Args:
            naics_require: NAICS prefixes (e.g., ["4244"] matches all 4244xx)
            time_period_start: Start date YYYY-MM-DD
            time_period_end: End date YYYY-MM-DD
            award_amount_min: Minimum award amount in dollars
            award_amount_max: Maximum award amount in dollars
            agencies: List of subtier agency names (e.g., ["Federal Emergency Management Agency"])
            state: 2-letter state code for place of performance (e.g., "FL")
            award_type_codes: USASpending award type codes. Defaults to contracts only:
                A = BPA Call, B = Purchase Order, C = Delivery Order, D = Definitive Contract
                Excludes grants (02-06), loans (07-09), direct payments (10-11), insurance (14)
            limit: Results per page (max 100)
            page: Page number (1-indexed)
        """
        if award_type_codes is None:
            award_type_codes = ["A", "B", "C", "D"]

        filters: dict = {
            "time_period": [
                {"start_date": time_period_start, "end_date": time_period_end}
            ],
            "naics_codes": {"require": naics_require},
            "award_type_codes": award_type_codes,
        }

        if recipient_search_text:
            filters["recipient_search_text"] = [recipient_search_text]

        # Dollar range filter
        if award_amount_min is not None or award_amount_max is not None:
            bounds: dict = {}
            if award_amount_min is not None:
                bounds["lower_bound"] = award_amount_min
            if award_amount_max is not None:
                bounds["upper_bound"] = award_amount_max
            filters["award_amounts"] = [bounds]

        # Agency filter (subtier level)
        if agencies:
            filters["agencies"] = [
                {"type": "awarding", "tier": "subtier", "name": name}
                for name in agencies
            ]

        # State / place of performance filter
        if state:
            filters["place_of_performance_locations"] = [
                {"country": "USA", "state": state}
            ]

        body = {
            "filters": filters,
            "fields": [
                "Award ID",
                "Recipient Name",
                "Recipient DUNS",
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
                "Place of Performance State Code",
                "Place of Performance City Name",
                "recipient_id",
                "generated_internal_id",
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

    def search_awards_all_pages(
        self,
        max_pages: int = 10,
        **kwargs,
    ) -> list[dict]:
        """Paginate through award search results.

        Accepts all search_awards() parameters via kwargs.
        Returns flat list of award dicts.
        USASpending uses hasNext for pagination (no total count upfront).
        """
        all_results = []
        limit = kwargs.pop("limit", 100)

        for page_num in range(1, max_pages + 1):
            data = self.search_awards(limit=limit, page=page_num, **kwargs)
            results = data.get("results", [])

            if not results:
                break

            all_results.extend(results)
            has_next = data.get("page_metadata", {}).get("hasNext", False)

            if page_num == 1:
                print(f"  USASpending: {len(results)} results (page 1, hasNext={has_next})")
            else:
                print(f"  Page {page_num}: {len(results)} results (cumulative: {len(all_results)}, hasNext={has_next})")

            if not has_next or len(results) < limit:
                break

            time.sleep(0.5)  # courtesy delay

        return all_results

    def get_award_detail(self, generated_internal_id: str) -> dict:
        """Get full details for a single award including POP dates.

        The spending_by_award search endpoint does not return POP dates.
        This detail endpoint (GET) does.
        """
        try:
            return self._request(f"awards/{generated_internal_id}/", method="GET")
        except requests.HTTPError as e:
            log.warning(f"Award detail failed for {generated_internal_id}: {e}")
            return {}

    def search_expiring_awards(
        self,
        naics_require: list[str],
        months_ahead: int = 12,
        award_amount_min: float | None = None,
        award_amount_max: float | None = None,
        agencies: list[str] | None = None,
        state: str = "",
        max_pages: int = 10,
    ) -> list[dict]:
        """Find contracts with period of performance ending in the next N months.

        Two-phase approach because spending_by_award search doesn't return POP dates:
        1. Search for recent awards with food NAICS codes
        2. Fetch full details (including POP dates) for each award
        3. Filter by POP end date locally

        This is API-intensive (1 detail call per award) so max_pages should be kept low.
        """
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        today = datetime.now()
        future = today + relativedelta(months=months_ahead)
        lookback_start = today - relativedelta(years=3)

        # Phase 1: Search for recent awards (action date in last 3 years)
        all_awards = self.search_awards_all_pages(
            naics_require=naics_require,
            time_period_start=lookback_start.strftime("%Y-%m-%d"),
            time_period_end=today.strftime("%Y-%m-%d"),
            award_amount_min=award_amount_min,
            award_amount_max=award_amount_max,
            agencies=agencies,
            state=state,
            max_pages=max_pages,
        )

        if not all_awards:
            return []

        # Phase 2: Fetch details to get POP dates, filter by expiring window
        today_str = today.strftime("%Y-%m-%d")
        future_str = future.strftime("%Y-%m-%d")
        expiring = []
        checked = 0

        print(f"  Checking POP dates for {len(all_awards)} awards...")
        for award in all_awards:
            gen_id = award.get("generated_internal_id", "")
            if not gen_id:
                continue

            detail = self.get_award_detail(gen_id)
            if not detail:
                continue
            checked += 1

            # Extract POP end date from detail
            pop_end = detail.get("period_of_performance", {}).get("end_date", "")
            if pop_end and today_str <= pop_end <= future_str:
                # Merge POP dates into the search result
                award["Period of Performance Start Date"] = detail.get("period_of_performance", {}).get("start_date", "")
                award["Period of Performance Current End Date"] = pop_end
                award["_pop_source"] = "detail_api"
                expiring.append(award)

            if checked % 50 == 0:
                print(f"    Checked {checked}/{len(all_awards)}, found {len(expiring)} expiring so far")

            time.sleep(0.2)  # courtesy delay

        print(f"  Checked {checked} awards, found {len(expiring)} expiring (POP end between {today_str} and {future_str})")
        return expiring

    # =========================================================================
    # Enhanced endpoints (Build #9 — recipient, geography, trends, subawards)
    # =========================================================================

    def spending_by_recipient(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        limit: int = 50,
    ) -> list[dict]:
        """Aggregate federal spending by recipient (vendor) for given NAICS codes.

        Returns top vendors by total contract dollars — key for incumbent intelligence.
        """
        body = {
            "category": "recipient",
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
            data = self._request("search/spending_by_category/recipient", body)
        except requests.HTTPError as e:
            log.warning(f"Spending by recipient failed: {e}")
            return []

        return data.get("results", [])

    def spending_by_county(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        state: str = "",
        limit: int = 50,
    ) -> list[dict]:
        """Aggregate federal spending by county for given NAICS codes.

        Useful for mapping geographic density of food procurement.
        """
        body = {
            "category": "county",
            "filters": {
                "time_period": [
                    {"start_date": time_period_start, "end_date": time_period_end}
                ],
                "naics_codes": {"require": naics_require},
            },
            "limit": limit,
            "page": 1,
        }

        if state:
            body["filters"]["place_of_performance_locations"] = [
                {"country": "USA", "state": state}
            ]

        try:
            data = self._request("search/spending_by_category/county", body)
        except requests.HTTPError as e:
            log.warning(f"Spending by county failed: {e}")
            return []

        return data.get("results", [])

    def spending_by_geography(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        geo_layer: str = "state",
        scope: str = "place_of_performance",
    ) -> list[dict]:
        """Geographic distribution of spending (state or county level).

        Args:
            geo_layer: 'state' or 'county'
            scope: 'place_of_performance' or 'recipient_location'
        """
        body = {
            "filters": {
                "time_period": [
                    {"start_date": time_period_start, "end_date": time_period_end}
                ],
                "naics_codes": {"require": naics_require},
            },
            "geo_layer": geo_layer,
            "scope": scope,
        }

        try:
            data = self._request("search/spending_by_geography", body)
        except requests.HTTPError as e:
            log.warning(f"Spending by geography failed: {e}")
            return []

        return data.get("results", [])

    def recipient_profile(self, recipient_id: str) -> dict:
        """Get detailed profile for a specific recipient (vendor).

        recipient_id comes from award search results (recipient_id field).
        Returns company details, total awards, agencies served, etc.
        """
        try:
            return self._request(f"recipient/{recipient_id}/", method="GET")
        except requests.HTTPError as e:
            log.warning(f"Recipient profile failed for {recipient_id}: {e}")
            return {}

    def new_awards_over_time(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        group: str = "month",
        state: str = "",
    ) -> list[dict]:
        """Get spending trends over time — monthly or quarterly.

        Args:
            group: 'month', 'quarter', or 'fiscal_year'
            state: 2-letter state code for place of performance filter
        """
        filters: dict = {
            "time_period": [
                {"start_date": time_period_start, "end_date": time_period_end}
            ],
            "naics_codes": {"require": naics_require},
        }
        if state:
            filters["place_of_performance_locations"] = [
                {"country": "USA", "state": state}
            ]

        body = {
            "filters": filters,
            "group": group,
        }

        try:
            data = self._request("search/spending_over_time", body)
        except requests.HTTPError as e:
            log.warning(f"Spending over time failed: {e}")
            return []

        return data.get("results", [])

    def search_subawards(
        self,
        naics_require: list[str],
        time_period_start: str,
        time_period_end: str,
        state: str = "",
        limit: int = 100,
        page: int = 1,
    ) -> dict:
        """Search subaward data — shows subcontracting relationships.

        Reveals which primes are subbing out food distribution work.
        """
        filters: dict = {
            "time_period": [
                {"start_date": time_period_start, "end_date": time_period_end}
            ],
            "naics_codes": {"require": naics_require},
        }
        if state:
            filters["place_of_performance_locations"] = [
                {"country": "USA", "state": state}
            ]

        body = {
            "filters": filters,
            "fields": [
                "sub_awardee_or_recipient_legal",
                "sub_legal_entity_country_name",
                "sub_legal_entity_city_name",
                "sub_legal_entity_state_code",
                "subaward_amount",
                "prime_award_recipient_name",
                "prime_award_amount",
                "awarding_agency_name",
                "awarding_sub_agency_name",
                "subaward_number",
                "subaward_description",
                "sub_action_date",
                "prime_award_generated_internal_id",
            ],
            "limit": limit,
            "page": page,
            "sort": "subaward_amount",
            "order": "desc",
        }

        try:
            data = self._request("subawards/", body)
        except requests.HTTPError as e:
            log.warning(f"Subaward search failed: {e}")
            return {"results": [], "page_metadata": {"total": 0}}

        return data

    @staticmethod
    def flatten_subaward(sub: dict) -> dict:
        """Flatten subaward response into flat dict for CSV output."""
        return {
            "subawardee_name": sub.get("sub_awardee_or_recipient_legal", ""),
            "subawardee_city": sub.get("sub_legal_entity_city_name", ""),
            "subawardee_state": sub.get("sub_legal_entity_state_code", ""),
            "subaward_amount": sub.get("subaward_amount", 0),
            "subaward_description": (sub.get("subaward_description", "") or "")[:500],
            "subaward_date": sub.get("sub_action_date", ""),
            "prime_vendor": sub.get("prime_award_recipient_name", ""),
            "prime_award_amount": sub.get("prime_award_amount", 0),
            "awarding_agency": sub.get("awarding_agency_name", ""),
            "awarding_sub_agency": sub.get("awarding_sub_agency_name", ""),
        }

    @staticmethod
    def flatten_award(award: dict) -> dict:
        """Flatten USASpending award response into a flat dict for CSV output.

        USASpending spending_by_award returns fields using their display names
        as keys (e.g., "Award ID", "Recipient Name").
        """
        return {
            "award_id": award.get("Award ID", ""),
            "recipient_name": award.get("Recipient Name", ""),
            "recipient_duns": award.get("Recipient DUNS", ""),
            "awarding_agency": award.get("Awarding Agency", ""),
            "awarding_sub_agency": award.get("Awarding Sub Agency", ""),
            "award_amount": award.get("Award Amount", 0),
            "total_outlays": award.get("Total Outlays", 0),
            "description": (award.get("Description", "") or "")[:500],
            "naics_code": award.get("NAICS Code", ""),
            "naics_description": award.get("NAICS Description", ""),
            "pop_start_date": award.get("Period of Performance Start Date", ""),
            "pop_end_date": award.get("Period of Performance Current End Date", ""),
            "contract_type": award.get("Contract Award Type", ""),
            "pop_state": award.get("Place of Performance State Code", ""),
            "pop_city": award.get("Place of Performance City Name", ""),
            "generated_internal_id": award.get("generated_internal_id", ""),
        }
