Slide 4 looks great visually. One remaining issue: the concentric circles have NO hover interaction. When I mouse over the rings, nothing happens — no tooltip, no highlight, no card connection.

This is the only fix needed. Add hover interactivity to the concentric circles:

1. Each ring must be a separate hoverable element (likely individual div or SVG path elements with pointer-events enabled, not a flat image or single div with CSS gradients)
2. On hover:
   - The hovered ring increases opacity by ~15%
   - A tooltip appears near the cursor showing: channel name, dollar range, confidence level, and 1-2 sentence insight
   - The corresponding card on the right gets a brighter/thicker left border
3. On mouse leave: everything resets to default state

The tooltip should match slide 5's bar chart tooltip style — clean, modern, white background with subtle shadow, text in navy-950.

IMPORTANT: If the rings are currently built as CSS box-shadows, border rings, or background gradients on a single element, they need to be refactored into separate hoverable elements (individual absolutely-positioned divs or SVG circles). A single element cannot have per-ring hover states.

Do not change anything else about slide 4 — the layout, sizing, cards, and labels are all approved.