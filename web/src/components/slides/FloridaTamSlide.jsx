import { useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'

// Ring data — outside-in, sized proportional to dollar value midpoint
const RING_CONFIG = [
  { label: 'State', amount: '$20-30M', confidence: 'MEDIUM', detail: 'MFMP + corrections + FL agencies. Free registration. Largest single channel.', color: '#C9A84C', midVal: 25 },
  { label: 'Education', amount: '$15-25M', confidence: 'MEDIUM', detail: '67 county districts, 2.8M students. Small district contracts under $350K. NSLP funded.', color: '#E8913A', midVal: 20 },
  { label: 'Micro-Purchase', amount: '$8-15M', confidence: 'HIGH', detail: '83% invisible in public databases. Below $15K threshold — no competitive bidding required. Fastest path to first contract.', color: '#1B7A8A', midVal: 12 },
  { label: 'Federal FPDS', amount: '$6.4M', confidence: 'HIGH', detail: '117 tracked contracts >$10K. The visible tip of the iceberg.', color: '#239BAD', midVal: 6.4 },
  { label: 'Local / Municipal', amount: '$8-15M', confidence: 'MEDIUM', detail: 'County jails (30-50 rebids/yr), municipal facilities. DemandStar + VendorLink portals.', color: '#6366f1', midVal: 11.5 },
]

// SVG ring geometry — larger chart with more center breathing room
const SVG_SIZE = 560
const CX = SVG_SIZE / 2
const CY = SVG_SIZE / 2
const OUTER_R = 260
const CENTER_R = 80
const RING_GAP = 5
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

// Opacity levels for rings — higher contrast
const BASE_OPACITIES = [0.70, 0.75, 0.80, 0.85, 0.90]
const HOVER_OPACITIES = [0.90, 0.92, 0.95, 0.95, 1.0]
function ringOpacity(index, isHovered) {
  return isHovered ? HOVER_OPACITIES[index] : BASE_OPACITIES[index]
}

export default function FloridaTamSlide() {
  const [hoveredRing, setHoveredRing] = useState(null)

  return (
    <div className="w-full h-full flex flex-col px-12 lg:px-14 pt-4 pb-3 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -left-40" opacity={0.03} />

      {/* Header */}
      <div className="mb-2 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-1"
        >
          Florida Total Addressable Market
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          $90M Year 1 Accessible Market
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600 max-w-2xl"
        >
          Contracts under $350K that Newport can pursue from day one. The full Florida food procurement market exceeds $1.1B.
        </motion.p>
        <GoldLine width={60} className="mt-1.5" delay={0.25} />
      </div>

      {/* Main: circles left (~58%) + channel cards right (~38%) */}
      <div className="flex gap-4 relative z-10 flex-1 min-h-0">

        {/* Concentric circles — SVG annular rings */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center justify-center relative"
          style={{ width: '58%' }}
        >
          <svg
            width={SVG_SIZE}
            height={SVG_SIZE}
            viewBox={`0 0 ${SVG_SIZE} ${SVG_SIZE}`}
            className="overflow-visible"
            style={{ maxWidth: '100%', maxHeight: '100%' }}
          >
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
            <circle cx={CX} cy={CY} r={CENTER_R} fill="white" opacity={0.95} />

            {/* Center text: $87M — with more room */}
            <motion.g
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
            >
              <text
                x={CX}
                y={CY - 8}
                textAnchor="middle"
                dominantBaseline="central"
                className="font-body"
                style={{
                  fontSize: '52px',
                  fontWeight: 700,
                  fill: '#C9A84C',
                  letterSpacing: '-0.03em',
                }}
              >
                $90M
              </text>
              <text
                x={CX}
                y={CY + 28}
                textAnchor="middle"
                dominantBaseline="central"
                className="font-body"
                style={{
                  fontSize: '11px',
                  fontWeight: 600,
                  fill: '#71717a',
                  letterSpacing: '0.15em',
                  textTransform: 'uppercase',
                }}
              >
                Y1 Accessible
              </text>
            </motion.g>
          </svg>

          {/* Hover tooltip */}
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
                  className="rounded-xl px-4 py-3 max-w-[300px]"
                  style={{
                    backgroundColor: '#18181b',
                    border: '1px solid transparent',
                  }}
                >
                  <p className="font-body text-[14px] font-semibold text-white">
                    {RING_CONFIG[hoveredRing].label}
                  </p>
                  <p className="font-body text-[13px] text-white/80 mt-0.5">
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

        {/* Right: 5 channel cards */}
        <div className="flex flex-col gap-2.5 justify-center" style={{ width: '38%' }}>
          {RING_CONFIG.map((ring, i) => (
            <motion.div
              key={ring.label}
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: 0.45 + i * 0.08 }}
              className="rounded-xl bg-white px-5 py-4 shadow-sm border border-zinc-200 transition-all duration-200 relative overflow-hidden"
              style={{
                borderColor: hoveredRing === i ? ring.color : undefined,
                boxShadow: hoveredRing === i
                  ? `0 0 0 1px ${ring.color}40, 0 2px 8px rgba(0,0,0,0.08)`
                  : undefined,
              }}
              onMouseEnter={() => setHoveredRing(i)}
              onMouseLeave={() => setHoveredRing(null)}
            >
              {/* Left accent strip */}
              <div
                className="absolute left-0 top-2 bottom-2 rounded-full transition-all duration-200"
                style={{
                  backgroundColor: ring.color,
                  width: hoveredRing === i ? 4 : 3,
                  opacity: hoveredRing === i ? 1 : 0.8,
                }}
              />
              <div className="flex items-start gap-3 pl-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="font-body text-sm font-bold text-zinc-950">
                      {ring.label}
                    </span>
                    <span
                      className="font-body text-xl font-bold tracking-tight leading-none shrink-0"
                      style={{ color: ring.color }}
                    >
                      {ring.amount}
                    </span>
                  </div>
                  <p className="font-body text-[13px] text-zinc-600 mt-1 leading-snug">
                    {ring.detail}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom: legend + source */}
      <div className="flex items-center justify-between mt-2 relative z-10">
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
                  className="w-3 h-3 rounded-full"
                  style={{
                    backgroundColor: ring.color,
                    opacity: BASE_OPACITIES[i],
                    border: `1px solid ${ring.color}`,
                  }}
                />
                <span className="font-body text-[12px] text-zinc-600">{ring.label}</span>
              </div>
            ))}
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="text-[10px] text-zinc-400"
          >
            USASpending API FY2024 | FL MFMP | FL DOE, USDA NSLP | County procurement
          </motion.p>
        </div>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
