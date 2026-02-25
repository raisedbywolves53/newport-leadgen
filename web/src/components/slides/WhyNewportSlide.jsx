import { motion } from 'motion/react'
import { Shield, Building2, TrendingDown, Truck } from 'lucide-react'

const pillars = [
  {
    icon: Building2,
    stat: '30',
    unit: 'Years',
    headline: 'Continuous Operations',
    detail: 'Real warehouse in Plantation, FL. Real fleet. Real W-2 workforce — the verifiable history agencies now require.',
    accent: '#C9A84C',
    hero: true,
  },
  {
    icon: TrendingDown,
    stat: '1,091',
    unit: 'Firms Suspended',
    headline: 'Post-Fraud Vacuum',
    detail: 'SBA cleared 25% of the 8(a) program in Jan 2026. DOJ prosecuted a $550M scheme. Agencies need clean vendors.',
    accent: '#C9A84C',
  },
  {
    icon: Shield,
    stat: '83%',
    unit: 'Micro-Purchase',
    headline: 'Below the Threshold',
    detail: 'Of FL food contracts fall under $15K — no competitive bidding, no past performance needed. Win on day one.',
    accent: '#1B7A8A',
  },
  {
    icon: Truck,
    stat: '$5M',
    unit: 'Entry Tier',
    headline: 'Infrastructure Edge',
    detail: 'FL competitors #5–10 do $1–5M with less capability. Newport enters with trucks, cold chain, and routes.',
    accent: '#1B7A8A',
  },
]

function HeroCard({ pillar }) {
  const Icon = pillar.icon
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="row-span-2 rounded-2xl bg-white p-10 shadow-[0_2px_8px_rgba(0,0,0,0.06)] border border-black/[0.04] flex flex-col justify-center relative overflow-hidden"
    >
      {/* Subtle gold accent strip */}
      <div className="absolute left-0 top-8 bottom-8 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />

      <div className="pl-4">
        <div
          className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
          style={{ backgroundColor: '#C9A84C15' }}
        >
          <Icon className="w-6 h-6" style={{ color: '#C9A84C' }} strokeWidth={1.8} />
        </div>

        <div className="flex items-baseline gap-3 mb-2">
          <span className="font-body text-7xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
            {pillar.stat}
          </span>
          <span className="font-body text-lg font-medium text-navy-800/35 uppercase tracking-wide">
            {pillar.unit}
          </span>
        </div>

        <h3 className="font-body text-xl font-semibold text-navy-950 mt-4 mb-3">
          {pillar.headline}
        </h3>

        <p className="font-body text-[15px] leading-relaxed text-navy-800/70">
          {pillar.detail}
        </p>

        <div className="flex items-center gap-2 mt-5 pt-5 border-t border-black/[0.06]">
          <span className="font-body text-xs font-medium text-navy-800/45">Since 1996</span>
          <span className="text-navy-800/25">·</span>
          <span className="font-body text-xs font-medium text-navy-800/45">Plantation, FL</span>
        </div>
      </div>
    </motion.div>
  )
}

function StatCard({ pillar, index }) {
  const Icon = pillar.icon
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay: 0.4 + index * 0.1 }}
      className="rounded-2xl bg-white p-8 shadow-[0_1px_4px_rgba(0,0,0,0.05)] border border-black/[0.04] flex flex-col justify-center"
    >
      <div className="flex items-start gap-5">
        <div
          className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0"
          style={{ backgroundColor: `${pillar.accent}12` }}
        >
          <Icon className="w-5 h-5" style={{ color: pillar.accent }} strokeWidth={1.8} />
        </div>
        <div className="flex-1">
          <div className="flex items-baseline gap-2 mb-1">
            <span
              className="font-body text-3xl font-bold tracking-tight leading-none"
              style={{ color: pillar.accent }}
            >
              {pillar.stat}
            </span>
            <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide">
              {pillar.unit}
            </span>
          </div>
          <h3 className="font-body text-base font-semibold text-navy-950 mb-1.5">
            {pillar.headline}
          </h3>
          <p className="font-body text-sm leading-relaxed text-navy-800/65">
            {pillar.detail}
          </p>
        </div>
      </div>
    </motion.div>
  )
}

export default function WhyNewportSlide() {
  const hero = pillars[0]
  const rest = pillars.slice(1)

  return (
    <div className="w-full h-full flex flex-col justify-center px-20 pb-16">
      {/* Header */}
      <div className="mb-8">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-[#1B7A8A] mb-3"
        >
          Competitive Moat
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          Why Newport Wins
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-navy-800/60 max-w-2xl"
        >
          A 30-year track record can't be manufactured. In the current post-fraud environment,
          agencies need vendors with auditable, transparent histories.
        </motion.p>
      </div>

      {/* Bento grid: hero left (2 rows) + 3 cards stacked right */}
      <div className="grid grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr] gap-5" style={{ height: '460px' }}>
        <HeroCard pillar={hero} />
        {rest.map((p, i) => (
          <StatCard key={p.headline} pillar={p} index={i} />
        ))}
      </div>

      {/* Source */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.0 }}
        className="text-[10px] text-navy-800/35 mt-4"
      >
        SBA.gov (Jan 28 2026) · DOJ OPA (Jun 12 2025) · USASpending FY2024
      </motion.p>
    </div>
  )
}
