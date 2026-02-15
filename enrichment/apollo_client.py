"""Apollo.io API client for lead enrichment.

Budget-conscious design:
  - People Search is FREE (0 credits) — find decision makers by company/title
  - Email reveal costs 1 email credit (unlimited on paid plans under Fair Use)
  - Phone reveal costs ~8 mobile credits — OFF by default (we already have
    business phones from Google Places)

Usage:
    from enrichment.apollo_client import ApolloClient
    client = ApolloClient(api_key="...")
    people = client.search_people(domain="example.com", titles=["Owner"])
    enriched = client.enrich_person(first_name="John", last_name="Doe", domain="example.com")
"""

import logging
import os
import time
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

BASE_URL = "https://api.apollo.io/api/v1"

# Decision-maker titles by ICP type
DECISION_MAKER_TITLES = {
    "real_estate_agents": ["Owner", "Broker", "Managing Broker", "Team Lead", "Realtor"],
    "property_managers": ["Owner", "Operations Manager", "Maintenance Director", "Property Manager"],
    "home_inspectors": ["Owner", "Chief Inspector", "Lead Inspector"],
    "insurance_agents": ["Agent", "Owner", "Agency Owner", "Principal"],
    "home_builders": ["Owner", "President", "VP Operations", "General Manager"],
    "adjacent_trades": ["Owner", "General Manager", "Operations Manager"],
    "commercial_properties": ["Facility Manager", "Property Manager", "Owner", "Operations Manager"],
}


def domain_from_url(url) -> str:
    """Extract clean domain from a URL (strip www. prefix)."""
    if not url or not isinstance(url, str):
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        host = urlparse(url).hostname or ""
        return host.removeprefix("www.")
    except Exception:
        return ""


