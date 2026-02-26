import { useState } from 'react'
import { motion } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { FL_TAM_CHANNELS } from '../../data/market'

function fmtM(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`
  if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

// Five rings — outside-in: gold 20%, gold 35%, teal 40%, teal 60%, teal 80%
// Map to channels: State (biggest estimate) → Education → Micro-Purchase → Federal → Local
const RING_DATA = [
  { channel: 'State (MFMP + FL Agencies)', label: 'State', amount: '$20-30M', color: 'rgba(201,168,76,0.20)', idx: 2 },
  { channel: 'Education (67 Districts)', label: 'Education', amount: '$10-20M', color: 'rgba(201,168,76,0.35)', idx: 3 },
  { channel: 'Federal Micro-Purchases', label: 'Micro-Purchase', amount: '$8-15M', color: 'rgba(27,122,138,0.40)', idx: 1 },
  { channel: 'Federal (FPDS Visible)', label: 'Federal', amount: '$6.4M', color: 'rgba(27,122,138,0.60)', idx: 0 },
  { channel: 'Local (County/Municipal)', label: 'Local', amount: '$3-7M', color: 'rgba(27,122,138,0.80)', idx: 4 },
]

// Channel detail cards — one per ring, rich context
const CHANNEL_CARDS = [
  {
    label: 'State Agencies',
    amount: '$20-30M',
    detail: 'MFMP, corrections, FL agencies. Free registration.',
    dotColor: 'rgba(201,168,76,0.20)',
    dotBorder: '#C9A84C',
  },
  {
    label: 'Education',
    amount: '$10-20M',
    detail: '67 county districts, 2.8M students, NSLP funded.',
    dotColor: 'rgba(201,168,76,0.35)',
    dotBorder: '#C9A84C',
  },
  {
    label: 'Micro-Purchase',
    amount: '$8-15M',
    detail: '83% invisible in public databases.',
    dotColor: 'rgba(27,122,138,0.40)',
    dotBorder: '#1B7A8A',
  },
  {
    label: 'Federal FPDS',
    amount: '$6.4M',
    detail: '117 tracked contracts >$10K.',
    dotColor: 'rgba(27,122,138,0.60)',
    dotBorder: '#1B7A8A',
  },
  {
    label: 'Local / Municipal',
    amount: '$3-7M',
    detail: 'County jails, municipal facilities, DemandStar.',
    dotColor: 'rgba(27,122,138,0.80)',
    dotBorder: '#1B7A8A',
  },
]

// Concentric circle sizes — outermost to innermost (~30% larger)
const RING_SIZES = [500, 408, 316, 230, 150]
const CONTAINER = 520

export default function FloridaTamSlide() {
  const [hoveredRing, setHoveredRing] = useState(null)

  return (
    <div className="w-full h-full flex flex-col justify-center px-16 pt-6 pb-8 relative overflow-hidden">
      {/* Background decorative rings */}
      <BackgroundRing size={500} className="-top-40 -left-40" opacity={0.03} />
      <BackgroundRing size={300} className="bottom-16 -right-24" opacity={0.025} />

      {/* Header — compact top spacing */}
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

      {/* Main: circles left (~60%) + channel cards right (~35%) — tight gap */}
      <div className="flex gap-3 relative z-10 flex-1 min-h-0">

        {/* Concentric circles — float directly on background, no card */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex items-center justify-center"
          style={{ width: '60%' }}
        >
          <div className="relative" style={{ width: CONTAINER, height: CONTAINER }}>
            {RING_DATA.map((ring, i) => (
              <motion.div
                key={ring.label}
                initial={{ scale: 0.6, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.35 + i * 0.1, duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
                className="absolute rounded-full cursor-pointer transition-all duration-200"
                style={{
                  width: RING_SIZES[i],
                  height: RING_SIZES[i],
                  left: (CONTAINER - RING_SIZES[i]) / 2,
                  top: (CONTAINER - RING_SIZES[i]) / 2,
                  backgroundColor: ring.color,
                  filter: hoveredRing === i ? 'brightness(1.3)' : 'brightness(1)',
                }}
                onMouseEnter={() => setHoveredRing(i)}
                onMouseLeave={() => setHoveredRing(null)}
              />
            ))}

            {/* Ring labels — positioned on each ring */}
            {RING_DATA.map((ring, i) => {
              // Position labels at well-separated angles to avoid overlap
              const radius = RING_SIZES[i] / 2
              // Spread labels: top-left, top-right, left, right, bottom
              const angles = [-130, -40, 195, -10, 160]
              const angle = angles[i] * (Math.PI / 180)
              // Use larger offset for outer rings, smaller for inner
              const labelRadius = radius * (i < 2 ? 0.70 : 0.65)
              const x = CONTAINER / 2 + Math.cos(angle) * labelRadius
              const y = CONTAINER / 2 + Math.sin(angle) * labelRadius

              // Skip label for innermost ring (too small)
              if (i === 4) return null

              return (
                <motion.div
                  key={`label-${ring.label}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.8 + i * 0.08, duration: 0.4 }}
                  className="absolute pointer-events-none text-center"
                  style={{
                    left: x,
                    top: y,
                    transform: 'translate(-50%, -50%)',
                    zIndex: 5,
                  }}
                >
                  <span className="font-body text-[11px] font-semibold text-white/90 block leading-tight drop-shadow-[0_1px_2px_rgba(0,0,0,0.4)]">
                    {ring.label}
                  </span>
                  <span className="font-body text-[10px] text-white/70 block leading-tight drop-shadow-[0_1px_2px_rgba(0,0,0,0.4)]">
                    {ring.amount}
                  </span>
                </motion.div>
              )
            })}

            {/* Center: $87M */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.9, duration: 0.5 }}
              className="absolute inset-0 flex items-center justify-center"
              style={{ zIndex: 10 }}
            >
              <div className="text-center">
                <span className="font-body text-5xl font-bold tracking-tight block leading-none text-white drop-shadow-[0_1px_3px_rgba(0,0,0,0.3)]">
                  $87M
                </span>
                <span className="font-body text-[10px] font-semibold uppercase tracking-widest block mt-1.5 text-white/80 drop-shadow-[0_1px_2px_rgba(0,0,0,0.3)]">
                  Total TAM
                </span>
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Right: 5 compact channel cards */}
        <div className="flex flex-col gap-2.5 justify-center" style={{ width: '35%' }}>
          {CHANNEL_CARDS.map((card, i) => (
            <motion.div
              key={card.label}
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: 0.45 + i * 0.08 }}
              className="rounded-xl bg-white/80 backdrop-blur-sm px-4 py-3 shadow-[0_1px_3px_rgba(0,0,0,0.04)] transition-all duration-200"
              style={{
                borderWidth: 1,
                borderStyle: 'solid',
                borderColor: hoveredRing === i ? card.dotBorder : 'rgba(0,0,0,0.06)',
              }}
            >
              <div className="flex items-start gap-3">
                <div
                  className="w-3 h-3 rounded-full shrink-0 mt-1"
                  style={{ backgroundColor: card.dotColor, border: `1.5px solid ${card.dotBorder}` }}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="font-body text-sm font-semibold text-navy-950">
                      {card.label}
                    </span>
                    <span
                      className="font-body text-lg font-bold tracking-tight leading-none shrink-0"
                      style={{ color: '#1B7A8A' }}
                    >
                      {card.amount}
                    </span>
                  </div>
                  <p className="font-body text-xs text-navy-800/50 mt-0.5 leading-snug">
                    {card.detail}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom: channel dot legend + source + compass star */}
      <div className="flex items-center justify-between mt-3 relative z-10">
        <div>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="flex items-center gap-4 mb-1"
          >
            {RING_DATA.map((ring) => (
              <div key={ring.label} className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: ring.color, border: `1px solid ${ring.idx < 2 ? '#C9A84C' : '#1B7A8A'}` }} />
                <span className="font-body text-[10px] text-navy-800/40">{ring.label}</span>
              </div>
            ))}
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="text-[10px] text-navy-800/35"
          >
            USASpending API FY2024 | FL MFMP | FL DOE, USDA NSLP | County procurement
          </motion.p>
        </div>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
