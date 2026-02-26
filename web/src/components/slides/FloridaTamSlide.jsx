import { useState } from 'react'
import { motion } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'

// Ring data — outside-in, sized proportional to dollar value midpoint
// Richer tooltip content per feedback v4
const RING_CONFIG = [
  { label: 'State', amount: '$20-30M', confidence: 'MEDIUM', detail: 'MFMP + corrections + FL agencies. Free registration. Largest single channel.', color: 'rgba(201,168,76,0.20)', hoverColor: 'rgba(201,168,76,0.35)', accent: '#C9A84C', midVal: 25 },
  { label: 'Education', amount: '$10-20M', confidence: 'MEDIUM', detail: '67 county districts, 2.8M students. NSLP funded. Second largest opportunity.', color: 'rgba(201,168,76,0.35)', hoverColor: 'rgba(201,168,76,0.50)', accent: '#C9A84C', midVal: 15 },
  { label: 'Micro-Purchase', amount: '$8-15M', confidence: 'HIGH', detail: '83% invisible in public databases. Below $15K threshold — no competitive bidding required. Fastest path to first contract.', color: 'rgba(27,122,138,0.40)', hoverColor: 'rgba(27,122,138,0.55)', accent: '#1B7A8A', midVal: 12 },
  { label: 'Federal FPDS', amount: '$6.4M', confidence: 'HIGH', detail: '117 tracked contracts >$10K. The visible tip of the iceberg.', color: 'rgba(27,122,138,0.60)', hoverColor: 'rgba(27,122,138,0.75)', accent: '#1B7A8A', midVal: 6.4 },
  { label: 'Local / Municipal', amount: '$3-7M', confidence: 'MEDIUM', detail: 'County jails, municipal facilities. DemandStar + VendorLink portals.', color: 'rgba(27,122,138,0.80)', hoverColor: 'rgba(27,122,138,0.95)', accent: '#1B7A8A', midVal: 5 },
]

// Compute ring outer radii so thickness ∝ dollar value
const OUTER_R = 250
const TOTAL_VAL = RING_CONFIG.reduce((s, r) => s + r.midVal, 0)
const CENTER_R = 60
const RING_GAP = 2 // px gap between rings for visual separation
const USABLE = OUTER_R - CENTER_R - RING_GAP * (RING_CONFIG.length - 1)
const RING_RADII = (() => {
  const radii = []
  let r = OUTER_R
  for (let i = 0; i < RING_CONFIG.length; i++) {
    const outerR = r
    const thickness = (RING_CONFIG[i].midVal / TOTAL_VAL) * USABLE
    r -= thickness
    radii.push({ outer: outerR, inner: r })
    r -= RING_GAP // gap before next ring
  }
  return radii
})()
const CONTAINER = OUTER_R * 2 + 20