class ApolloClient:
    """Thin wrapper around Apollo.io REST API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("APOLLO_API_KEY", "")
        if not self.api_key:
            raise ValueError("APOLLO_API_KEY not set")
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        })
        self._request_count = 0
        self._credits_used = 0

    # --- low-level helpers ---

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an API request with retry on 429 rate limits."""
        url = f"{BASE_URL}/{path.lstrip('/')}"
        for attempt in range(4):
            resp = self.session.request(method, url, timeout=30, **kwargs)
            if resp.status_code == 429:
                wait = min(2 ** attempt * 5, 60)
                log.warning(f"Rate limited, retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            self._request_count += 1
            return resp.json()
        resp.raise_for_status()
        return {}

    @property
    def stats(self) -> dict:
        return {"requests": self._request_count, "credits_used": self._credits_used}

    # --- People Search (FREE — 0 credits) ---

    def search_people(
        self,
        organization_name: str = "",
        domain: str = "",
        titles: list[str] | None = None,
        per_page: int = 5,
    ) -> list[dict]:
        """Search for people at a company by title. FREE — no credits consumed.

        Returns list of person dicts with: name, title, linkedin_url, etc.
        Email/phone NOT included — must call enrich_person() to reveal.
        """
        body: dict = {"per_page": per_page, "page": 1}
        if domain:
            body["q_organization_domains"] = domain
        if organization_name and not domain:
            body["q_organization_name"] = organization_name
        if titles:
            body["person_titles"] = titles

        if not domain and not organization_name:
            return []

        try:
            data = self._request("POST", "mixed_people/api_search", json=body)
        except requests.HTTPError as e:
            log.warning(f"People search failed: {e}")
            return []

        return data.get("people", [])

    # --- People Enrichment (1 email credit per reveal) ---

    def enrich_person(
        self,
        first_name: str = "",
        last_name: str = "",
        domain: str = "",
        organization_name: str = "",
        apollo_id: str = "",
    ) -> dict | None:
        """Enrich a single person to get their email. Costs 1 email credit.

        Phone enrichment is intentionally disabled to save mobile credits.
        """
        body: dict = {}
        if apollo_id:
            body["id"] = apollo_id
        else:
            if first_name:
                body["first_name"] = first_name
            if last_name:
                body["last_name"] = last_name
            if domain:
                body["domain"] = domain
            if organization_name:
                body["organization_name"] = organization_name

        if not body:
            return None

        try:
            data = self._request("POST", "people/match", json=body)
        except requests.HTTPError as e:
            log.warning(f"Person enrichment failed: {e}")
            return None

        person = data.get("person")
        if person:
            self._credits_used += 1
        return person

    def bulk_enrich_people(self, details: list[dict]) -> list[dict | None]:
        """Enrich up to 10 people in one request. Each match costs 1 email credit.

        Each item in details should have keys like: first_name, last_name, domain, etc.
        """
        if not details:
            return []

        # Apollo bulk_match accepts max 10 per request
        results = []
        for i in range(0, len(details), 10):
            batch = details[i:i + 10]
            try:
                data = self._request("POST", "people/bulk_match", json={"details": batch})
            except requests.HTTPError as e:
                log.warning(f"Bulk enrichment failed: {e}")
                results.extend([None] * len(batch))
                continue

            credits = data.get("credits_consumed", len(batch))
            self._credits_used += credits

            matches = data.get("matches", [])
            # Pad if fewer results than expected
            while len(matches) < len(batch):
                matches.append(None)
            results.extend(matches)

            if i + 10 < len(details):
                time.sleep(1)  # rate limit courtesy

        return results

    # --- Organization Enrichment (1 credit) ---

    def enrich_organization(self, domain: str = "", name: str = "") -> dict | None:
        """Enrich a company to get employee count, revenue, industry, etc."""
        params = {}
        if domain:
            params["domain"] = domain
        if name:
            params["organization_name"] = name
        if not params:
            return None

        try:
            data = self._request("GET", "organizations/enrich", params=params)
        except requests.HTTPError as e:
            log.warning(f"Org enrichment failed: {e}")
            return None

        return data.get("organization")

    # --- Convenience: find decision maker + email in one shot ---

    def find_decision_maker(
        self,
        company_name: str,
        website: str = "",
        icp_type: str = "",
    ) -> dict:
        """Find a decision maker at a company and reveal their email.

        Returns dict with: first_name, last_name, title, email, linkedin_url
        Costs: 0 credits (search) + 1 email credit (enrichment) = 1 credit total
        """
        domain = domain_from_url(website)
        titles = DECISION_MAKER_TITLES.get(icp_type, ["Owner", "General Manager"])

        # Step 1: FREE search for people with matching titles
        people = self.search_people(
            organization_name=company_name,
            domain=domain,
            titles=titles,
            per_page=3,
        )

        if not people:
            # Broaden search — try without title filter
            people = self.search_people(
                organization_name=company_name,
                domain=domain,
                per_page=3,
            )

        if not people:
            return {"first_name": "", "last_name": "", "title": "", "email": "", "linkedin_url": ""}

        # Pick the best match — prefer someone with has_email=True
        best = people[0]
        for p in people:
            if p.get("has_email"):
                best = p
                break

        first_name = best.get("first_name", "")
        title = best.get("title", "")
        apollo_id = best.get("id", "")

        # Search results obfuscate last_name — must enrich to reveal
        # Only spend a credit if the person has an email
        if not best.get("has_email") and not apollo_id:
            return {"first_name": first_name, "last_name": "", "title": title, "email": "", "linkedin_url": ""}

        # Step 2: Enrich by Apollo ID to reveal full details (1 credit)
        enriched = self.enrich_person(apollo_id=apollo_id)

        if not enriched:
            return {"first_name": first_name, "last_name": "", "title": title, "email": "", "linkedin_url": ""}

        return {
            "first_name": enriched.get("first_name", first_name) or first_name,
            "last_name": enriched.get("last_name", ""),
            "title": enriched.get("title", title) or title,
            "email": enriched.get("email", ""),
            "linkedin_url": enriched.get("linkedin_url", ""),
        }
