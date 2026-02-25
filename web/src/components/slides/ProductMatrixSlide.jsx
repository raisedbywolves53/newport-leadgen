import { motion } from 'motion/react'
import { Star, TrendingUp, AlertTriangle } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { PRODUCT_TIERS } from '../../data/market'

function fmtM(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

export default function ProductMatrixSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>Product Opportunity Matrix</SlideTitle>
      <SlideSubtitle>
        Prioritized by FL demand, competition level, and Newport's pricing advantage.
      </SlideSubtitle>

      {/* Tier 1 */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="mb-4"
      >
        <div className="flex items-center gap-2 mb-2">
          <Star className="w-4 h-4 text-amber-400" />
          <span className="text-amber-400 font-semibold text-sm uppercase tracking-wider">Tier 1 — Highest Priority</span>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {PRODUCT_TIERS.tier1.map((p) => (
            <div key={p.psc} className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="text-offwhite font-semibold text-sm">{p.name}</h4>
                  <span className="text-slate-400 text-xs">PSC {p.psc}</span>
                </div>
                <span className="text-amber-400 font-body text-lg font-bold">{fmtM(p.flSpend)}</span>
              </div>
              <p className="text-slate-400 text-xs leading-relaxed mb-2">{p.advantage}</p>
              <div className="flex gap-3 text-xs">
                <span className="text-teal-400">{p.soleSource}% sole-source</span>
                <span className="text-slate-500">Gov markup: {p.govMarkup}</span>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Tier 2 */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.4 }}
        className="mb-4"
      >
        <div className="flex items-center gap-2 mb-2">
          <TrendingUp className="w-4 h-4 text-teal-400" />
          <span className="text-teal-400 font-semibold text-sm uppercase tracking-wider">Tier 2 — Growth Targets</span>
        </div>
        <div className="grid grid-cols-3 gap-3">
          {PRODUCT_TIERS.tier2.map((p) => (
            <div key={p.psc} className="rounded-lg border border-navy-700 bg-navy-800/50 p-3">
              <h4 className="text-offwhite font-semibold text-sm mb-1">{p.name}</h4>
              <span className="text-teal-400 font-body text-base font-bold">{fmtM(p.flSpend)}</span>
              <span className="text-slate-500 text-xs ml-1">FL</span>
              <p className="text-slate-400 text-xs mt-1">{p.soleSource}% sole-source</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Tier 3 — Avoid */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.4 }}
      >
        <div className="flex items-center gap-2 mb-1.5">
          <AlertTriangle className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-slate-500 font-semibold text-xs uppercase tracking-wider">Avoid / Long-Term Only</span>
        </div>
        <div className="flex gap-4">
          {PRODUCT_TIERS.avoid.map((p) => (
            <span key={p.psc} className="text-xs text-slate-500">
              <span className="text-slate-400">{p.name}</span> — {p.reason}
            </span>
          ))}
        </div>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="mt-4 text-xs text-teal-400/80 font-medium text-center"
      >
        Most food contracts use LPTA (Lowest Price Technically Acceptable) — this directly favors wholesale distributors with volume purchasing.
      </motion.p>

      <SourceCitation>
        FPDS FY2024 by PSC code | USASpending FL awards | FAR 15.101-2 (LPTA evaluation)
      </SourceCitation>
    </SlideLayout>
  )
}
