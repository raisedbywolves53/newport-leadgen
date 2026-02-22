"""Bid/No-Bid scoring framework for federal contract opportunities.

Scores opportunities on 9 weighted factors to produce a 0-100 score and
a decision label (Strong Bid / Bid / Review / No-Bid).

Five factors auto-score from opportunity data; four default to 3 (neutral)
and can be overridden when manual assessment is available.

Usage:
    python scoring/bid_scorer.py --csv data/final/govt_opportunity_pipeline_*.csv
    python scoring/bid_scorer.py --csv FILE --overrides '{"past_performance": 1}'
"""

import argparse
import json
import logging
import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import pandas as pd

log = logging.getLogger(__name__)

CONFIG_PATH = _project_root / "config" / "government_contracts.json"

# ── Scoring weights (must sum to 1.0) ────────────────────────────────────

SCORING_FACTORS = {
    "naics_alignment":       {"weight": 0.15, "auto": True},
    "geography":             {"weight": 0.15, "auto": True},
    "contract_size":         {"weight": 0.10, "auto": True},
    "competition_level":     {"weight": 0.10, "auto": True},
    "past_performance":      {"weight": 0.15, "auto": False},
    "evaluation_criteria":   {"weight": 0.10, "auto": False},
    "relationship_status":   {"weight": 0.10, "auto": False},
    "timeline_feasibility":  {"weight": 0.10, "auto": True},
    "strategic_value":       {"weight": 0.05, "auto": False},
}

DECISION_THRESHOLDS = [
    (80, "Strong Bid", "green"),
    (65, "Bid",        "blue"),
    (50, "Review",     "yellow"),
    (0,  "No-Bid",     "red"),
]


# ── Auto-scoring functions (each returns 1, 3, or 5) ────────────────────

def score_naics_alignment(naics_code: str, config: dict) -> int:
    """5=primary NAICS, 3=secondary, 1=unrelated."""
    if not naics_code:
        return 3
    primary = config.get("naics_codes", {}).get("primary", {})
    secondary = config.get("naics_codes", {}).get("secondary", {})
    if naics_code in primary:
        return 5
    if naics_code in secondary:
        return 3
    return 1


def score_geography(state: str, config: dict) -> int:
    """5=FL (home state), 3=target state, 1=other."""
    if not state:
        return 3
    state = state.upper().strip()
    if state == "FL":
        return 5
    target_states = config.get("target_states", [])
    if state in target_states:
        return 3
    return 1


def score_contract_size(amount, config: dict) -> int:
    """5=$10K-$350K (simplified acquisition), 3=borderline, 1=outside range."""
    if amount is None or amount == "" or (isinstance(amount, float) and pd.isna(amount)):
        return 3  # unknown
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return 3
    sa = config.get("simplified_acquisition", {})
    sa_min = sa.get("small_contract_min", 10000)
    sa_max = sa.get("small_contract_max", 350000)
    if sa_min <= amount <= sa_max:
        return 5
    if 5000 <= amount < sa_min or sa_max < amount <= 500000:
        return 3
    return 1


def score_competition_level(set_aside: str, num_offers=None) -> int:
    """5=small biz set-aside + low offers, 3=moderate, 1=crowded."""
    is_small_biz = False
    if set_aside:
        sa_lower = set_aside.lower()
        is_small_biz = any(kw in sa_lower for kw in [
            "small", "sba", "8(a)", "hubzone", "sdvosb", "wosb", "edwosb",
            "total small business", "partial small business",
        ])

    if num_offers is not None:
        try:
            num_offers = int(num_offers)
        except (ValueError, TypeError):
            num_offers = None

    if is_small_biz and (num_offers is None or num_offers <= 3):
        return 5
    if is_small_biz or (num_offers is not None and num_offers <= 5):
        return 3
    if num_offers is not None and num_offers > 8:
        return 1
    return 3


def score_timeline_feasibility(days_until_deadline) -> int:
    """5=30+ days, 3=14-30 days, 1=<14 days."""
    if days_until_deadline is None or days_until_deadline == "":
        return 3
    try:
        days = float(days_until_deadline)
    except (ValueError, TypeError):
        return 3
    if pd.isna(days):
        return 3
    if days >= 30:
        return 5
    if days >= 14:
        return 3
    return 1


# ── Core scoring engine ──────────────────────────────────────────────────

def score_opportunity(
    opportunity: dict,
    overrides: dict | None = None,
    config: dict | None = None,
) -> dict:
    """Score a single opportunity. Returns full breakdown + total + decision.

    Args:
        opportunity: Flat dict from SAMClient.flatten_opportunity()
        overrides: Manual factor scores (1-5) for non-auto factors
        config: government_contracts.json config; loaded if not provided

    Returns:
        dict with keys: factors (per-factor breakdown), total_score (0-100),
        decision, decision_color
    """
    if config is None:
        config = json.loads(CONFIG_PATH.read_text())

    overrides = overrides or {}

    factors = {}

    # Auto-scored factors
    factors["naics_alignment"] = score_naics_alignment(
        opportunity.get("naics_code", ""), config
    )
    factors["geography"] = score_geography(
        opportunity.get("pop_state", "") or opportunity.get("office", ""),
        config,
    )
    factors["contract_size"] = score_contract_size(
        opportunity.get("award_amount") or opportunity.get("contract_size_est"),
        config,
    )
    factors["competition_level"] = score_competition_level(
        opportunity.get("set_aside", ""),
        opportunity.get("num_offers") or opportunity.get("offers_received"),
    )
    factors["timeline_feasibility"] = score_timeline_feasibility(
        opportunity.get("days_until_deadline"),
    )

    # Manual factors (default 3, overridable)
    for manual_factor in ["past_performance", "evaluation_criteria",
                          "relationship_status", "strategic_value"]:
        factors[manual_factor] = overrides.get(manual_factor, 3)

    # Allow overriding auto factors too
    for factor_name in factors:
        if factor_name in overrides:
            factors[factor_name] = overrides[factor_name]

    # Compute weighted total: sum(score * weight) / 5 * 100
    total = 0.0
    for factor_name, score in factors.items():
        weight = SCORING_FACTORS[factor_name]["weight"]
        total += score * weight

    total_score = round(total / 5.0 * 100, 1)

    decision, decision_color = get_decision(total_score)

    return {
        "factors": factors,
        "total_score": total_score,
        "decision": decision,
        "decision_color": decision_color,
    }


