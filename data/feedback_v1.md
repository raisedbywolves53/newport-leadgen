Slides 4 and 5 need another pass. The current versions feel like cookie-cutter templates — the bento grid is being forced onto data that needs its own layout. Each slide should feel like a purpose-built dashboard, not a stamped template.

SLIDE 4 (FloridaTamSlide) — FULL REWRITE:

The story: "$87M market, five layers deep — here's how to read it."

Layout: The concentric circles ARE the slide. They should be large, centered, and commanding — not crammed into a small card. Think of this as a full-width data visualization with supporting context.

Structure:
- Header area: eyebrow + headline + subtitle + GoldLine (same as now, that's fine)
- Main area: Large concentric circle visualization taking up ~60% of the slide width, vertically centered. Five rings using ONLY these colors from outside in: gold at 20% opacity, gold at 35%, teal at 40%, teal at 60%, teal at 80%. Center: "$87M" in white bold text with "TOTAL TAM" beneath it. Each ring has its label (channel name + dollar amount) positioned cleanly ON the ring.
- Right side (~35%): A vertical stack of 5 compact channel cards — one per ring. Each card: small colored dot matching its ring color, channel name (sm semibold), dollar amount (xl bold, teal), one-line detail (xs, navy-800/50). These cards should feel like a legend that also tells you WHY each channel matters. Include the detail text like "117 tracked contracts >$10K" and "83% invisible in public databases" — that context is critical to the story.
- Bottom: channel dot legend row + source citation

The circles should have a subtle hover interaction — when you mouse over a ring, it slightly brightens and the corresponding card on the right gets a subtle highlight border. This is the "interactive" feel of a real dashboard.

Do NOT put the circles inside a card. They float directly on the slide background. The right-side channel cards ARE in standard card surfaces.

SLIDE 5 (ProductMatrixSlide) — FULL REWRITE:

The story: "Not all products are equal — here's where Newport has pricing power."

Layout: Two distinct zones — chart on top, detail cards below.

Structure:
- Header area: eyebrow + headline + subtitle + GoldLine
- Top zone (hero visual, ~55% of content height): A horizontal bar chart inside a wide card. Full width. ECharts with these specs:
  - Bars sorted descending by FL spend
  - Tier 1 bars: gold fill with 80% opacity, rounded right ends (borderRadius: [0, 4, 4, 0])
  - Tier 2 bars: teal fill with 70% opacity, same rounded ends
  - Tier 3/Avoid bars: navy-800 at 15% opacity (barely visible — they're deprioritized)
  - Category labels on Y axis in Inter 12px
  - Value labels at end of each bar in matching color, bold
  - Grid: subtle horizontal lines only, no vertical, no chart border
  - Chart should have generous internal padding so bars aren't cramped
  - Add a compact legend below the chart: gold dot "Tier 1 — Highest", teal dot "Tier 2 — Growth", gray dot "Avoid"
  - Hover interaction: hovering a bar shows a tooltip with sole-source %, markup range, and one-line advantage text
- Bottom zone (~40%): Two cards side by side (grid-cols-2 gap-4)
  - Left card: "Confectionery & Nuts" deep dive — $55M national stat in gold, "58% sole-source" callout, Newport's Segment E advantage, "HIGHEST FIT" as a gold ghost badge (bg-[#C9A84C]/10 text-[#C9A84C])
  - Right card: "LPTA Evaluation" — explain why Lowest Price Technically Acceptable favors wholesalers, with the key insight that volume purchasing = pricing power
- Footer: Avoid items as subtle strikethrough text + source citation

IMPORTANT: Do not strip content. Every insight, detail line, and data point that existed in the previous version should still be present — just better organized. The slides should feel RICHER than before, not emptier.

Charts must be static on render (no animation/bounce) but CAN have hover interactions (tooltips, highlights). Modern and sleek like a Bloomberg or Stripe dashboard.