# Slide Fixes — BATCH 3

> **Context**: BATCH2 established the right structural patterns (bento grid on slide 6, hierarchical cards on slide 7, tiered table on slide 8) but the execution has layout/spacing issues. This batch fixes those issues by aligning with the EXACT container and spacing patterns from the validated Slide 3 (WhyNewportSlide.jsx).
>
> **Reference file**: `src/components/slides/WhyNewportSlide.jsx` — the LOCKED quality benchmark. Copy patterns from this file directly.

---

## Fix 1: Slide 6 — ConfectioneryGapSlide.jsx

**Problem**: Content clips at the bottom. The container uses `pt-6 pb-20` without `justify-center`, while validated Slide 3 uses `justify-center px-20 pb-16`. The ~40px difference pushes the bento grid's bottom row into the source citation.

**Changes**:

### 1a. Fix the root container (line ~34)

Change:
```jsx
<div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
```

To (matching Slide 3 exactly):
```jsx
<div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
```

### 1b. That's it.

The bento grid structure, hero card, stat cards, and source section are already correct — they mirror Slide 3's pattern. The ONLY problem was the container padding/centering.

Do NOT change:
- The grid: `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr]` with `height: '460px'` ✓
- The hero card with `row-span-2` ✓
- The 3 StatCards ✓
- The source section ✓

---

## Fix 2: Slide 7 — TargetAgenciesSlide.jsx

**Problem**: Cards are too compact, leaving ~40% of the slide as empty whitespace below the secondary cards. The source line with `mt-auto` pushes to the very bottom, making the gap obvious.

**Changes**:

### 2a. Fix the root container (line ~17)

Change:
```jsx
<div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
```

To:
```jsx
<div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
```

### 2b. Wrap all content below the header in a flex-1 container

After the header `</div>` and before the primary targets grid, wrap everything (both card grids + expansion label) in a growing container:

```jsx
{/* Card sections — fill available space */}
<div className="flex flex-col flex-1 min-h-0 relative z-10">
```

Close this `</div>` right before the Source `<div>`.

### 2c. Make the primary cards grid grow

Change the primary targets grid (line ~50):
```jsx
<div className="grid grid-cols-2 gap-4 mb-4 relative z-10">
```

To:
```jsx
<div className="grid grid-cols-2 gap-5 mb-4 flex-1">
```

Remove the `relative z-10` (the wrapper now handles z-10).

### 2d. Make the primary cards fill their grid cells

Each primary card currently has `p-6`. Change to `p-8` and ensure they grow:

In the primary agency card `motion.div` (line ~60):
```jsx
className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-6 relative overflow-hidden"
```

Change to:
```jsx
className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-8 relative overflow-hidden flex flex-col"
```

### 2e. Make secondary cards slightly taller

Change secondary cards (line ~110):
```jsx
className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] px-5 py-4 relative overflow-hidden"
```

To:
```jsx
className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] px-6 py-5 relative overflow-hidden"
```

### 2f. Increase gap between expansion label and secondary grid

Change the secondary grid gap (line ~100):
```jsx
<div className="grid grid-cols-2 gap-4 relative z-10">
```

To:
```jsx
<div className="grid grid-cols-2 gap-5">
```

### 2g. Fix the source section

Change source container (line ~142):
```jsx
<div className="flex items-center justify-between mt-auto pt-4 relative z-10">
```

To:
```jsx
<div className="flex items-center justify-between mt-4 relative z-10">
```

The `mt-auto` is no longer needed because the flex-1 wrapper fills the space naturally.

---

## Fix 3: Slide 8 — CompetitionSlide.jsx

**Problem**: Table content overflows — the bottom 2 competitors (Matts Trading, Wholesome Foods) are cut off. 3 tier labels + 9 data rows + header = ~740px of content squeezed into ~520px.

**Changes**:

### 3a. Fix the root container (line ~119)

Change:
```jsx
<div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
```

To:
```jsx
<div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
```

### 3b. Tighten the header spacing

Change header `mb-4` (line ~123):
```jsx
<div className="mb-4 relative z-10">
```

To:
```jsx
<div className="mb-3 relative z-10">
```

Also reduce the subtitle margin. Change `mb-2` on the h2 (line ~136):
```jsx
className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
```

To:
```jsx
className="font-body text-3xl font-bold tracking-tight text-navy-950 mb-1"
```

(Using `text-3xl` because this is a data-dense slide — the design system allows it.)

And change the subtitle text size from `text-sm` to `text-[13px]`:
```jsx
className="font-body text-[13px] text-navy-800/60 max-w-2xl"
```

