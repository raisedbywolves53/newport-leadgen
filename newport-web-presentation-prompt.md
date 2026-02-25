# PROMPT FOR NEW CHAT

## Paste this as your message:

---

Build an interactive web presentation for Newport Wholesalers' government contracting opportunity as a single React (.jsx) artifact. This replaces a PowerPoint deck we already built — the goal is a hybrid that toggles between "Presentation Mode" (polished full-screen slides you navigate with arrows/clicks) and "Model Mode" (interactive financial dashboard with sliders).

Project: newport-leadgen

## DESIGN DIRECTION
- Palette: "Midnight Executive" — dark navy (#0F1A2E, #1A2744), teal (#1B7A8A), warm amber accent (#E8913A), off-white (#F5F6FA)
- Typography: Use Google Fonts — a serif display font (like Playfair Display or similar) for titles, clean sans-serif for body
- Tone: Investment-grade pitch meets interactive data tool. Think McKinsey deck meets Bloomberg terminal toggle.
- Icons: Use lucide-react throughout

## ARCHITECTURE
1. **Presentation Mode**: Full-screen slide sections navigated via arrow keys, click, or nav dots. Smooth scroll-snap or state-based transitions. Sections:
   - Title slide
   - Executive Summary (4 stat callouts: $87M TAM, 83% zero-bid contracts, $841K cumulative OE by Y5, 70% renewal rate)
   - Section divider: "The Opportunity"
   - Why Newport Wins (4 cards with icons: 30yr operations, post-DOGE moat, infrastructure in place, no past performance needed)
   - The Florida Opportunity (3 big stat blocks + funnel: $87M → $17-20M biddable → $6.4M FPDS visible)
   - Confectionery Gap (PSC 8925 — 58% sole-source, only 45 national awards, Newport's Segment E candy expertise)
   - Target Agencies (2x2: DOJ/BOP $3.7M/71 contracts, Military/DoD $2.3M/43, FEMA disaster-driven, School Districts $500M-$1B FL)
   - Competition table (#1-8 FL food distributors, Newport enters at #5-10 tier with $1-5M)
   - Section divider: "The Strategy"
   - How It Works (pipeline: Identify → Score → Pursue → Submit → Win, plus 3 capability cards)
   - Two Routes comparison (Free $0/yr vs Paid $13K/yr — feature comparison + outcome rows)
   - Credibility Waterfall (Year 1: build track record → Years 2-3: leverage & compound → Years 4-5: incumbent advantage)
   - Section divider: "The Economics" ← THIS IS WHERE THE TOGGLE LIVES
   - Financial slides (Owner Earnings trajectory chart + 5-Year P&L table + Compounding Flywheel stacked bar)
   - Section divider: "Execution"
   - Risk & Compliance (What You Need vs What You DON'T Need side-by-side)
   - Key Questions (10 questions table)
   - Next Steps + contact (closing slide)

2. **Model Mode Toggle**: Available on the financial section slides. When toggled:
   - Slide content shifts/shrinks to accommodate interactive controls
   - Sliders appear for: Gross Margin (15-30%, default 22%), Renewal Rate (50-90%, default 70%), Win Rate (8-20%, default 12%), Avg Contract Value ($5K-$50K, default $15K), Bid Volume Growth (5-20%/yr, default 10%)
   - The full 5-year P&L recomputes live: Bids Submitted, Contracts Won, Active Contracts, Renewed, Revenue, Gross Profit, Bid Prep Costs, Fulfillment, Program Costs, Owner Earnings, Cumulative OE
   - Charts animate/update in real-time with the new values
   - A "Reset to Base Case" button restores defaults

3. **Financial Model Logic** (base case):
   - Year 1: 84 bids, 12% win rate = 10 wins, $15K avg = $100K revenue, 22% gross margin
   - Renewals: 70% of prior year active contracts renew
   - Active = new wins + renewed
   - Bid volume grows ~10%/yr
   - Costs: Bid prep ~$260/bid, Fulfillment 3% of revenue, Program costs decline from $11K to $4K
   - Revenue = active contracts × avg contract value
   - Owner Earnings = Gross Profit - Bid Prep - Fulfillment - Program Costs

## KEY BEHAVIORS
- Stat callouts should count up from 0 when they scroll into view (useIntersectionObserver or similar)
- Charts should animate on entry
- The Presentation ↔ Model toggle should be a smooth, visually satisfying transition (not a jarring page swap)
- Keyboard navigation: left/right arrows move between slides, Escape exits model mode
- Mobile-responsive but optimized for desktop/tablet presentation
- Nav dots or progress indicator showing current position in deck

## AVAILABLE LIBRARIES (in Claude artifact environment)
- React (useState, useEffect, useCallback, useRef, useMemo)
- recharts (LineChart, BarChart, PieChart, etc.)
- lucide-react (all icons)
- lodash
- Tailwind CSS (utility classes only, no compiler)
- shadcn/ui components

Do NOT use localStorage or sessionStorage. Keep all state in React useState/useReducer.

Build the complete working artifact. This is the main deliverable — take the space you need.

---

## END OF PROMPT

