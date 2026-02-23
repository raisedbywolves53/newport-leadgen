"""Bid/No-Bid scoring framework for Newport Wholesalers government opportunities.

Evaluates federal/state/local contract opportunities on 9 weighted factors,
producing a 0-100 score and a recommendation (Strong Bid / Bid / Review / No-Bid).

Five factors auto-score from opportunity data; four default to conservative values
and can be overridden when manual assessment is available.

Scoring matrix calibrated for Newport Wholesalers:
  - 30-year South Florida grocery wholesaler
  - NAICS 424410/424450/424490 (grocery merchant wholesalers)
  - Targeting $10K-$350K micro and small contracts
  - New to government contracting (no prior past performance)
  - Delivery radius: South FL > FL statewide > Southeast US

Usage:
    # Score a single opportunity
    scorer = BidNoBidScorer()
    result = scorer.score(opportunity_dict)

    # Batch score from CSV
    python scoring/bid_no_bid.py --csv data/final/govt_opportunity_pipeline_*.csv
    python scoring/bid_no_bid.py --csv FILE --overrides '{"past_performance": 100}'
    python scoring/bid_no_bid.py --csv FILE --top 10
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
_govcon = _project_root / "govcon"
if str(_govcon) not in sys.path:
    sys.path.insert(0, str(_govcon))

import pandas as pd

log = logging.getLogger(__name__)

CONFIG_PATH = _project_root / "config" / "government_contracts.json"

# ---------------------------------------------------------------------------
# Scoring constants
# ---------------------------------------------------------------------------

SCORING_FACTORS = {
    "naics_alignment":       {"weight": 0.15, "auto": True,  "label": "NAICS Alignment"},
    "geography":             {"weight": 0.15, "auto": True,  "label": "Geography"},
    "contract_size":         {"weight": 0.10, "auto": True,  "label": "Contract Size"},
    "competition_level":     {"weight": 0.10, "auto": True,  "label": "Competition Level"},
    "past_performance":      {"weight": 0.15, "auto": False, "label": "Past Performance Req"},
    "evaluation_criteria":   {"weight": 0.10, "auto": False, "label": "Evaluation Criteria Fit"},
    "relationship_status":   {"weight": 0.10, "auto": False, "label": "Relationship Status"},
    "timeline_feasibility":  {"weight": 0.10, "auto": True,  "label": "Timeline Feasibility"},
    "strategic_value":       {"weight": 0.05, "auto": False, "label": "Strategic Value"},
}

# Verify weights sum to 1.0
_weight_sum = sum(f["weight"] for f in SCORING_FACTORS.values())
assert abs(_weight_sum - 1.0) < 1e-9, f"Scoring weights must sum to 1.0, got {_weight_sum}"

DECISION_THRESHOLDS = [
    (80, "Strong Bid", "green"),
    (65, "Bid",        "blue"),
    (50, "Review",     "yellow"),
    (0,  "No-Bid",     "red"),
]

# Conservative defaults for manual factors (Newport is new to gov contracting)
MANUAL_DEFAULTS = {
    "past_performance":    100,  # Target no-past-perf-required opportunities
    "evaluation_criteria":  50,  # Assume best-value equal weight
    "relationship_status":  25,  # No relationship but accessible
    "strategic_value":      50,  # Moderate strategic benefit assumed
}

# ---------------------------------------------------------------------------
# Newport-specific reference data
# ---------------------------------------------------------------------------

PRIMARY_NAICS = {"424410", "424450", "424490"}

ADJACENT_NAICS = {
    "722310",   # Food Service Contractors
    "424420",   # Packaged Frozen Food
    "424430",   # Dairy Product
    "424440",   # Poultry and Poultry Product
    "424460",   # Fish and Seafood
    "424470",   # Meat and Meat Product
    "424480",   # Fresh Fruit and Vegetable
}

# 311xxx food manufacturing codes are also adjacent
FOOD_MFG_PREFIX = "311"

SOUTH_FL_COUNTIES = {
    "MIAMI-DADE", "MIAMI DADE", "MIAMIDADE", "DADE",
    "BROWARD",
    "PALM BEACH", "PALMBEACH",
}

SOUTHEAST_STATES = {"GA", "SC", "NC", "AL", "TN", "MS", "LA"}
MID_ATLANTIC_STATES = {"VA", "DC", "MD"}
EXTENDED_STATES = {"TX", "AR", "KY"}

# ---------------------------------------------------------------------------
# Scorer class
# ---------------------------------------------------------------------------


class BidNoBidScorer:
    """Score government opportunities for Newport Wholesalers.

    Evaluates each opportunity on 9 weighted factors (0-100 each),
    producing a composite score and a bid/no-bid recommendation with
    human-readable reasoning.

    Example:
        scorer = BidNoBidScorer()
        result = scorer.score(opportunity_data)
        # result = {
        #     "total_score": 78,
        #     "recommendation": "Bid",
        #     "recommendation_color": "blue",
        #     "factor_scores": {
        #         "naics_alignment": {"score": 100, "weight": 0.15, ...},
        #         ...
        #     },
        #     "reasoning": "Strong NAICS match (424410 primary). ..."
        # }

        # Batch scoring
        results = scorer.score_batch(opportunities_list)
    """

    def __init__(self, config_path: str | Path | None = None):
        """Initialize scorer with config from government_contracts.json.

        Args:
            config_path: Path to config file. Defaults to config/government_contracts.json
                         relative to project root.
        """
        self._config_path = Path(config_path) if config_path else CONFIG_PATH
        self._config = self._load_config()
        self._primary_naics = self._build_primary_naics()
        self._adjacent_naics = self._build_adjacent_naics()
        self._target_states = set(self._config.get("target_states", []))
        log.info(
            "BidNoBidScorer initialized: %d primary NAICS, %d adjacent NAICS, %d target states",
            len(self._primary_naics),
            len(self._adjacent_naics),
            len(self._target_states),
        )

    # ---- Config loading ---------------------------------------------------

    def _load_config(self) -> dict:
        """Load government_contracts.json config."""
        if not self._config_path.exists():
            log.warning("Config file not found at %s, using built-in defaults", self._config_path)
            return {}
        try:
            return json.loads(self._config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            log.error("Failed to load config: %s", exc)
            return {}

    def _build_primary_naics(self) -> set[str]:
        """Build primary NAICS set from config, falling back to hardcoded."""
        # Always include Newport's three core NAICS regardless of config
        codes = set(PRIMARY_NAICS)
        return codes

    def _build_adjacent_naics(self) -> set[str]:
        """Build adjacent NAICS set from config primary + secondary."""
        codes = set(ADJACENT_NAICS)
        # Add all primary codes from config that aren't Newport's core three
        config_primary = self._config.get("naics_codes", {}).get("primary", {})
        for code in config_primary:
            if code not in PRIMARY_NAICS:
                codes.add(code)
        # Add all secondary codes from config (311xxx food manufacturing)
        config_secondary = self._config.get("naics_codes", {}).get("secondary", {})
        for code in config_secondary:
            codes.add(code)
        return codes

    # ---- Individual factor scoring (each returns 0-100) --------------------

    def _score_naics_alignment(self, opp: dict) -> tuple[int, str]:
        """Score NAICS code alignment.

        Returns:
            (score, reasoning) where score is 0-100.
            100: Primary exact match (424410, 424450, 424490)
             75: Adjacent (722310, 424420-424480, 311xxx)
             25: Tangentially related
              0: No match
        """
        naics = self._extract_naics(opp)
        if not naics:
            log.debug("NAICS missing, defaulting to 25 (tangential)")
            return 25, "NAICS code not provided; scored conservatively as tangential"

        if naics in self._primary_naics:
            return 100, f"Primary NAICS exact match ({naics})"

        if naics in self._adjacent_naics:
            return 75, f"Adjacent NAICS match ({naics})"

        # Check 311xxx prefix (food manufacturing family)
        if naics.startswith(FOOD_MFG_PREFIX):
            return 75, f"Food manufacturing NAICS ({naics})"

        # Check if at least in 42xxxx wholesale trade
        if naics.startswith("42"):
            return 25, f"Wholesale trade NAICS but not food-specific ({naics})"

        return 0, f"NAICS {naics} does not match Newport's food wholesale focus"

    def _score_geography(self, opp: dict) -> tuple[int, str]:
        """Score geographic alignment.

        Returns:
            (score, reasoning) where score is 0-100.
            100: South FL (Miami-Dade, Broward, Palm Beach)
             80: FL statewide
             60: Southeast (GA, SC, NC, AL, TN, MS, LA)
             40: Mid-Atlantic (VA, DC, MD)
             20: National/other US
              0: International
        """
        state = self._extract_state(opp)
        county = self._extract_county(opp)
        pop_city = self._extract_city(opp)

        # Check for international indicators
        country = str(opp.get("country", "") or opp.get("pop_country", "") or "").upper().strip()
        if country and country not in ("US", "USA", "UNITED STATES", ""):
            return 0, f"International location ({country})"

        # Check for South Florida by county
        if county:
            county_upper = county.upper().strip()
            for sfl_county in SOUTH_FL_COUNTIES:
                if sfl_county in county_upper:
                    return 100, f"South Florida ({county}, FL)"

        # Check for South Florida by city name heuristic
        if state == "FL" and pop_city:
            city_upper = pop_city.upper().strip()
            south_fl_cities = {
                "MIAMI", "FORT LAUDERDALE", "FT LAUDERDALE", "WEST PALM BEACH",
                "BOCA RATON", "HIALEAH", "HOLLYWOOD", "POMPANO BEACH",
                "CORAL SPRINGS", "PEMBROKE PINES", "DEERFIELD BEACH",
                "HOMESTEAD", "DORAL", "SUNRISE", "PLANTATION",
                "DAVIE", "MIRAMAR", "DELRAY BEACH", "BOYNTON BEACH",
                "CORAL GABLES", "AVENTURA", "COCONUT CREEK",
                "LAUDERHILL", "TAMARAC", "MARGATE", "NORTH MIAMI",
                "KEY BISCAYNE", "MIAMI BEACH", "MIAMI GARDENS",
                "NORTH LAUDERDALE", "RIVIERA BEACH", "LAKE WORTH",
                "JUPITER", "WELLINGTON", "ROYAL PALM BEACH",
            }
            if city_upper in south_fl_cities:
                return 100, f"South Florida ({pop_city}, FL)"

        # Florida statewide
        if state == "FL":
            return 80, "Florida statewide"

        # Southeast US
        if state in SOUTHEAST_STATES:
            return 60, f"Southeast US ({state})"

        # Mid-Atlantic
        if state in MID_ATLANTIC_STATES:
            return 40, f"Mid-Atlantic ({state})"

        # Extended target states
        if state in EXTENDED_STATES:
            return 30, f"Extended target state ({state})"

        # Other known US state
        if state and len(state) == 2 and state.isalpha():
            return 20, f"National/other US state ({state})"

        # No geographic info
        if not state:
            return 20, "No geographic data; scored as national/unknown"

        return 20, f"Other US location ({state})"

    def _score_contract_size(self, opp: dict) -> tuple[int, str]:
        """Score contract value fit.

        Returns:
            (score, reasoning) where score is 0-100.
            100: $25K-$75K (ideal first-year target)
             80: $75K-$150K
             60: $150K-$350K
             40: $10K-$25K (small but builds past performance)
             20: >$350K (stretch)
              0: <$10K (not worth effort)
        """
        amount = self._extract_amount(opp)
        if amount is None:
            return 60, "Contract value unknown; scored conservatively as mid-range"

        if amount < 10_000:
            return 0, f"Contract value ${amount:,.0f} is below $10K threshold"
        if amount <= 25_000:
            return 40, f"Small contract (${amount:,.0f}) but builds past performance"
        if amount <= 75_000:
            return 100, f"Ideal sweet spot (${amount:,.0f}) for first-year targeting"
        if amount <= 150_000:
            return 80, f"Strong value (${amount:,.0f}) within capability range"
        if amount <= 350_000:
            return 60, f"Mid-range (${amount:,.0f}), within simplified acquisition"
        return 20, f"Large contract (${amount:,.0f}), may exceed current capacity"

    def _score_competition_level(self, opp: dict) -> tuple[int, str]:
        """Score expected competition level.

        Returns:
            (score, reasoning) where score is 0-100.
            100: Sole-source or single bid expected
             80: 2-3 expected bidders
             60: 4-6 expected bidders
             40: 7-10 expected bidders
             20: >10 expected bidders
              0: Incumbent-locked/wired
        """
        set_aside = str(opp.get("set_aside", "") or opp.get("type_of_set_aside", "") or "").lower()
        num_offers = self._extract_int(
            opp.get("num_offers")
            or opp.get("offers_received")
            or opp.get("number_of_offers_received")
        )
        competition_type = str(
            opp.get("competition_type", "")
            or opp.get("extent_competed", "")
            or opp.get("type_of_contract_pricing", "")
            or ""
        ).lower()
        solicitation_type = str(opp.get("type", "") or opp.get("ptype", "") or "").lower()

        # Detect sole-source indicators
        sole_source_keywords = [
            "sole source", "sole-source", "solesource",
            "not competed", "not available for competition",
            "only one source", "j&a", "justification",
        ]
        is_sole_source = any(kw in competition_type for kw in sole_source_keywords)
        is_sole_source = is_sole_source or any(kw in set_aside for kw in sole_source_keywords)

        if is_sole_source:
            return 100, "Sole-source or non-competitive procurement"

        # Detect incumbent-locked indicators
        incumbent_keywords = ["follow-on", "follow on", "bridge", "incumbent"]
        is_incumbent_locked = any(
            kw in str(opp.get("title", "")).lower() or kw in competition_type
            for kw in incumbent_keywords
        )
        if is_incumbent_locked and not num_offers:
            return 0, "Appears incumbent-locked (follow-on/bridge contract)"

        # Score by number of offers if available
        if num_offers is not None:
            if num_offers <= 1:
                return 100, f"Single bid ({num_offers} offer received)"
            if num_offers <= 3:
                return 80, f"Low competition ({num_offers} bidders)"
            if num_offers <= 6:
                return 60, f"Moderate competition ({num_offers} bidders)"
            if num_offers <= 10:
                return 40, f"High competition ({num_offers} bidders)"
            return 20, f"Very high competition ({num_offers} bidders)"

        # Heuristic from set-aside type
        favorable_set_asides = [
            "small", "sba", "8(a)", "hubzone", "sdvosb", "wosb", "edwosb",
            "total small business", "partial small business",
        ]
        has_set_aside = any(kw in set_aside for kw in favorable_set_asides)

        # Sources sought / pre-solicitation typically have less competition data
        if solicitation_type in ("sources sought", "presol", "ss", "p"):
            return 60, "Pre-solicitation/sources sought; competition level unclear"

        if has_set_aside:
            return 60, f"Small business set-aside ({set_aside.strip()}); moderate competition expected"

        # Default: assume moderate competition
        return 60, "Competition level unknown; scored conservatively as moderate"

    def _score_timeline_feasibility(self, opp: dict) -> tuple[int, str]:
        """Score timeline feasibility based on response deadline.

        Returns:
            (score, reasoning) where score is 0-100.
            100: 30+ days until deadline
             80: 15-30 days
             60: 7-14 days
             30: 3-7 days
              0: <3 days or already passed
        """
        days = self._extract_days_until_deadline(opp)
        if days is None:
            return 60, "No deadline provided; scored conservatively as 7-14 days"

        if days < 0:
            return 0, f"Deadline has passed ({abs(days):.0f} days ago)"
        if days < 3:
            return 0, f"Only {days:.0f} days remaining; insufficient response time"
        if days < 7:
            return 30, f"{days:.0f} days remaining; very tight timeline"
        if days < 15:
            return 60, f"{days:.0f} days remaining; feasible but tight"
        if days < 30:
            return 80, f"{days:.0f} days remaining; adequate response time"
        return 100, f"{days:.0f} days remaining; comfortable timeline"

    # ---- Core scoring engine ----------------------------------------------

    def score(
        self,
        opportunity: dict[str, Any],
        overrides: dict[str, int] | None = None,
    ) -> dict[str, Any]:
        """Score a single opportunity on all 9 factors.

        Args:
            opportunity: Flat dict of opportunity data (from SAM.gov API,
                         CSV import, or manual entry). Expected keys include
                         naics_code, pop_state, award_amount, set_aside,
                         days_until_deadline, etc.
            overrides:   Manual scores (0-100) for any factor. Overrides
                         auto-scored and manual-default values alike.

        Returns:
            dict with keys:
                total_score (float): Weighted composite score 0-100
                recommendation (str): "Strong Bid" / "Bid" / "Review" / "No-Bid"
                recommendation_color (str): green / blue / yellow / red
                factor_scores (dict): Per-factor breakdown with score, weight,
                                      weighted_contribution, auto flag, reasoning
                reasoning (str): Human-readable summary of the scoring decision
        """
        overrides = overrides or {}
        factor_scores = {}
        reasoning_parts = []

        # --- Auto-scored factors ---
        auto_scorers = {
            "naics_alignment":      self._score_naics_alignment,
            "geography":            self._score_geography,
            "contract_size":        self._score_contract_size,
            "competition_level":    self._score_competition_level,
            "timeline_feasibility": self._score_timeline_feasibility,
        }

        for factor_name, scorer_fn in auto_scorers.items():
            meta = SCORING_FACTORS[factor_name]
            if factor_name in overrides:
                raw_score = self._clamp_score(overrides[factor_name])
                reason = f"Manual override ({raw_score})"
                log.debug("Factor %s: override=%d", factor_name, raw_score)
            else:
                raw_score, reason = scorer_fn(opportunity)
                raw_score = self._clamp_score(raw_score)
                log.debug("Factor %s: auto=%d — %s", factor_name, raw_score, reason)

            weighted = raw_score * meta["weight"]
            factor_scores[factor_name] = {
                "score": raw_score,
                "weight": meta["weight"],
                "weighted_contribution": round(weighted, 2),
                "auto": factor_name not in overrides,
                "label": meta["label"],
                "reasoning": reason,
            }
            reasoning_parts.append(f"{meta['label']}: {reason} ({raw_score}/100)")

        # --- Manual factors (default to conservative values) ---
        for factor_name, default_val in MANUAL_DEFAULTS.items():
            meta = SCORING_FACTORS[factor_name]
            if factor_name in overrides:
                raw_score = self._clamp_score(overrides[factor_name])
                reason = f"Manual override ({raw_score})"
                is_auto = False
            else:
                raw_score = default_val
                reason = f"Default conservative estimate ({raw_score})"
                is_auto = False

            log.debug("Factor %s: %s=%d", factor_name, "override" if factor_name in overrides else "default", raw_score)

            weighted = raw_score * meta["weight"]
            factor_scores[factor_name] = {
                "score": raw_score,
                "weight": meta["weight"],
                "weighted_contribution": round(weighted, 2),
                "auto": is_auto,
                "label": meta["label"],
                "reasoning": reason,
            }
            reasoning_parts.append(f"{meta['label']}: {reason} ({raw_score}/100)")

        # --- Compute weighted total ---
        total_score = sum(fs["weighted_contribution"] for fs in factor_scores.values())
        total_score = round(total_score, 1)

        recommendation, rec_color = self._get_decision(total_score)

        # --- Build reasoning summary ---
        opp_title = opportunity.get("title", "Untitled opportunity")[:80]
        opp_id = (
            opportunity.get("notice_id")
            or opportunity.get("solicitation_number")
            or "N/A"
        )
        reasoning_header = (
            f"Opportunity: {opp_title} ({opp_id})\n"
            f"Score: {total_score}/100 -> {recommendation}\n\n"
        )
        reasoning = reasoning_header + "\n".join(f"  - {r}" for r in reasoning_parts)

        log.info(
            "Scored %s: %.1f/100 (%s) — %s",
            opp_id, total_score, recommendation, opp_title,
        )

        return {
            "total_score": total_score,
            "recommendation": recommendation,
            "recommendation_color": rec_color,
            "factor_scores": factor_scores,
            "reasoning": reasoning,
        }

    def score_batch(
        self,
        opportunities: list[dict[str, Any]],
        overrides: dict[str, int] | None = None,
        overrides_map: dict[str, dict[str, int]] | None = None,
    ) -> list[dict[str, Any]]:
        """Score a batch of opportunities.

        Args:
            opportunities: List of flat opportunity dicts.
            overrides:     Global overrides applied to ALL opportunities.
            overrides_map: Dict mapping notice_id -> per-opportunity overrides.
                           Per-opportunity overrides take precedence over global.

        Returns:
            List of dicts, each containing the original opportunity data plus:
                bid_score (float): Total composite score
                bid_decision (str): Recommendation label
                bid_reasoning (str): Human-readable reasoning
                _score_result (dict): Full score result (removed before CSV export)
        """
        overrides = overrides or {}
        overrides_map = overrides_map or {}
        results = []

        log.info("Batch scoring %d opportunities", len(opportunities))

        for opp in opportunities:
            opp_id = (
                opp.get("notice_id")
                or opp.get("solicitation_number")
                or ""
            )
            # Merge global overrides with per-opportunity overrides
            merged_overrides = {**overrides}
            if opp_id in overrides_map:
                merged_overrides.update(overrides_map[opp_id])

            result = self.score(opp, overrides=merged_overrides)
            results.append({
                **opp,
                "bid_score": result["total_score"],
                "bid_decision": result["recommendation"],
                "bid_reasoning": result["reasoning"],
                "_score_result": result,
            })

        # Sort by score descending
        results.sort(key=lambda x: x.get("bid_score", 0), reverse=True)

        # Summary log
        decisions = {}
        for r in results:
            d = r.get("bid_decision", "Unknown")
            decisions[d] = decisions.get(d, 0) + 1
        log.info(
            "Batch complete: %s",
            ", ".join(f"{k}={v}" for k, v in sorted(decisions.items())),
        )

        return results

    # ---- Decision thresholds ----------------------------------------------

    @staticmethod
    def _get_decision(score: float) -> tuple[str, str]:
        """Map a 0-100 score to a decision label and color."""
        for threshold, label, color in DECISION_THRESHOLDS:
            if score >= threshold:
                return label, color
        return "No-Bid", "red"

    # ---- Data extraction helpers ------------------------------------------
    # These handle the variety of field names from SAM.gov, USASpending,
    # CSV imports, and manual entry. Missing data returns None.

    @staticmethod
    def _extract_naics(opp: dict) -> str | None:
        """Extract NAICS code from opportunity data."""
        raw = (
            opp.get("naics_code")
            or opp.get("naicsCode")
            or opp.get("naics")
            or opp.get("NAICS")
            or ""
        )
        raw = str(raw).strip()
        # Strip description if present (e.g., "424410 - General Line Grocery")
        match = re.match(r"^(\d{4,6})", raw)
        return match.group(1) if match else None

    @staticmethod
    def _extract_state(opp: dict) -> str | None:
        """Extract state abbreviation from opportunity data."""
        raw = (
            opp.get("pop_state")
            or opp.get("state")
            or opp.get("place_of_performance_state")
            or opp.get("pop_state_code")
            or opp.get("recipient_state_code")
            or ""
        )
        raw = str(raw).upper().strip()
        if len(raw) == 2 and raw.isalpha():
            return raw
        # Try to extract from office/agency location
        office = str(opp.get("office", "") or "").upper()
        # Look for two-letter state code at end, e.g., "NAVSUP FLC JACKSONVILLE, FL"
        state_match = re.search(r"\b([A-Z]{2})\s*$", office)
        if state_match:
            return state_match.group(1)
        return raw if raw else None

    @staticmethod
    def _extract_county(opp: dict) -> str | None:
        """Extract county from opportunity data."""
        raw = (
            opp.get("pop_county")
            or opp.get("county")
            or opp.get("place_of_performance_county")
            or ""
        )
        return str(raw).strip() if raw else None

    @staticmethod
    def _extract_city(opp: dict) -> str | None:
        """Extract city from opportunity data."""
        raw = (
            opp.get("pop_city")
            or opp.get("city")
            or opp.get("place_of_performance_city")
            or ""
        )
        return str(raw).strip() if raw else None

    def _extract_amount(self, opp: dict) -> float | None:
        """Extract contract dollar amount from opportunity data."""
        for field in [
            "award_amount", "contract_value", "total_obligation",
            "award_ceiling", "estimated_value", "contract_size_est",
            "total_obligated_amount", "award_base_value",
        ]:
            val = opp.get(field)
            result = self._parse_float(val)
            if result is not None and result > 0:
                return result
        return None

    def _extract_days_until_deadline(self, opp: dict) -> float | None:
        """Extract or compute days until response deadline."""
        # Direct field
        days = self._parse_float(opp.get("days_until_deadline"))
        if days is not None:
            return days

        # Compute from deadline date
        for field in [
            "response_deadline", "responseDeadLine", "close_date",
            "response_date", "archive_date", "deadline",
        ]:
            date_str = opp.get(field)
            if not date_str:
                continue
            parsed = self._parse_date(str(date_str))
            if parsed:
                delta = (parsed - datetime.now()).total_seconds() / 86400
                return round(delta, 1)

        return None

    @staticmethod
    def _extract_int(val: Any) -> int | None:
        """Safely extract an integer value."""
        if val is None or val == "":
            return None
        try:
            result = int(float(val))
            return result if result >= 0 else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_float(val: Any) -> float | None:
        """Safely parse a float value, handling NaN and empty strings."""
        if val is None or val == "":
            return None
        try:
            result = float(val)
            if pd.isna(result):
                return None
            return result
        except (ValueError, TypeError):
            # Try stripping currency symbols
            if isinstance(val, str):
                cleaned = re.sub(r"[,$\s]", "", val)
                try:
                    return float(cleaned)
                except (ValueError, TypeError):
                    return None
            return None

    @staticmethod
    def _parse_date(date_str: str) -> datetime | None:
        """Parse a date string in common formats."""
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S%z",
            "%m/%d/%Y",
            "%m/%d/%y",
            "%m-%d-%Y",
            "%Y%m%d",
            "%d-%b-%Y",
        ]
        date_str = date_str.strip()
        for fmt in formats:
            try:
                return datetime.strptime(date_str[:len(date_str)], fmt)
            except (ValueError, IndexError):
                continue
        return None

    @staticmethod
    def _clamp_score(score: int | float) -> int:
        """Clamp a score to the 0-100 range."""
        return max(0, min(100, int(round(score))))

    # ---- Formatting -------------------------------------------------------

    def format_scorecard(self, result: dict, opportunity: dict) -> str:
        """Format a CLI-printable scorecard for one opportunity.

        Args:
            result: Output from self.score()
            opportunity: The original opportunity dict

        Returns:
            Multi-line string with formatted scorecard
        """
        lines = []
        title = str(opportunity.get("title", "Unknown"))[:70]
        sol_num = (
            opportunity.get("solicitation_number")
            or opportunity.get("notice_id")
            or "N/A"
        )
        agency = opportunity.get("agency", opportunity.get("department_name", "N/A"))
        state = self._extract_state(opportunity) or "N/A"
        amount = self._extract_amount(opportunity)
        amount_str = f"${amount:,.0f}" if amount else "Unknown"

        lines.append(f"{'=' * 78}")
        lines.append(f"  {title}")
        lines.append(f"  Sol#: {sol_num}  |  Agency: {agency}  |  State: {state}  |  Value: {amount_str}")
        lines.append(f"{'=' * 78}")

        factor_scores = result["factor_scores"]
        for factor_name, meta in SCORING_FACTORS.items():
            fs = factor_scores[factor_name]
            score_val = fs["score"]
            weight = fs["weight"]
            weighted = fs["weighted_contribution"]
            auto_tag = "auto" if fs["auto"] else "manual"
            # Visual bar: 20 chars wide, filled proportionally
            filled = int(score_val / 100 * 20)
            bar = "#" * filled + "." * (20 - filled)
            lines.append(
                f"  {meta['label']:25s} [{bar}] {score_val:3d}/100  "
                f"(wt {weight:.0%}, +{weighted:5.1f})  [{auto_tag}]"
            )
            # Show reasoning indented
            lines.append(f"  {'':25s}   {fs['reasoning']}")

        lines.append(f"  {'-' * 74}")
        total = result["total_score"]
        rec = result["recommendation"]
        lines.append(f"  TOTAL SCORE: {total:.1f}/100  |  RECOMMENDATION: {rec}")
        lines.append("")

        return "\n".join(lines)

    def format_summary(self, scored_results: list[dict]) -> str:
        """Format a summary of batch scoring results.

        Args:
            scored_results: Output from self.score_batch()

        Returns:
            Multi-line string with scoring summary
        """
        lines = []
        decisions = {}
        for item in scored_results:
            d = item.get("bid_decision", "Unknown")
            decisions[d] = decisions.get(d, 0) + 1

        lines.append(f"\n{'=' * 78}")
        lines.append(f"SCORING SUMMARY ({len(scored_results)} opportunities)")
        lines.append(f"{'=' * 78}")

        for _, label, color in DECISION_THRESHOLDS:
            count = decisions.get(label, 0)
            pct = (count / max(len(scored_results), 1)) * 100
            lines.append(f"  {label:15s}: {count:3d}  ({pct:5.1f}%)")

        if scored_results:
            avg_score = sum(s.get("bid_score", 0) for s in scored_results) / len(scored_results)
            max_score = max(s.get("bid_score", 0) for s in scored_results)
            min_score = min(s.get("bid_score", 0) for s in scored_results)
            lines.append(f"\n  Average score: {avg_score:.1f}")
            lines.append(f"  Range: {min_score:.1f} - {max_score:.1f}")

            # Top 3 preview
            lines.append(f"\n  Top 3:")
            for item in scored_results[:3]:
                title = str(item.get("title", "Unknown"))[:50]
                score = item.get("bid_score", 0)
                dec = item.get("bid_decision", "?")
                lines.append(f"    {score:5.1f} [{dec:11s}]  {title}")

        lines.append("")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """CLI entry point for bid/no-bid scoring."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(
        description="Bid/No-Bid scoring for Newport government contract opportunities",
        epilog=(
            "Examples:\n"
            "  python scoring/bid_no_bid.py --csv data/final/govt_opportunity_pipeline_*.csv\n"
            "  python scoring/bid_no_bid.py --csv FILE --overrides '{\"past_performance\": 100}'\n"
            "  python scoring/bid_no_bid.py --csv FILE --top 10\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--csv", required=True,
        help="Path to opportunity CSV (from contract_scanner, daily_monitor, or manual)",
    )
    parser.add_argument(
        "--overrides", default="{}",
        help='JSON string of manual factor overrides (0-100), e.g. \'{"past_performance": 100}\'',
    )
    parser.add_argument(
        "--top", type=int, default=0,
        help="Show only top N scored opportunities (default: show all)",
    )
    parser.add_argument(
        "--output", default="",
        help="Output CSV path (default: auto-generated in data/final/)",
    )

    args = parser.parse_args()

    # --- Load CSV ---
    csv_path = Path(args.csv)
    if not csv_path.exists():
        # Try glob expansion for wildcard paths
        import glob
        matches = sorted(glob.glob(str(csv_path)))
        if matches:
            csv_path = Path(matches[-1])  # Most recent
            log.info("Glob matched: %s", csv_path)
        else:
            print(f"ERROR: CSV file not found: {args.csv}")
            sys.exit(1)

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} opportunities from {csv_path.name}")

    # --- Parse overrides ---
    try:
        overrides = json.loads(args.overrides)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in --overrides: {exc}")
        sys.exit(1)

    # --- Score ---
    scorer = BidNoBidScorer()
    opps = df.to_dict("records")
    scored = scorer.score_batch(opps, overrides=overrides)

    # --- Print scorecards ---
    display = scored[:args.top] if args.top else scored
    for item in display:
        result = item.get("_score_result")
        if result:
            print(scorer.format_scorecard(result, item))

    # --- Print summary ---
    print(scorer.format_summary(scored))

    # --- Save output CSV ---
    # Remove internal fields before saving
    for item in scored:
        item.pop("_score_result", None)
        # Truncate reasoning for CSV (keep first line only)
        reasoning = item.get("bid_reasoning", "")
        if reasoning:
            first_line = reasoning.split("\n")[0]
            item["bid_reasoning"] = first_line

    scored_df = pd.DataFrame(scored)

    if args.output:
        out_path = Path(args.output)
    else:
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        out_dir = _project_root / "data" / "final"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"govt_scored_opportunities_{date_str}.csv"

    scored_df.to_csv(out_path, index=False)
    print(f"\nSaved scored results to {out_path}")


if __name__ == "__main__":
    main()
