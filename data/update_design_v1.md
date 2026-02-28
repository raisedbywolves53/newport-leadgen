Read web/DESIGN-SYSTEM.md completely before doing anything — it is the single source of truth for all visual decisions.

Then read these 3 slide files:
- web/src/components/slides/WhyNewportSlide.jsx
- web/src/components/slides/FloridaTamSlide.jsx  
- web/src/components/slides/ProductMatrixSlide.jsx

TASK: Audit slides 3–5 against the DESIGN-SYSTEM.md and fix any deviations. The design system was just rewritten with explicit component blueprints (MetricCard, HeroMetricCard, ChartCard) and dashboard layout patterns (A–F). Each slide must structurally match these blueprints.

For each slide, check and fix:

1. CARD ANATOMY — Every card must have the shadcn structure:
   - CardHeader zone: title is `text-sm text-zinc-500` (muted, small). NOT bold, NOT dark.
   - CardContent zone: big number + detail
   - CardFooter zone (where applicable): separated by `border-t border-zinc-100`

2. CHART CARDS — FloridaTamSlide and ProductMatrixSlide both have chart areas. Each must have:
   - CardHeader with `text-lg font-semibold text-zinc-950` title + `text-sm text-zinc-500` description
   - CardContent with the chart
   - CardFooter with legend, separated by `border-t border-zinc-100`

3. CARD SURFACE — Every card: `rounded-xl bg-white border border-zinc-200 shadow-sm`. No exceptions. No `bg-white/70`, no `backdrop-blur`, no custom shadows.

4. METRIC TILES — The stat tiles on each slide must follow the MetricCard blueprint:
   - Title top in `text-sm text-zinc-500`
   - Value below in `text-2xl font-semibold tracking-tight` with accent color
   - Optional icon top-right in `w-8 h-8 rounded-md bg-zinc-100`
   - Padding `p-6` standard or `p-5` compact

5. LAYOUT GRIDS:
   - Slide 3: Pattern D (bento) — `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr] gap-4`
   - Slide 4: Pattern A variant — `grid-cols-[3fr_2fr] gap-4`
   - Slide 5: Pattern B — full-width ChartCard + `grid-cols-3 gap-4` stat row below

6. HERO CARD — Max 1 per slide with gold accent strip: `absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]`

7. HEADER ZONE — Every slide:
   - Eyebrow: `text-xs font-medium uppercase tracking-widest text-teal-500`
   - Headline: `text-3xl font-semibold tracking-tight text-zinc-950`
   - Subtitle: `text-sm text-zinc-600 max-w-2xl`
   - GoldLine width={48}

8. SOURCE ZONE — Bottom of every slide with SourceCitation component

9. ANIMATION — Cards stagger at `delay: 0.3 + i * 0.08`. Total under 1.5s.

10. SPACING — `gap-4` between all cards. `px-16 lg:px-20 pb-16` on container. `mb-4` after header.

Do NOT change the data, content, or narrative of any slide. Only fix structural alignment with the design system blueprints. After changes, run `cd web && npm run build` to verify no errors.