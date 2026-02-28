import { useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import { TrendingUp, Shield } from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'

// Ring data — outside-in, sized proportional to dollar value midpoint
const RING_CONFIG = [
  { label: 'State', amount: '$20-30M', confidence: 'MEDIUM', detail: 'MFMP + corrections + FL agencies. Free registration. Largest single channel.', color: '#C9A84C', midVal: 25 },
  { label: 'Education', amount: '$10-20M', confidence: 'MEDIUM', detail: '67 county districts, 2.8M students. NSLP funded. Second largest opportunity.', color: '#C9A84C', midVal: 15 },
  { label: 'Micro-Purchase', amount: '$8-15M', confidence: 'HIGH', detail: '83% invisible in public databases. Below $15K threshold — no competitive bidding required. Fastest path to first contract.', color: '#1B7A8A', midVal: 12 },
  { label: 'Federal FPDS', amount: '$6.4M', confidence: 'HIGH', detail: '117 tracked contracts >$10K. The visible tip of the iceberg.', color: '#1B7A8A', midVal: 6.4 },
  { label: 'Local / Municipal', amount: '$3-7M', confidence: 'MEDIUM', detail: 'County jails, municipal facilities. DemandStar + VendorLink portals.', color: '#1B7A8A', midVal: 5 },
]

// SVG ring geometry
const SVG_SIZE = 380
const CX = SVG_SIZE / 2
const CY = SVG_SIZE / 2
const OUTER_R = 170
const CENTER_R = 44
const RING_GAP = 4
const TOTAL_VAL = RING_CONFIG.reduce((s, r) => s + r.midVal, 0)
const USABLE = OUTER_R - CENTER_R - RING_GAP * (RING_CONFIG.length - 1)

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

const BASE_OPACITIES = [0.45, 0.55, 0.60, 0.70, 0.82]
const HOVER_OPACITIES = [0.65, 0.75, 0.80, 0.88, 0.95]
function ringOpacity(index, isHovered) {
  return isHovered ? HOVER_OPACITIES[index] : BASE_OPACITIES[index]
}

// Collapse 5 channels to 4 stat cards
const STAT_CARDS = [
  {
    label: 'State Procurement',
    value: '$20–30M',
    accent: '#C9A84C',
    badge: { text: 'MEDIUM', variant: 'text-zinc-600' },
    footerHighlight: 'MFMP + corrections + FL agencies',
    footerDescription: 'Largest single channel',
  },
  {
    label: 'Education / NSLP',
    value: '$10–20M',
    accent: '#C9A84C',
    badge: { text: 'MEDIUM', variant: 'text-zinc-600' },
    footerHighlight: '67 county districts, 2.8M students',
    footerDescription: 'NSLP funded',
  },
  {
    label: 'Micro-Purchase',
    value: '$8–15M',
    accent: '#1B7A8A',
    badge: { icon: TrendingUp, text: 'HIGH', variant: 'text-emerald-700' },
    footerHighlight: '83% invisible in databases',
    footerDescription: 'Below $15K — no bid required',
  },
  {
    label: 'Federal + Local',
    value: '$9.4M',
    accent: '#1B7A8A',
    badge: { icon: Shield, text: 'HIGH', variant: 'text-emerald-700' },
    footerHighlight: '117 tracked contracts + county jails',
    footerDescription: 'Visible tip + municipal',
  },
]

export default function FloridaTamSlide() {
  const [hoveredRing, setHoveredRing] = useState(null)

  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      {/* ZONE 1: Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block text-xs font-medium uppercase tracking-widest text-zinc-400 mb-3"
        >
          Florida Total Addressable Market
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          $87M Market, Five Layers Deep
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          Federal is the entry point — state, education, and local expand the
          opportunity.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — 4 channels HORIZONTAL */}
      <div className="grid grid-cols-4 gap-4 mb-4 relative z-10">
        {STAT_CARDS.map((stat, i) => {
          const BadgeIcon = stat.badge.icon
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ y: -2 }}
              transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-6 py-6 cursor-default"
            >
              <div className="px-6 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500">{stat.label}</span>
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 ${stat.badge.variant}`}
                  >
                    {BadgeIcon && <BadgeIcon className="w-3 h-3" />}
                    {stat.badge.text}
                  </span>
                </div>
                <span
                  className="text-2xl font-semibold tabular-nums tracking-tight"
                  style={{ color: stat.accent }}
                >
                  {stat.value}
                </span>
              </div>
              <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
                <div className="flex items-center gap-2 font-medium text-zinc-900">
                  {stat.footerHighlight}
                </div>
                <div className="text-zinc-500 text-xs">
                  {stat.footerDescription}
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* ZONE 3: ChartCard — full-width concentric rings */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out relative overflow-hidden flex flex-col z-10"
        style={{ height: '300px' }}
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

        {/* CardHeader */}
        <div className="p-6 pb-0 pl-8">
          <h3 className="text-lg font-semibold text-zinc-950">TAM by Channel</h3>
          <p className="text-sm text-zinc-500 mt-1">
            FL Government Food Procurement — $87M Total
          </p>
        </div>

        {/* CardContent: SVG rings */}
        <div className="flex-1 min-h-0 flex items-center justify-center px-4 relative">
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
            <circle cx={CX} cy={CY} r={CENTER_R} fill="white" opacity={0.92} />
            <motion.g
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
            >
              <text
                x={CX} y={CY - 4}
                textAnchor="middle" dominantBaseline="central"
                style={{ fontSize: '32px', fontWeight: 700, fill: '#C9A84C', letterSpacing: '-0.03em', fontFamily: 'Inter, system-ui, sans-serif' }}
              >
                $87M
              </text>
              <text
                x={CX} y={CY + 18}
                textAnchor="middle" dominantBaseline="central"
                style={{ fontSize: '9px', fontWeight: 600, fill: '#71717a', letterSpacing: '0.15em', textTransform: 'uppercase', fontFamily: 'Inter, system-ui, sans-serif' }}
              >
                Total TAM
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
                className="absolute pointer-events-none z-20"
                style={{ left: '50%', top: 12, transform: 'translateX(-50%)' }}
              >
                <div className="rounded-lg px-4 py-3 max-w-[280px]" style={{ backgroundColor: '#18181b', border: '1px solid #27272a' }}>
                  <p className="text-[13px] font-semibold text-zinc-50">{RING_CONFIG[hoveredRing].label}</p>
                  <p className="text-xs text-zinc-300 mt-0.5">
                    {RING_CONFIG[hoveredRing].amount}
                    <span className="text-zinc-500 ml-2">Confidence: {RING_CONFIG[hoveredRing].confidence}</span>
                  </p>
                  <p className="text-xs text-zinc-400 mt-1 leading-snug">{RING_CONFIG[hoveredRing].detail}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* CardFooter: legend */}
        <div className="px-6 pb-4 pt-3 pl-8 border-t border-zinc-100 flex items-center gap-4 flex-wrap">
          {RING_CONFIG.map((ring, i) => (
            <div key={ring.label} className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: ring.color, opacity: BASE_OPACITIES[i] }} />
              <span className="text-xs text-zinc-500">{ring.label}</span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* ZONE 5: Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-[10px] text-zinc-300"
        >
          USASpending API FY2024 | FL MFMP | FL DOE, USDA NSLP | County procurement portals
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
