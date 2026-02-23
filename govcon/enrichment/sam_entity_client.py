"""SAM.gov Entity Management API client for competitor intelligence.

Queries the Entity Management API v3 to find all registered federal contractors
by NAICS code, state, and business type. Returns vendor registration data
including size certifications, CAGE codes, contacts, and NAICS codes.

This is the COMPETITOR INTELLIGENCE source — shows who Newport is up against.

Rate limits: 1,000 requests/day with the same SAM_API_KEY used for Opportunities.
Max 10 records per page (synchronous). Async bulk extract supports up to 1M records.

Usage:
    from enrichment.sam_entity_client import SAMEntityClient
    client = SAMEntityClient()
    entities = client.search_entities(primary_naics="424410", state="FL")
"""

import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

ENTITY_URL = "https://api.sam.gov/entity-information/v3/entities"


class SAMEntityClient:
    """Wrapper around SAM.gov Entity Management API v3."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("SAM_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "SAM_API_KEY not set. Get a free key at https://sam.gov/content/entity-registration"
            )
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        self._request_count = 0
        self._daily_count = 0
        self._daily_limit = 1000

    def _request(self, params: dict) -> dict:
        """Make GET request with API key and retry on 429."""
        params["api_key"] = self.api_key

        if self._daily_count >= 900:
            log.warning(
                f"Approaching SAM.gov daily limit: {self._daily_count}/{self._daily_limit}"
            )
        if self._daily_count >= self._daily_limit:
            raise RuntimeError(
                f"SAM.gov daily limit reached ({self._daily_limit}). Wait until tomorrow."
            )

        for attempt in range(4):
            resp = self.session.get(ENTITY_URL, params=params, timeout=30)
            if resp.status_code == 429:
                wait = min(2 ** attempt * 5, 60)
                log.warning(f"Rate limited by SAM.gov Entity API, retrying in {wait}s...")
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

    def search_entities(
        self,
        primary_naics: str = "",
        naics_code: str = "",
        state: str = "",
        registration_status: str = "A",
        business_type: str = "",
        q: str = "",
        page: int = 0,
        page_size: int = 10,
    ) -> dict:
        """Search registered entities by NAICS, state, and business type.

        Args:
            primary_naics: 6-digit primary NAICS code (exact match)
            naics_code: Any NAICS on entity registration
            state: 2-letter state code for physical address
            registration_status: A=Active, E=Expired
            business_type: 2-char business type code
            q: Free text search
            page: Page number (0-indexed)
            page_size: Results per page (max 10 for synchronous)
        """
        params: dict = {
            "registrationStatus": registration_status,
            "includeSections": "entityRegistration,coreData,assertions,pointsOfContact",
            "page": page,
            "size": min(page_size, 10),
        }

        if primary_naics:
            params["primaryNaics"] = primary_naics
        if naics_code:
            params["naicsCode"] = naics_code
        if state:
            params["physicalAddressProvinceOrStateCode"] = state
        if business_type:
            params["businessTypeCode"] = business_type
        if q:
            params["q"] = q

        try:
            data = self._request(params)
        except requests.HTTPError as e:
            log.warning(f"Entity search failed: {e}")
            return {"entityData": [], "totalRecords": 0}

        return data

    def search_entities_all_pages(
        self,
        max_pages: int = 50,
        **kwargs,
    ) -> list[dict]:
        """Paginate through entity search results.

        SAM Entity API returns max 10 per page synchronous.
        Max 10,000 total records via pagination.
        """
        all_entities = []

        for page_num in range(max_pages):
            data = self.search_entities(page=page_num, **kwargs)
            entities = data.get("entityData", [])

            if not entities:
                break

            all_entities.extend(entities)
            total = data.get("totalRecords", 0)

            if page_num == 0:
                print(f"  SAM Entity API: {total} total records, fetching...")

            if page_num % 10 == 9:
                print(f"    Page {page_num + 1}: {len(all_entities)} fetched so far")

            if len(all_entities) >= total:
                break

            time.sleep(1)  # rate limit courtesy

        print(f"  Fetched {len(all_entities)} entities total")
        return all_entities

    def search_food_wholesalers_by_state(
        self,
        naics_codes: list[str],
        states: list[str],
        max_pages_per_query: int = 20,
    ) -> list[dict]:
        """Search for food wholesalers across multiple NAICS codes and states.

        Deduplicates by UEI across NAICS/state combinations.
        """
        all_entities = []
        seen_ueis = set()
        total_queries = len(naics_codes) * len(states)
        query_num = 0

        for naics in naics_codes:
            for state in states:
                query_num += 1
                print(
                    f"  [{query_num}/{total_queries}] NAICS {naics}, state={state}...",
                    end=" ",
                    flush=True,
                )

                entities = self.search_entities_all_pages(
                    primary_naics=naics,
                    state=state,
                    max_pages=max_pages_per_query,
                )

                new_count = 0
                for entity in entities:
                    reg = entity.get("entityRegistration", {})
                    uei = reg.get("ueiSAM", "")
                    if uei and uei not in seen_ueis:
                        seen_ueis.add(uei)
                        all_entities.append(entity)
                        new_count += 1

                print(f"{len(entities)} results, {new_count} new (deduped)")
                time.sleep(1)

        print(f"\n  Total unique entities: {len(all_entities)}")
        return all_entities

    @staticmethod
    def flatten_entity(entity: dict) -> dict:
        """Flatten entity response into flat dict for CSV output."""
        reg = entity.get("entityRegistration", {})
        core = entity.get("coreData", {})
        assertions = entity.get("assertions", {})
        poc = entity.get("pointsOfContact", {})

        # Physical address
        phys_addr = core.get("physicalAddress", {})

        # Government business POC
        gov_poc = poc.get("governmentBusinessPOC", {})

        # NAICS codes from assertions
        naics_list = assertions.get("naicsCode", {})
        primary_naics = ""
        all_naics = []
        if isinstance(naics_list, list):
            for n in naics_list:
                code = n.get("naicsCode", "")
                if code:
                    all_naics.append(code)
                if n.get("primaryInd", False):
                    primary_naics = code
        elif isinstance(naics_list, dict):
            primary_naics = naics_list.get("primaryNaicsCode", "")

        # Size certifications / business types
        biz_types = reg.get("businessTypes", [])
        if isinstance(biz_types, list):
            biz_type_str = ", ".join(
                bt.get("shortDescription", bt.get("businessTypeCode", ""))
                for bt in biz_types
                if isinstance(bt, dict)
            )
        else:
            biz_type_str = str(biz_types) if biz_types else ""

        return {
            "uei": reg.get("ueiSAM", ""),
            "cage_code": reg.get("cageCode", ""),
            "legal_business_name": reg.get("legalBusinessName", ""),
            "dba_name": reg.get("dbaName", ""),
            "registration_status": reg.get("registrationStatus", ""),
            "registration_date": reg.get("registrationDate", ""),
            "expiration_date": reg.get("registrationExpirationDate", ""),
            "primary_naics": primary_naics,
            "all_naics": "; ".join(all_naics),
            "business_types": biz_type_str,
            "physical_address_line1": phys_addr.get("addressLine1", ""),
            "physical_city": phys_addr.get("city", ""),
            "physical_state": phys_addr.get("stateOrProvinceCode", ""),
            "physical_zip": phys_addr.get("zipCode", ""),
            "physical_country": phys_addr.get("countryCode", ""),
            "poc_name": f"{gov_poc.get('firstName', '')} {gov_poc.get('lastName', '')}".strip(),
            "poc_title": gov_poc.get("title", ""),
            "poc_email": gov_poc.get("emailAddress", ""),
            "poc_phone": gov_poc.get("USPhone", ""),
        }
