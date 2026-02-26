import { useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'

// Ring data — outside-in, sized proportional to dollar value midpoint
const RING_CONFIG = [
  { label: 'State', amount: '$20-30M', confidence: 'MEDIUM', detail: 'MFMP + corrections + FL agencies. Free registration. Largest single channel.', color: '#C9A84C', midVal: 25 },
  { label: 'Education', amount: '$10-20M', confidence: 'MEDIUM', detail: '67 county districts, 2.8M students. NSLP funded. Second largest opportunity.', color: '#C9A84C', midVal: 15 },
  { label: 'Micro-Purchase', amount: '$8-15M', confidence: 'HIGH', detail: '83% invisible in public databases. Below $15K threshold — no competitive bidding required. Fastest path to first contract.', color: '#1B7A8A', midVal: 12 },
  { label: 'Federal FPDS', amount: '$6.4M', confidence: 'HIGH', detail: '117 tracked contracts >$10K. The visible tip of the iceberg.', color: '#1B7A8A', midVal: 6.4 },
  { label: 'Local / Municipal', amount: '$3-7M', confidence: 'MEDIUM', detail: 'County jails, municipal facilities. DemandStar + VendorLink portals.', color: '#1B7A8A', midVal: 5 },
]

// SVG ring geometry
const SVG_SIZE = 500
const CX = SVG_SIZE / 2
const CY = SVG_SIZE / 2
const OUTER_R = 220
const CENTER_R = 55
const RING_GAP = 4
const TOTAL_VAL = RING_CONFIG.reduce((s, r) => s + r.midVal, 0)
const USABLE = OUTER_R - CENTER_R - RING_GAP * (RING_CONFIG.length - 1)

// Precompute ring radii and SVG stroke parameters
const RINGS = (() => {
  const rings = []
  let r = OUTER_R
  for (let i = 0; i < RING_CONFIG.length; i++) {
    const thickness = (RING_CONFIG[i].midVal / TOTAL_VAL) * USABLE
    const outerR = r
    const innerR = r - thickness
    const midR = (outerR + innerR) / 2
    rings.push({ outerR, innerR, midR, thickness })
    r = innerR - RING_GAP
  }
  return rings
})()

// Opacity levels for rings — Bloomberg-bold, progressively darker toward center
const BASE_OPACITIES = [0.45, 0.55, 0.60, 0.70, 0.82]
const HOVER_OPACITIES = [0.65, 0.75, 0.80, 0.88, 0.95]
function ringOpacity(index, isHovered) {
  return isHovered ? HOVER_OPACITIES[index] : BASE_OPACITIES[index]
}

export default function FloridaTamSlide() {
  const [hoveredRing, setHoveredRing] = useState(null)

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

        {/* Concentric circles — SVG annular rings for true per-ring hover */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center justify-center relative"
          style={{ width: '60%' }}
        >
          <svg
            width={SVG_SIZE}
            height={SVG_SIZE}
            viewBox={`0 0 ${SVG_SIZE} ${SVG_SIZE}`}
            className="overflow-visible"
            style={{ maxWidth: '100%', maxHeight: '100%' }}
          >
            {/* Rings — each is a <circle> with stroke = thickness */}
            {RING_CONFIG.map((ring, i) => {
              const { midR, thickness } = RINGS[i]
              const isHovered = hoveredRing === i
              return (
                <motion.circle
                  key={ring.label}
                  cx={CX}
                  cy={CY}
                  r={midR}
                  fill="none"
                  stroke={ring.color}
                  strokeWidth={thickness}
                  opacity={ringOpacity(i, isHovered)}
                  initial={{ r: 0, opacity: 0 }}
                  animate={{ r: midR, opacity: ringOpacity(i, isHovered) }}
                  transition={{ delay: 0.35 + i * 0.1, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
                  className="cursor-pointer"
                  style={{ transition: 'opacity 0.2s ease' }}
                  onMouseEnter={() => setHoveredRing(i)}
                  onMouseLeave={() => setHoveredRing(null)}
                />
              )
            })}

            {/* White backdrop circle behind center text */}
            <circle cx={CX} cy={CY} r={CENTER_R} fill="white" opacity={0.92} />

            {/* Center text: $87M */}
            <motion.g
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
            >
              <text
                x={CX}
                y={CY - 6}
                textAnchor="middle"
                dominantBaseline="central"
                className="font-body"
                style={{
                  fontSize: '48px',
                  fontWeight: 800,
                  fill: '#C9A84C',
                  letterSpacing: '-0.03em',
                  filter: 'drop-shadow(0 2px 4px rgba(15,26,46,0.25))',
                }}
              >
                $87M
              </text>
              <text
                x={CX}
                y={CY + 26}
                textAnchor="middle"
                dominantBaseline="central"
                className="font-body"
                style={{
                  fontSize: '10px',
                  fontWeight: 700,
                  fill: '#0F1A2E',
                  opacity: 0.5,
                  letterSpacing: '0.15em',
                  textTransform: 'uppercase',
                }}
              >
                Total TAM
              </text>
            </motion.g>
          </svg>

          {/* Hover tooltip — dark style matching slide 5's bar chart tooltip */}
          <AnimatePresence>
            {hoveredRing !== null && (
              <motion.div
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 4 }}
                transition={{ duration: 0.15 }}
                className="absolute pointer-events-none"
                style={{
                  zIndex: 20,
                  left: '50%',
                  top: 8,
                  transform: 'translateX(-50%)',
                }}
              >
                <div
                  className="rounded-lg px-4 py-3 max-w-[280px]"
                  style={{
                    backgroundColor: 'rgba(36,51,86,0.95)',
                    border: '1px solid transparent',
                  }}
                >
                  <p className="font-body text-[13px] font-semibold text-white">
                    {RING_CONFIG[hoveredRing].label}
                  </p>
                  <p className="font-body text-[12px] text-white/80 mt-0.5">
                    {RING_CONFIG[hoveredRing].amount}
                    <span className="text-white/50 ml-2">
                      Confidence: {RING_CONFIG[hoveredRing].confidence}
                    </span>
                  </p>
                  <p className="font-body text-[12px] text-white/70 mt-1 leading-snug">
                    {RING_CONFIG[hoveredRing].detail}
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Right: 5 channel cards — with colored left border + hover highlight */}
        <div className="flex flex-col gap-2.5 justify-center" style={{ width: '35%' }}>
          {RING_CONFIG.map((ring, i) => (
            <motion.div
              key={ring.label}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: 0.45 + i * 0.08 }}
              className="rounded-xl bg-white/80 backdrop-blur-sm px-4 py-4 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] transition-all duration-200 relative overflow-hidden"
              style={{
                borderColor: hoveredRing === i ? ring.color : undefined,
                boxShadow: hoveredRing === i
                  ? `0 0 0 1px ${ring.color}40, 0 2px 8px rgba(0,0,0,0.08)`
                  : '0 1px 3px rgba(0,0,0,0.04)',
              }}
              onMouseEnter={() => setHoveredRing(i)}
              onMouseLeave={() => setHoveredRing(null)}
            >
              {/* Left accent strip — thicker/brighter on hover */}
              <div
                className="absolute left-0 top-2 bottom-2 rounded-full transition-all duration-200"
                style={{
                  backgroundColor: ring.color,
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
            {RING_CONFIG.map((ring, i) => (
              <div key={ring.label} className="flex items-center gap-1.5">
                <div
                  className="w-2.5 h-2.5 rounded-full"
                  style={{
                    backgroundColor: ring.color,
                    opacity: BASE_OPACITIES[i],
                    border: `1px solid ${ring.color}`,
                  }}
                />
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
