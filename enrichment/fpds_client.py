"""FPDS (Federal Procurement Data System) client for competition density analysis.

Wraps the `fpds` Python library which parses the FPDS ATOM feed with
auto-pagination and XML-to-JSON conversion. No API key required.

Key metric: NUMBER_OF_OFFERS_RECEIVED per award — direct measure of competition
density per NAICS/agency. Low avg offers = easy entry. High = crowded.

Fields USASpending doesn't surface cleanly:
  - Vendor CAGE codes
  - Detailed small business certifications (8(a), HUBZone, WOSB, SDVOSB)
  - Contract modification history
  - Number of offers received per award

Usage:
    from enrichment.fpds_client import FPDSClient
    client = FPDSClient()
    records = client.search_contracts(naics_code="424410", date_range="[2024/01/01, 2025/01/01]")
"""

import asyncio
import logging
import time

from fpds import fpdsRequest

log = logging.getLogger(__name__)


def _get_nested(record: dict, path: str, default=""):
    """Safely extract a value from a deeply nested fpds dict using __ path."""
    return record.get(path, default)


class FPDSClient:
    """Wrapper around the fpds library for FPDS ATOM feed queries."""

    def __init__(self, thread_count: int = 5):
        self.thread_count = thread_count
        self._request_count = 0
        self._record_count = 0

    @property
    def stats(self) -> dict:
        return {
            "queries": self._request_count,
            "records_fetched": self._record_count,
        }

    def search_contracts(
        self,
        naics_code: str = "",
        vendor_state: str = "",
        pop_state: str = "",
        date_range: str = "",
        amount_range: str = "",
        agency_code: str = "",
        psc_code: str = "",
        max_records: int = 5000,
    ) -> list[dict]:
        """Search FPDS contract transactions.

        Args:
            naics_code: 6-digit NAICS code (e.g., "424410")
            vendor_state: 2-letter vendor home state (e.g., "FL")
            pop_state: Place of performance state name (e.g., "Florida")
            date_range: Signed date range in FPDS format "[YYYY/MM/DD, YYYY/MM/DD]"
            amount_range: Obligated amount range "[min, max]" (e.g., "[25000, 999999999]")
            agency_code: 4-digit agency code (e.g., "1540" for BOP)
            psc_code: Product/service code (e.g., "8905")
            max_records: Cap on total records returned (default 5000)

        Returns:
            List of raw fpds record dicts.
        """
        kwargs = {}

        if naics_code:
            kwargs["PRINCIPAL_NAICS_CODE"] = naics_code
        if vendor_state:
            kwargs["VENDOR_ADDRESS_STATE_CODE"] = vendor_state
        if pop_state:
            kwargs["POP_STATE_NAME"] = pop_state
        if date_range:
            kwargs["SIGNED_DATE"] = date_range
        if amount_range:
            kwargs["OBLIGATED_AMOUNT"] = amount_range
        if agency_code:
            kwargs["AGENCY_CODE"] = agency_code
        if psc_code:
            kwargs["PRODUCT_OR_SERVICE_CODE"] = psc_code

        if not kwargs:
            raise ValueError("At least one search parameter is required")

        try:
            req = fpdsRequest(thread_count=self.thread_count, **kwargs)
        except Exception as e:
            log.warning(f"FPDS query setup failed: {e}")
            return []

        try:
            records = asyncio.run(req.data())
        except Exception as e:
            log.warning(f"FPDS fetch failed: {e}")
            return []

        self._request_count += 1
        self._record_count += len(records)

        if len(records) > max_records:
            log.info(f"Capping results from {len(records)} to {max_records}")
            records = records[:max_records]

        return records

    def search_contracts_multi_naics(
        self,
        naics_codes: list[str],
        date_range: str = "",
        amount_range: str = "",
        vendor_state: str = "",
        pop_state: str = "",
        max_records_per_naics: int = 5000,
    ) -> list[dict]:
        """Search across multiple NAICS codes, deduplicating by contract PIID + mod.

        Returns:
            Deduplicated list of fpds records.
        """
        all_records = []
        seen_keys = set()
        total = len(naics_codes)

        for i, naics in enumerate(naics_codes):
            print(f"  [{i + 1}/{total}] NAICS {naics}...", end=" ", flush=True)

            records = self.search_contracts(
                naics_code=naics,
                date_range=date_range,
                amount_range=amount_range,
                vendor_state=vendor_state,
                pop_state=pop_state,
                max_records=max_records_per_naics,
            )

            new_count = 0
            for rec in records:
                piid = _get_nested(rec, "content__award__awardID__awardContractID__PIID")
                mod = _get_nested(rec, "content__award__awardID__awardContractID__modNumber")
                agency = _get_nested(rec, "content__award__awardID__awardContractID__agencyID")
                key = f"{piid}|{mod}|{agency}"

                if key not in seen_keys:
                    seen_keys.add(key)
                    all_records.append(rec)
                    new_count += 1

            print(f"{len(records)} records, {new_count} new")
            time.sleep(0.5)  # courtesy delay

        return all_records

    @staticmethod
    def flatten_contract(rec: dict) -> dict:
        """Flatten an FPDS record into a flat dict for CSV output.

        Extracts the key fields for competition density analysis:
        - Contract ID, agency, vendor, dollar values
        - NUMBER_OF_OFFERS_RECEIVED (the critical competition metric)
        - Small business certifications
        - Place of performance
        """
        g = lambda path, default="": _get_nested(rec, path, default)

        # Small business certifications — collect active ones
        certs = []
        cert_map = {
            "8(a)": "content__award__vendor__vendorSiteDetails__vendorCertifications__isSBACertified8AProgramParticipant",
            "HUBZone": "content__award__vendor__vendorSiteDetails__vendorCertifications__isSBACertifiedHUBZone",
            "SDB": "content__award__vendor__vendorSiteDetails__vendorCertifications__isSelfCertifiedSmallDisadvantagedBusiness",
        }
        socio_map = {
            "Small Business": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__isSmallBusiness",
            "WOSB": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__isWomenOwnedSmallBusiness",
            "SDVOSB": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__isServiceRelatedDisabledVeteranOwnedBusiness",
            "Veteran Owned": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__isVeteranOwned",
            "Women Owned": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__isWomenOwned",
            "Minority Owned": "content__award__vendor__vendorSiteDetails__vendorSocioEconomicIndicators__minorityOwned__isMinorityOwned",
        }

        for label, path in {**cert_map, **socio_map}.items():
            val = g(path, "false")
            if val == "true" or val is True:
                certs.append(label)

        # Parse offers received
        offers_raw = g("content__award__competition__numberOfOffersReceived", "")
        try:
            offers = int(offers_raw) if offers_raw else None
        except (ValueError, TypeError):
            offers = None

        # Parse obligated amount
        amount_raw = g("content__award__dollarValues__obligatedAmount", "0")
        try:
            amount = float(amount_raw)
        except (ValueError, TypeError):
            amount = 0.0

        total_value_raw = g("content__award__totalDollarValues__totalBaseAndAllOptionsValue", "0")
        try:
            total_value = float(total_value_raw)
        except (ValueError, TypeError):
            total_value = 0.0

        return {
            "piid": g("content__award__awardID__awardContractID__PIID"),
            "mod_number": g("content__award__awardID__awardContractID__modNumber"),
            "agency_code": g("content__award__awardID__awardContractID__agencyID"),
            "agency_name": g("content__award__awardID__awardContractID__agencyID__name"),
            "department": g("content__award__purchaserInformation__contractingOfficeAgencyID__departmentName"),
            "contracting_office": g("content__award__purchaserInformation__contractingOfficeID__name"),
            "naics_code": g("content__award__productOrServiceInformation__principalNAICSCode"),
            "naics_description": g("content__award__productOrServiceInformation__principalNAICSCode__description"),
            "psc_code": g("content__award__productOrServiceInformation__productOrServiceCode"),
            "psc_description": g("content__award__productOrServiceInformation__productOrServiceCode__description"),
            "description": g("content__award__contractData__descriptionOfContractRequirement"),
            "action_type": g("content__award__contractData__contractActionType__description"),
            "contract_pricing": g("content__award__contractData__typeOfContractPricing__description"),
            "obligated_amount": amount,
            "total_base_and_options": total_value,
            "signed_date": g("content__award__relevantContractDates__signedDate"),
            "effective_date": g("content__award__relevantContractDates__effectiveDate"),
            "completion_date": g("content__award__relevantContractDates__currentCompletionDate"),
            "ultimate_completion_date": g("content__award__relevantContractDates__ultimateCompletionDate"),
            "offers_received": offers,
            "extent_competed": g("content__award__competition__extentCompeted__description"),
            "set_aside": g("content__award__competition__typeOfSetAside__description"),
            "solicitation_procedures": g("content__award__competition__solicitationProcedures__description"),
            "vendor_name": g("content__award__vendor__vendorHeader__vendorName"),
            "vendor_uei": g("content__award__vendor__vendorSiteDetails__entityIdentifiers__vendorUEIInformation__UEI"),
            "vendor_cage": g("content__award__vendor__vendorSiteDetails__entityIdentifiers__cageCode"),
            "vendor_state": g("content__award__vendor__vendorSiteDetails__vendorLocation__state"),
            "vendor_city": g("content__award__vendor__vendorSiteDetails__vendorLocation__city"),
            "vendor_size": g("content__award__vendor__contractingOfficerBusinessSizeDetermination__description"),
            "vendor_certifications": ", ".join(certs) if certs else "",
            "pop_state": g("content__award__placeOfPerformance__principalPlaceOfPerformance__stateCode"),
            "pop_city": g("content__award__placeOfPerformance__placeOfPerformanceZIPCode__city"),
            "pop_county": g("content__award__placeOfPerformance__placeOfPerformanceZIPCode__county"),
        }