def score_opportunities_batch(
    opportunities: list[dict],
    overrides_map: dict | None = None,
    config: dict | None = None,
) -> list[dict]:
    """Score a batch of opportunities.

    Args:
        opportunities: List of flat opportunity dicts
        overrides_map: Dict mapping notice_id -> overrides dict
        config: Shared config (loaded once if not provided)

    Returns:
        List of dicts, each containing the opportunity + scoring result
    """
    if config is None:
        config = json.loads(CONFIG_PATH.read_text())

    overrides_map = overrides_map or {}
    results = []

    for opp in opportunities:
        opp_id = opp.get("notice_id", opp.get("solicitation_number", ""))
        overrides = overrides_map.get(opp_id, {})
        result = score_opportunity(opp, overrides=overrides, config=config)
        results.append({
            **opp,
            "bid_score": result["total_score"],
            "bid_decision": result["decision"],
            "_score_result": result,
        })

    return results


def get_decision(score: float) -> tuple[str, str]:
    """Map a 0-100 score to a decision label and color."""
    for threshold, label, color in DECISION_THRESHOLDS:
        if score >= threshold:
            return label, color
    return "No-Bid", "red"


def format_scorecard(result: dict, opportunity: dict) -> str:
    """Format a CLI-printable scorecard for one opportunity."""
    lines = []
    title = opportunity.get("title", "Unknown")[:60]
    sol_num = opportunity.get("solicitation_number", "N/A")

    lines.append(f"{'='*70}")
    lines.append(f"  {title}")
    lines.append(f"  Solicitation: {sol_num}")
    lines.append(f"{'='*70}")

    factors = result["factors"]
    for factor_name, score_val in factors.items():
        weight = SCORING_FACTORS[factor_name]["weight"]
        auto_tag = "auto" if SCORING_FACTORS[factor_name]["auto"] else "manual"
        bar = "#" * score_val + "." * (5 - score_val)
        weighted = score_val * weight / 5.0 * 100
        lines.append(
            f"  {factor_name:25s} [{bar}] {score_val}/5  "
            f"(wt {weight:.0%}, contrib {weighted:5.1f})  [{auto_tag}]"
        )

    lines.append(f"  {'-'*66}")
    total = result["total_score"]
    decision = result["decision"]
    lines.append(f"  TOTAL SCORE: {total:.1f}/100  |  DECISION: {decision}")
    lines.append("")

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Bid/No-Bid scoring for federal contract opportunities"
    )
    parser.add_argument(
        "--csv", required=True,
        help="Path to opportunity pipeline CSV (from contract_scanner.py)",
    )
    parser.add_argument(
        "--overrides", default="{}",
        help='JSON string of manual factor overrides, e.g. \'{"past_performance": 1}\'',
    )
    parser.add_argument(
        "--output", default="",
        help="Output CSV path (default: auto-generated in data/final/)",
    )
    parser.add_argument(
        "--top", type=int, default=0,
        help="Show only top N scored opportunities",
    )

    args = parser.parse_args()

    # Load CSV
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} opportunities from {csv_path.name}")

    overrides = json.loads(args.overrides)
    config = json.loads(CONFIG_PATH.read_text())

    # Score all opportunities
    opps = df.to_dict("records")
    scored = score_opportunities_batch(opps, overrides_map={}, config=config)

    # Apply global overrides to all
    if overrides:
        scored = []
        for opp in opps:
            result = score_opportunity(opp, overrides=overrides, config=config)
            scored.append({
                **opp,
                "bid_score": result["total_score"],
                "bid_decision": result["decision"],
                "_score_result": result,
            })

    # Sort by score descending
    scored.sort(key=lambda x: x.get("bid_score", 0), reverse=True)

    # Print scorecards
    display = scored[:args.top] if args.top else scored
    for item in display:
        result = item.pop("_score_result", None)
        if result:
            print(format_scorecard(result, item))

    # Summary
    decisions = {}
    for item in scored:
        d = item.get("bid_decision", "Unknown")
        decisions[d] = decisions.get(d, 0) + 1

    print(f"\n{'='*70}")
    print(f"SCORING SUMMARY ({len(scored)} opportunities)")
    print(f"{'='*70}")
    for label, _, color in DECISION_THRESHOLDS:
        count = decisions.get(label, 0)
        print(f"  {label:15s}: {count}")

    avg_score = sum(s.get("bid_score", 0) for s in scored) / max(len(scored), 1)
    print(f"\n  Average score: {avg_score:.1f}")

    # Save scored CSV
    # Remove internal _score_result before saving
    for item in scored:
        item.pop("_score_result", None)

    scored_df = pd.DataFrame(scored)
    if args.output:
        out_path = Path(args.output)
    else:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y%m%d_%H%M")
        out_dir = _project_root / "data" / "final"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"govt_scored_opportunities_{date_str}.csv"

    scored_df.to_csv(out_path, index=False)
    print(f"\n  Saved scored results to {out_path}")


if __name__ == "__main__":
    main()
