import { motion } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { COMPETITORS } from '../../data/market'

const topTier = COMPETITORS.filter(c => c.tier === 'top')
const midTier = COMPETITORS.filter(c => c.tier === 'mid')
const targetTier = COMPETITORS.filter(c => c.tier === 'target')

function fmtM(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

function tierLeftBorder(tier) {
  if (tier === 'top') return '#C9A84C'
  if (tier === 'mid') return '#1B7A8A'
  return 'transparent'
}

function TierBadge({ tier }) {
  if (tier === 'top') {
    return (
      <span className="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-[10px] font-semibold" style={{ backgroundColor: 'rgba(201,168,76,0.10)', color: '#C9A84C' }}>
        Top Tier
      </span>
    )
  }
  if (tier === 'mid') {
    return (
      <span className="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-[10px] font-semibold" style={{ backgroundColor: 'rgba(27,122,138,0.10)', color: '#1B7A8A' }}>
        Mid Tier
      </span>
    )
  }
  return null
}

function TierLabel({ children }) {
  return (
    <div className="px-6 py-2 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
      <span className="font-body text-[10px] font-semibold uppercase tracking-widest text-navy-800/30">
        {children}
      </span>
    </div>
  )
}

function CompetitorRow({ c, i, baseDelay }) {
  return (
    <motion.div
      key={c.rank}
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: baseDelay + i * 0.06, duration: 0.3 }}
      className={`grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-l-[3px] border-b border-black/[0.06] ${
        i % 2 === 0 ? 'bg-navy-950/[0.02]' : 'bg-transparent'
      }`}
      style={{ borderLeftColor: tierLeftBorder(c.tier) }}
    >
      {/* Rank — centered */}
      <span className="font-body text-base font-semibold text-center text-navy-800/50">
        #{c.rank}
      </span>

      {/* Company — left-aligned */}
      <span className={`font-body text-base ${
        c.tier === 'top' ? 'font-semibold text-navy-950' : 'text-navy-800/70'
      }`}>
        {c.company}
        <TierBadge tier={c.tier} />
      </span>

      {/* Amount — left-aligned */}
      <span className={`font-body text-base font-bold tracking-tight ${
        c.rank === 1 ? '' : c.tier === 'top' ? 'text-navy-950' : c.tier === 'mid' ? 'text-navy-950' : 'text-navy-800/60'
      }`} style={c.rank === 1 ? { color: '#C9A84C' } : undefined}>
        {fmtM(c.amount)}
      </span>

      {/* Notes — left-aligned */}
      <span className="font-body text-sm text-navy-800/50">
        {c.notes}
      </span>
    </motion.div>
  )
}

function NewportCalloutRow() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.95, duration: 0.4 }}
      className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-5 border-l-[4px] border-b border-black/[0.06]"
      style={{ backgroundColor: 'rgba(27,122,138,0.06)', borderLeftColor: '#C9A84C' }}
    >
      <span className="font-body text-base font-bold text-center" style={{ color: '#1B7A8A' }}>
        →
      </span>
      <span className="font-body text-base font-bold" style={{ color: '#1B7A8A' }}>
        Newport Wholesalers
        <span className="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-[10px] font-semibold" style={{ backgroundColor: 'rgba(201,168,76,0.10)', color: '#C9A84C' }}>
          Entry
        </span>
      </span>
      <span className="font-body text-base font-bold tracking-tight" style={{ color: '#C9A84C' }}>
        $1-5M
      </span>
      <span className="font-body text-sm text-navy-800/60">
        30-year track record · Cold chain · Plantation, FL
      </span>
    </motion.div>
  )
}

export default function CompetitionSlide() {
  return (
    <div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
      <BackgroundRing size={400} className="-top-32 -right-32" opacity={0.03} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-navy-800/40 mb-3"
        >
          Competitive Analysis
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          The Competitive Field
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-navy-800/60 max-w-2xl"
        >
          The top is locked — but Newport enters with more infrastructure than anyone in the $1-5M tier.
        </motion.p>
        <GoldLine width={60} className="mt-3" delay={0.25} />
      </div>

      {/* Table card — fills remaining space */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.45 }}
        className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] overflow-hidden relative z-10 flex-1"
      >
        {/* Table header — centered text */}
        <div
          className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-b-2 border-black/[0.10]"
          style={{ backgroundColor: 'rgba(15,26,46,0.05)' }}
        >
          <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Rank</span>
          <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Company</span>
          <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">FL Gov Awards</span>
          <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Notes</span>
        </div>

        {/* National Leaders */}
        <TierLabel>— National Leaders —</TierLabel>
        {topTier.map((c, i) => (
          <CompetitorRow key={c.rank} c={c} i={i} baseDelay={0.4} />
        ))}

        {/* Regional Mid-Market */}
        <TierLabel>— Regional Mid-Market —</TierLabel>
        {midTier.map((c, i) => (
          <CompetitorRow key={c.rank} c={c} i={i} baseDelay={0.55} />
        ))}

        {/* Newport's Competitive Tier */}
        <TierLabel>— Newport's Competitive Tier —</TierLabel>
        {/* Rainmaker first — the direct competitor */}
        <CompetitorRow c={targetTier[0]} i={0} baseDelay={0.7} />

        {/* Newport callout — inline after Rainmaker */}
        <NewportCalloutRow />

        {/* Remaining target tier */}
        {targetTier.slice(1).map((c, i) => (
          <CompetitorRow key={c.rank} c={c} i={i + 1} baseDelay={0.75} />
        ))}
      </motion.div>

      {/* Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-[10px] text-navy-800/35"
        >
          USASpending API, FY2024 FL food contracts under $350K
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.4} />
      </div>
    </div>
  )
}
