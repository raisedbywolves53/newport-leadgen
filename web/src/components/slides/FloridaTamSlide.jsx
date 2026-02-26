import { motion } from 'motion/react'
import SourceCitation from '../ui/SourceCitation'

// Concentric circle layers — ordered outermost (largest) to innermost (smallest)
// Sized using sqrt-of-cumulative scaling so ring widths reflect channel value
const CONTAINER = 380
const CIRCLE_LAYERS = [
  { color: '#239BAD', size: 380 }, // State — outermost
  { color: '#3CC0D4', size: 310 }, // Education
  { color: '#E8913A', size: 240 }, // Micro-Purchase
  { color: '#1B7A8A', size: 168 }, // Federal (FPDS)
  { color: '#243356', size: 108 }, // Local — innermost (navy-800)
]

// Channel breakdown — matches circle order (outside → inside)
const CHANNELS = [
  { name: 'State Agencies', amount: 'Est. $20-30M', detail: 'MFMP, corrections, state agencies', color: '#239BAD' },
  { name: 'Education (67 Dist.)', amount: 'Est. $10-20M', detail: 'School districts, NSLP funded', color: '#3CC0D4' },
  { name: 'Federal Micro-Purchase', amount: '$8-15M', detail: '83% invisible in public databases', color: '#E8913A' },
  { name: 'Federal (FPDS Visible)', amount: '$6.4M', detail: '117 tracked contracts >$10K', color: '#1B7A8A' },
  { name: 'County / Local', amount: 'Est. $3-7M', detail: 'Jails, municipal, local gov', color: '#243356' },
]

// Key insight callouts — the "so what" narrative
const INSIGHTS = [
  { value: '83%', label: 'Below Micro-Purchase', detail: 'No competitive bidding under $15K — fastest path to first contract', accent: '#E8913A' },
  { value: '$6.4M', label: 'Visible in FPDS Today', detail: '117 FL contracts tracked — the tip of the iceberg', accent: '#1B7A8A' },
  { value: '5', label: 'Procurement Portals', detail: 'Each channel has its own registration and bidding process', accent: '#C9A84C' },
]

export default function FloridaTamSlide() {
  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-16 pt-5 pb-24 max-w-7xl mx-auto relative">

      {/* Title block — sized to command attention */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <span className="font-body text-[10px] font-semibold text-navy-800/40 uppercase tracking-widest">
          Florida Total Addressable Market
        </span>
        <h2 className="font-body text-[2.75rem] leading-[1.1] font-bold tracking-tight text-navy-950 mt-1">
          Five Channels to Market
        </h2>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-sm text-navy-800/50 mt-1 mb-2"
      >
        Federal is the entry point — state, education, and local expand the opportunity.
      </motion.p>

      <motion.div
        initial={{ width: 0 }}
        animate={{ width: 48 }}
        transition={{ duration: 0.8, delay: 0.25 }}
        className="h-px mb-3"
        style={{ backgroundColor: '#C9A84C' }}
      />

      {/* Main content — 3-zone dashboard layout */}
      <div className="flex-1 min-h-0 grid grid-cols-[165px_1fr_245px] gap-5 items-center">

        {/* LEFT: Channel breakdown legend */}
        <div className="flex flex-col gap-3">
          {CHANNELS.map((ch, i) => (
            <motion.div
              key={ch.name}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + i * 0.1, duration: 0.4 }}
              className="flex items-start gap-2"
            >
              <div
                className="w-2.5 h-2.5 rounded-full mt-[3px] shrink-0"
                style={{ backgroundColor: ch.color }}
              />
              <div>
                <span className="font-body text-[11px] font-semibold text-navy-950 block leading-tight">
                  {ch.name}
                </span>
                <span
                  className="font-body text-[13px] font-bold block mt-px"
                  style={{ color: ch.color }}
                >
                  {ch.amount}
                </span>
                <span className="font-body text-[9px] text-navy-800/40 block mt-px leading-tight">
                  {ch.detail}
                </span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* CENTER: Concentric circles — the visual anchor */}
        <div className="flex items-center justify-center">
          <div className="relative" style={{ width: CONTAINER, height: CONTAINER }}>

            {/* Circles — back to front, largest first */}
            {CIRCLE_LAYERS.map((layer, i) => (
              <motion.div
                key={i}
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{
                  delay: 0.25 + i * 0.12,
                  duration: 0.6,
                  ease: [0.25, 0.1, 0.25, 1],
                }}
                className="absolute rounded-full"
                style={{
                  width: layer.size,
                  height: layer.size,
                  backgroundColor: layer.color,
                  left: (CONTAINER - layer.size) / 2,
                  top: (CONTAINER - layer.size) / 2,
                }}
              />
            ))}

            {/* Center hero: $87M */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.0, duration: 0.5 }}
              className="absolute inset-0 flex items-center justify-center"
              style={{ zIndex: 10 }}
            >
              <div className="text-center">
                <span className="font-body text-[2.5rem] font-bold text-white tracking-tight block leading-none">
                  $87M
                </span>
                <span className="font-body text-[9px] font-semibold text-white/50 uppercase tracking-widest block mt-1">
                  Total TAM
                </span>
              </div>
            </motion.div>

            {/* Ring amount labels — positioned on each visible ring area */}
            {/* State ring — top */}
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2 }}
              className="absolute font-body text-[11px] font-bold text-white/80"
              style={{ top: 14, left: '50%', transform: 'translateX(-50%)' }}
            >
              $20-30M
            </motion.span>

            {/* Education ring — upper right */}
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.3 }}
              className="absolute font-body text-[11px] font-bold text-white/80"
              style={{ top: 52, right: 56 }}
            >
              $10-20M
            </motion.span>

            {/* Micro ring — right */}
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.4 }}
              className="absolute font-body text-[11px] font-bold text-white/90"
              style={{ top: CONTAINER / 2 - 6, right: 78 }}
            >
              $8-15M
            </motion.span>

            {/* Federal ring — lower left */}
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.5 }}
              className="absolute font-body text-[10px] font-bold text-white/70"
              style={{ bottom: 88, left: 82 }}
            >
              $6.4M
            </motion.span>
          </div>
        </div>

        {/* RIGHT: Key insight cards */}
        <div className="flex flex-col gap-3 justify-center">
          {INSIGHTS.map((insight, i) => (
            <motion.div
              key={insight.label}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.45, delay: 0.6 + i * 0.15 }}
              className={`rounded-xl p-4 ${
                i === 0
                  ? 'border border-amber-500/20 bg-amber-500/[0.06]'
                  : i === 1
                  ? 'border border-teal-500/20 bg-teal-500/[0.06]'
                  : 'bg-white/60 backdrop-blur-sm border border-black/[0.05]'
              }`}
            >
              <span
                className="font-body text-2xl font-bold tracking-tight leading-none block mb-1"
                style={{ color: insight.accent }}
              >
                {insight.value}
              </span>
              <span className="font-body text-xs font-semibold text-navy-950 block mb-0.5">
                {insight.label}
              </span>
              <span className="font-body text-[11px] text-navy-800/50 leading-relaxed block">
                {insight.detail}
              </span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Confidence footnote */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6 }}
        className="font-body text-[10px] text-navy-800/35 mt-2"
      >
        Federal: HIGH confidence (API data) · State/Education/Local: MEDIUM confidence (estimates)
      </motion.p>

      <SourceCitation>
        Federal: USASpending API FY2024 (Feb 2026) | State: FL MFMP | Education: FL DOE, USDA NSLP | Local: County procurement
      </SourceCitation>
    </div>
  )
}