Change GoldLine margin from `mt-3` to `mt-2`:
```jsx
<GoldLine width={60} className="mt-2" delay={0.25} />
```

### 3c. Tighten the table header row

Change (line ~160):
```jsx
className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-b-2 border-black/[0.10]"
```

To:
```jsx
className="grid grid-cols-[40px_1.4fr_120px_1fr] px-5 py-2.5 border-b-2 border-black/[0.10]"
```

Also reduce the header text from `text-xs` to `text-[10px]`:
```jsx
<span className="font-body text-[10px] font-bold uppercase tracking-wider text-navy-800/50 text-center">
```

Apply this to all 4 header spans.

### 3d. Tighten the TierLabel component

Change the TierLabel function (line ~39-47):
```jsx
function TierLabel({ children }) {
  return (
    <div className="px-6 py-2 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
      <span className="font-body text-[10px] font-semibold uppercase tracking-widest text-navy-800/30">
        {children}
      </span>
    </div>
  )
}
```

To:
```jsx
function TierLabel({ children }) {
  return (
    <div className="px-5 py-1 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
      <span className="font-body text-[9px] font-semibold uppercase tracking-widest text-navy-800/25">
        {children}
      </span>
    </div>
  )
}
```

This saves ~12px per label × 3 = 36px.

### 3e. Tighten the CompetitorRow component

Change (line ~56):
```jsx
className={`grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-l-[3px] border-b border-black/[0.06] ${
```

To:
```jsx
className={`grid grid-cols-[40px_1.4fr_120px_1fr] px-5 py-2.5 border-l-[3px] border-b border-black/[0.06] ${
```

Change rank text from `text-base` to `text-sm`:
```jsx
<span className="font-body text-sm font-semibold text-center text-navy-800/50">
```

Change company text from `text-base` to `text-sm`:
```jsx
<span className={`font-body text-sm ${
```

Change amount text from `text-base` to `text-sm`:
```jsx
<span className={`font-body text-sm font-bold tracking-tight ${
```

Change notes text from `text-sm` to `text-xs`:
```jsx
<span className="font-body text-xs text-navy-800/50">
```

### 3f. Tighten the NewportCalloutRow

Change (line ~95):
```jsx
className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-5 border-l-[4px] border-b border-black/[0.06]"
```

To:
```jsx
className="grid grid-cols-[40px_1.4fr_120px_1fr] px-5 py-3 border-l-[4px] border-b border-black/[0.06]"
```

Change the arrow from `text-base` to `text-sm`:
```jsx
<span className="font-body text-sm font-bold text-center" style={{ color: '#1B7A8A' }}>
```

Change company name from `text-base` to `text-sm`:
```jsx
<span className="font-body text-sm font-bold" style={{ color: '#1B7A8A' }}>
```

Change amount from `text-base` to `text-sm`:
```jsx
<span className="font-body text-sm font-bold tracking-tight" style={{ color: '#C9A84C' }}>
```

Change notes from `text-sm` to `text-xs`:
```jsx
<span className="font-body text-xs text-navy-800/60">
```

### 3g. Tighten the source section

Change:
```jsx
<div className="flex items-center justify-between mt-4 relative z-10">
```

To:
```jsx
<div className="flex items-center justify-between mt-3 relative z-10">
```

---

## Summary of Space Savings (Slide 8)

| Element | Before | After | Savings |
|---------|--------|-------|---------|
| Container top padding | pt-6 (24px) | 0 (justify-center) | ~24px |
| Container bottom padding | pb-20 (80px) | pb-16 (64px) | 16px |
| Header section | ~130px | ~100px | ~30px |
| 3 × TierLabel | ~108px (36px each) | ~72px (24px each) | 36px |
| 9 × Data rows | ~504px (56px each) | ~360px (40px each) | 144px |
| Table header | ~56px | ~40px | 16px |
| Source section | mt-4 | mt-3 | 4px |
| **Total saved** | | | **~270px** |

This should bring total content from ~740px to ~470px, fitting comfortably in the ~520px available with the new container.

---

## Verification Checklist

After applying all changes, verify:

- [ ] Slide 6: Bento grid centered vertically, no clipping at bottom, source citation visible below grid
- [ ] Slide 7: Cards fill the vertical space naturally, no huge whitespace gap above the source line
- [ ] Slide 8: ALL 8 competitors + Newport callout row visible without scrolling, tier labels are subtle separators (not space hogs)
- [ ] All three slides: Container matches Slide 3's `justify-center px-20 pb-16` pattern
- [ ] Color discipline: Only gold (#C9A84C) and teal (#1B7A8A) as accents
- [ ] Typography: All Inter, no Playfair
