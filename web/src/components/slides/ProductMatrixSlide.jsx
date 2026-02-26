import { motion } from 'motion/react'
import { Star, TrendingUp, Shield, AlertTriangle } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { PRODUCT_TIERS } from '../../data/market'

function fmtM(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

export default function ProductMatrixSlide() {
  const produce = PRODUCT_TIERS.tier1[1]       // PSC 8915 — biggest FL spend
  const confectionery = PRODUCT_TIERS.tier1[0]  // PSC 8925 — highest Newport fit

  return (
    <div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
      {/* Background decorative rings */}
      <BackgroundRing size={450} className="-top-36 -right-36" opacity={0.03} />
      <BackgroundRing size={280} className="bottom-16 -left-24" opacity={0.025} />

      {/* Header — matches WhyNewport pattern */}
      <div className="mb-6 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-teal-500 mb-3"
        >
          Product Categories
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          Product Opportunity Matrix
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-navy-800/60 max-w-2xl"
        >
          Prioritized by FL demand, competition level, and Newport's pricing advantage.
        </motion.p>
        <GoldLine width={60} className="mt-4" delay={0.25} />
      </div>

      {/* Bento grid — hero left (2 rows) + 3 cards stacked right */}
      <div className="grid grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr] gap-5 relative z-10" style={{ height: '460px' }}>

        {/* HERO — Fresh Produce: biggest FL market */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="row-span-2 rounded-2xl bg-white p-10 shadow-[0_2px_8px_rgba(0,0,0,0.06)] border border-black/[0.04] flex flex-col justify-center relative overflow-hidden"
        >
          {/* Gold accent strip */}
          <div className="absolute left-0 top-8 bottom-8 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />

          <div className="pl-4">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
              style={{ backgroundColor: '#C9A84C15' }}
            >
              <Star className="w-6 h-6" style={{ color: '#C9A84C' }} strokeWidth={1.8} />
            </div>

            <div className="flex items-baseline gap-3 mb-2">
              <span className="font-body text-7xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
                {fmtM(produce.flSpend)}
              </span>
              <span className="font-body text-lg font-medium text-navy-800/35 uppercase tracking-wide">
                FL Spend
              </span>
            </div>

            <h3 className="font-body text-xl font-semibold text-navy-950 mt-4 mb-3">
              {produce.name}
              <span className="ml-2 text-[10px] font-bold text-white bg-teal-500 px-1.5 py-0.5 rounded-md align-middle">
                TIER 1
              </span>
            </h3>

            <p className="font-body text-[15px] leading-relaxed text-navy-800/70">
              {produce.advantage}
            </p>

            <div className="flex items-center gap-4 mt-5 pt-5 border-t border-black/[0.06]">
              <span className="font-body text-xs font-medium text-navy-800/45">PSC {produce.psc}</span>
              <span className="text-navy-800/25">&middot;</span>
              <span className="font-body text-xs font-medium text-teal-400">{produce.soleSource}% sole-source</span>
              <span className="text-navy-800/25">&middot;</span>
              <span className="font-body text-xs font-medium text-navy-800/45">{produce.govMarkup} markup</span>
            </div>
          </div>
        </motion.div>

        {/* Confectionery — Newport's unique edge (callout card, amber) */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.4 }}
          className="rounded-xl border border-amber-500/20 bg-amber-500/[0.06] p-5 flex flex-col justify-center relative overflow-hidden"
        >
          <span className="absolute top-3 right-3 text-[9px] font-bold text-white bg-amber-500 px-1.5 py-0.5 rounded-md">
            HIGHEST FIT
          </span>
          <div className="flex items-start gap-4">
            <div
              className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
              style={{ backgroundColor: '#E8913A15' }}
            >
              <Star className="w-5 h-5 text-amber-400" strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <div className="flex items-baseline gap-2 mb-1">
                <span className="font-body text-3xl font-bold tracking-tight leading-none text-amber-500">
                  {fmtM(confectionery.nationalSpend)}
                </span>
                <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide">
                  National
                </span>
              </div>
              <h3 className="font-body text-base font-semibold text-navy-950 mb-1.5">
                {confectionery.name}
              </h3>
              <p className="font-body text-sm leading-relaxed text-navy-800/65">
                {confectionery.advantage}. {confectionery.soleSource}% sole-source.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Tier 2 — Growth Targets (standard card) */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.5 }}
          className="rounded-2xl bg-white/70 backdrop-blur-sm p-5 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] flex flex-col justify-center"
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-teal-500/15 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-teal-400" strokeWidth={1.5} />
            </div>
            <span className="font-body text-xs font-semibold text-teal-400 uppercase tracking-wider">
              Tier 2 — Growth
            </span>
          </div>
          <div className="space-y-2.5">
            {PRODUCT_TIERS.tier2.map((p) => (
              <div key={p.psc} className="flex items-center justify-between">
                <span className="font-body text-sm text-navy-950 font-medium">{p.name}</span>
                <div className="flex items-baseline gap-1.5">
                  <span className="font-body text-sm font-bold text-teal-400">{fmtM(p.flSpend)}</span>
                  <span className="font-body text-[10px] text-navy-800/40">{p.soleSource}%</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* LPTA competitive insight (standard card) */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.6 }}
          className="rounded-2xl bg-white/70 backdrop-blur-sm p-5 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] flex flex-col justify-center"
        >
          <div className="flex items-start gap-4">
            <div className="w-9 h-9 rounded-lg bg-navy-950/[0.08] flex items-center justify-center shrink-0">
              <Shield className="w-5 h-5 text-navy-800/50" strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <h3 className="font-body text-base font-semibold text-navy-950 mb-1">
                LPTA Evaluation
              </h3>
              <p className="font-body text-sm leading-relaxed text-navy-800/65">
                Most food contracts use Lowest Price Technically Acceptable — directly favors wholesale distributors with volume purchasing.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Avoid note + source + compass star */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <div>
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-[11px] text-navy-800/40 flex items-center gap-1.5"
          >
            <AlertTriangle className="w-3 h-3" strokeWidth={1.5} />
            <span className="font-medium">Avoid:</span>
            {' '}{PRODUCT_TIERS.avoid.map(p => p.name).join(' \u00B7 ')}
          </motion.span>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="text-[10px] text-navy-800/35 mt-1"
          >
            FPDS FY2024 by PSC code | USASpending FL awards | FAR 15.101-2 (LPTA evaluation)
          </motion.p>
        </div>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
