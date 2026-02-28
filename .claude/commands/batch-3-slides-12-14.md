# Build Slides 12–14 — Split Layout + Table Layout

Read `web/DESIGN-SYSTEM.md` completely before starting. Follow it exactly.

## TWO LAYOUTS

**SPLIT** (slides 12, 14) = visual LEFT (col-span-3) + tiles RIGHT (col-span-2)
**TABLE** (slide 13) = tiles horizontal TOP + full-width table BELOW

See DESIGN-SYSTEM.md sections 6.2–6.4 for templates and 11 for Recharts.

---

## Slide 12: RelationshipSlide.jsx — SPLIT

**Data:** `import { INFLUENCE_LAYERS, BD_PROCESS_STEPS } from '../../data/strategy'`

**Header:** Eyebrow "Business Development" → Headline "Who to Know, How to Win" → Subtitle "The relationship-driven path to government procurement."

**LEFT (col-span-3):** ChartCard with numbered vertical timeline (5 BD steps). Each step = numbered circle (gold bg for step 1, zinc-100 for others) + step name + brief description. CardHeader "Business Development Process" / "5-step relationship building". CardFooter "The fastest path: relationship with a front-line buyer who can issue micro-purchase orders."

**RIGHT (col-span-2):** 3 stacked compact tiles (influence layers):
1. label "Front-Line Buyers", value "Micro-Purchase" (gold), badge "Primary", footer "Contracting officers with P-card authority" / "Direct purchase power under $15K"
2. label "Program Managers", value "Requirements" (teal), badge "Influence", footer "Define specifications and quantities" / "Shape future solicitations"
3. label "Contracting Officers", value "Authority" (teal), badge "Decision", footer "Sign contracts and approve vendors" / "Formal procurement authority"

**Source:** "FAR Part 13 | Federal Acquisition Institute"

---

## Slide 13: ComplianceSlide.jsx — TABLE LAYOUT

**Data:** `import { COMPLIANCE_REQUIRED, COMPLIANCE_NOT_NEEDED } from '../../data/strategy'`

**Header:** Eyebrow "Entry Barriers" → Headline "Lower Than You Think" → Subtitle "Government entry costs vs. complexity Newport avoids entirely."

**TOP ROW:** `grid-cols-3 gap-4` — **standard** stat cards:
1. label "Total Entry Cost", value "$4K–$31.5K" (gold), badge "One-time", footer "Registration fees + optional platforms" / "Compared to $500K+ for large contracts"
2. label "Complexity Avoided", value "$120–360K" (teal), badge "Saved", footer "No DCAA audit, no CAS, no clearance" / "Only applies above $2M threshold"
3. label "Registrations Needed", value "6" (teal), badge "Straightforward", footer "SAM, MFMP, GSA, cage code, etc." / "Most completed in 2–4 weeks"

**BELOW:** Full-width TableCard with gold accent strip. CardHeader "Requirements Checklist" / "What Newport needs vs. what it skips". Two-column layout inside: Left = Required items (Check icon teal + item name), Right = Not Required items (X icon zinc + item name line-through). Table rows `hover:bg-zinc-50`. CardFooter "Newport's entry point is below the complexity threshold that stops most companies."

**Source:** "FAR Part 4, 30, 31 | DCAA.mil | SAM.gov"

---

## Slide 14: RecommendationSlide.jsx — SPLIT

**Data:** `import { ROUTE_COMPARISON } from '../../data/strategy'`

**Header:** Eyebrow "Strategic Choice" → Headline "Two Paths Forward" → Subtitle "Free vs. paid market access — the visibility trade-off."

**LEFT (col-span-3):** ChartCard with route comparison visual (two columns inside card, or grouped bar chart). CardHeader "Route Comparison" / "Side-by-side capabilities and trade-offs". Use Check/X icons for boolean features. Paid column values in gold where superior. CardFooter "Recommendation: Paid route pays for itself within the first quarter."

**RIGHT (col-span-2):** 4 stacked compact tiles:
1. label "Free Route Cost", value "$0" (zinc-950), badge "No cost", footer "SAM.gov + manual portal checks" / "40–50% opportunity visibility"
2. label "Paid Route Cost", value "$13K/yr" (gold), badge "★ Recommended", footer "Unison + BidNet + DemandStar" / "90%+ opportunity visibility"
3. label "Visibility Gap", value "2x" (gold), badge "↑ Critical", footer "Paid sees 2x more opportunities" / "Higher win probability"
4. label "Break-Even", value "1 Win" (teal), badge "Low bar", footer "Single $15K+ contract covers cost" / "ROI from first government sale"

**Source:** "Unison Marketplace | BidNet Direct | DemandStar | SAM.gov"

---

## AFTER BUILDING ALL 3:

1. Register new slides in `web/src/data/slides.js` if needed
2. Run `cd web && npm run build` — zero errors

## Checklist:
- [ ] Slides 12, 14: `grid-cols-5 gap-4` split layout (visual LEFT, tiles RIGHT)
- [ ] Slide 13: standard stat row TOP + full-width table BELOW
- [ ] All cards have hover states
- [ ] Table rows have `hover:bg-zinc-50`
- [ ] Source citations present
- [ ] Build passes