export default function FloridaTamSlide() {
  const [hoveredRing, setHoveredRing] = useState(null)
  const cx = CONTAINER / 2
  const cy = CONTAINER / 2

  return (
    <div className="w-full h-full flex flex-col justify-center px-16 pt-6 pb-8 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -left-40" opacity={0.03} />
      <BackgroundRing size={300} className="bottom-16 -right-24" opacity={0.025} />

      {/* Header */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-teal-500 mb-3"
        >
          Florida Total Addressable Market
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          $87M Market, Five Layers Deep
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-navy-800/60 max-w-2xl"
        >
          Federal is the entry point — state, education, and local expand the opportunity.
        </motion.p>
        <GoldLine width={60} className="mt-3" delay={0.25} />
      </div>

      {/* Main: circles left (~60%) + channel cards right (~35%) */}
      <div className="flex gap-3 relative z-10 flex-1 min-h-0">

        {/* Concentric circles — no labels, hover-driven */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center justify-center"
          style={{ width: '60%' }}
        >
          <div className="relative" style={{ width: CONTAINER, height: CONTAINER }}>
            {/* Rings — proportional thickness, 2px gap between each */}
            {RING_CONFIG.map((ring, i) => {
              const size = RING_RADII[i].outer * 2
              return (
                <motion.div
                  key={ring.label}
                  initial={{ scale: 0.6, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.35 + i * 0.1, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
                  className="absolute rounded-full cursor-pointer transition-all duration-200"
                  style={{
                    width: size,
                    height: size,
                    left: (CONTAINER - size) / 2,
                    top: (CONTAINER - size) / 2,
                    backgroundColor: hoveredRing === i ? ring.hoverColor : ring.color,
                  }}
                  onMouseEnter={() => setHoveredRing(i)}
                  onMouseLeave={() => setHoveredRing(null)}
                />
              )
            })}

            {/* Hover tooltip — matches slide 5 bar chart style */}
            {hoveredRing !== null && (
              <div
                className="absolute pointer-events-none"
                style={{ zIndex: 20, left: cx, top: cy - OUTER_R - 14, transform: 'translate(-50%, -100%)' }}
              >
                <div className="rounded-lg px-4 py-3 bg-white shadow-[0_4px_16px_rgba(0,0,0,0.12)] border border-black/[0.06] max-w-[280px]">
                  <p className="font-body text-[13px] font-semibold text-navy-950">{RING_CONFIG[hoveredRing].label}</p>
                  <p className="font-body text-[12px] text-navy-800/70 mt-0.5">
                    {RING_CONFIG[hoveredRing].amount}
                    <span className="text-navy-800/40 ml-2">Confidence: {RING_CONFIG[hoveredRing].confidence}</span>
                  </p>
                  <p className="font-body text-[12px] text-navy-800/60 mt-1 leading-snug">{RING_CONFIG[hoveredRing].detail}</p>
                </div>
              </div>
            )}

            {/* Center: $87M */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
              className="absolute inset-0 flex items-center justify-center pointer-events-none"
              style={{ zIndex: 10 }}
            >
              <div className="text-center">
                <span className="font-body text-5xl font-bold tracking-tight block leading-none text-white drop-shadow-[0_1px_3px_rgba(0,0,0,0.3)]">
                  $87M
                </span>
                <span className="font-body text-[11px] font-semibold uppercase tracking-widest block mt-1.5 text-white/80 drop-shadow-[0_1px_2px_rgba(0,0,0,0.3)]">
                  Total TAM
                </span>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Right: 5 channel cards — larger, with colored left border */}
        <div className="flex flex-col gap-2.5 justify-center" style={{ width: '35%' }}>
          {RING_CONFIG.map((ring, i) => (
            <motion.div
              key={ring.label}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: 0.45 + i * 0.08 }}
              className="rounded-xl bg-white/80 backdrop-blur-sm px-4 py-4 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] transition-all duration-200 relative overflow-hidden"
              style={{
                borderColor: hoveredRing === i ? ring.accent : undefined,
              }}
            >
              {/* Left accent strip — thicker/brighter on hover */}
              <div
                className="absolute left-0 top-2 bottom-2 rounded-full transition-all duration-200"
                style={{
                  backgroundColor: ring.accent,
                  width: hoveredRing === i ? 4 : 3,
                  opacity: hoveredRing === i ? 1 : 0.7,
                }}
              />
              <div className="flex items-start gap-3 pl-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="font-body text-sm font-semibold text-navy-950">
                      {ring.label}
                    </span>
                    <span
                      className="font-body text-2xl font-bold tracking-tight leading-none shrink-0"
                      style={{ color: '#1B7A8A' }}
                    >
                      {ring.amount}
                    </span>
                  </div>
                  <p className="font-body text-sm text-navy-800/50 mt-1 leading-snug">
                    {ring.detail}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom: legend + source */}
      <div className="flex items-center justify-between mt-3 relative z-10">
        <div>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="flex items-center gap-4 mb-1"
          >
            {RING_CONFIG.map((ring) => (
              <div key={ring.label} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: ring.color, border: `1px solid ${ring.accent}` }} />
                <span className="font-body text-[12px] text-navy-800/50">{ring.label}</span>
              </div>
            ))}
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="text-[11px] text-navy-800/40"
          >
            USASpending API FY2024 | FL MFMP | FL DOE, USDA NSLP | County procurement
          </motion.p>
        </div>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
