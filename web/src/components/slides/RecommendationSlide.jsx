import { motion } from 'motion/react'
import { Eye, EyeOff, Check, X, TrendingUp } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { ROUTE_COMPARISON, ROUTE_SOURCE } from '../../data/strategy'

export default function RecommendationSlide() {
  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-5 pb-3 relative overflow-hidden">
      <BackgroundRing size={400} className="-bottom-32 -right-32" opacity={0.02} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-2 block"
        >
          Investment Decision
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-1"
        >
          Two Routes — Our Recommendation
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-base text-zinc-600"
        >
          You can enter this market for free. But full visibility into 90%+ of opportunities changes the math.
        </motion.p>
        <GoldLine width={60} className="mt-2" delay={0.25} />
      </div>

      {/* Unified card: two columns side by side */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl border border-zinc-200 shadow-sm overflow-hidden bg-white flex relative z-10"
      >
        {/* LEFT column — Free Route */}
        <div className="flex-1 flex flex-col border-r border-zinc-200">
          {/* Column header */}
          <div className="px-5 py-4 flex items-center justify-between" style={{ backgroundColor: '#f4f4f5', borderBottom: '2px solid #e4e4e7' }}>
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg bg-zinc-200/60 flex items-center justify-center">
                <EyeOff className="w-5 h-5 text-zinc-500" strokeWidth={1.5} />
              </div>
              <div>
                <h4 className="font-body text-base font-bold text-zinc-700">Free Route</h4>
                <span className="font-body text-[11px] text-zinc-600">SAM.gov + MFMP only</span>
              </div>
            </div>
            <span className="font-mono text-2xl font-bold text-zinc-500">$0<span className="text-sm font-normal text-zinc-400">/yr</span></span>
          </div>

          {/* Feature rows */}
          <div className="flex flex-col">
            {ROUTE_COMPARISON.map((row, i) => (
              <motion.div
                key={row.feature}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 + i * 0.06, duration: 0.25 }}
                className="px-5 py-3.5 border-b border-zinc-100 flex items-start gap-3"
                style={{ backgroundColor: i % 2 === 0 ? '#ffffff' : '#fafafa' }}
              >
                <div className="flex-1">
                  <span className="font-body text-base font-semibold text-zinc-800 block leading-tight">{row.feature}</span>
                  <span className="font-body text-sm text-zinc-700 leading-snug">{row.free}</span>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Footer summary */}
          <div className="px-5 py-4" style={{ backgroundColor: '#f4f4f5', borderTop: '2px solid #e4e4e7' }}>
            <div className="space-y-1.5">
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 text-zinc-500 shrink-0" strokeWidth={2} />
                <span className="font-body text-sm text-zinc-700">~40-50% of FL opportunities visible</span>
              </div>
              <div className="flex items-center gap-2">
                <X className="w-4 h-4 text-zinc-400 shrink-0" strokeWidth={2} />
                <span className="font-body text-sm text-zinc-600">Blind to micro-purchases (83% of awards)</span>
              </div>
            </div>
            <span className="font-body text-sm text-zinc-600 block mt-2.5 border-t border-zinc-200 pt-2">
              Viable starting point, but limited pipeline
            </span>
          </div>
        </div>

        {/* RIGHT column — Full Visibility (Recommended) */}
        <div className="flex-1 flex flex-col relative" style={{ backgroundColor: '#f8fffe' }}>
          {/* Teal left border accent */}
          <div className="absolute left-0 top-0 bottom-0 w-1" style={{ backgroundColor: '#1B7A8A' }} />

          {/* Column header */}
          <div className="px-5 py-4 flex items-center justify-between" style={{ backgroundColor: '#f0fdfa', borderBottom: '2px solid #99f6e4' }}>
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#1B7A8A18' }}>
                <Eye className="w-5 h-5" style={{ color: '#1B7A8A' }} strokeWidth={1.5} />
              </div>
              <div>
                <h4 className="font-body text-base font-bold" style={{ color: '#1B7A8A' }}>Full Visibility</h4>
                <span className="font-body text-[11px] text-zinc-500">GovSpend + CLEATUS + HigherGov</span>
              </div>
            </div>
            <div className="text-right">
              <span className="font-mono text-2xl font-bold block" style={{ color: '#1B7A8A' }}>$13.9K<span className="text-sm font-normal opacity-60">/yr</span></span>
              <span
                className="text-[10px] font-semibold px-2.5 py-0.5 rounded text-white uppercase tracking-wider inline-block mt-0.5"
                style={{ backgroundColor: '#C9A84C' }}
              >
                Recommended
              </span>
            </div>
          </div>

          {/* Feature rows — emphasized */}
          <div className="flex flex-col">
            {ROUTE_COMPARISON.map((row, i) => (
              <motion.div
                key={row.feature}
                initial={{ opacity: 0, x: 8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.06, duration: 0.25 }}
                className="px-5 py-3.5 border-b flex items-start gap-3"
                style={{
                  backgroundColor: i % 2 === 0 ? '#f8fffe' : '#f0fdfb',
                  borderColor: '#e6f7f3',
                }}
              >
                <div className="flex-1">
                  <span className="font-body text-base font-semibold text-zinc-900 block leading-tight">{row.feature}</span>
                  <span className="font-body text-sm font-medium leading-snug" style={{ color: '#1B7A8A' }}>{row.paid}</span>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Footer — ROI summary */}
          <div className="px-5 py-4" style={{ backgroundColor: '#f0fdfa', borderTop: '2px solid #99f6e4' }}>
            <div className="space-y-1.5">
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 shrink-0" style={{ color: '#1B7A8A' }} strokeWidth={2} />
                <span className="font-body text-sm font-medium" style={{ color: '#1B7A8A' }}>90%+ of FL opportunities visible</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 shrink-0" style={{ color: '#1B7A8A' }} strokeWidth={2} />
                <span className="font-body text-sm font-medium" style={{ color: '#1B7A8A' }}>Micro-purchases, set-asides, AI bid scoring</span>
              </div>
            </div>
            <div className="flex items-center gap-2 mt-2.5 border-t pt-2" style={{ borderColor: '#99f6e4' }}>
              <TrendingUp className="w-4 h-4" style={{ color: '#C9A84C' }} />
              <span className="font-body text-sm font-bold" style={{ color: '#1B7A8A' }}>
                2-3x more pipeline at $1.08/opportunity/day
              </span>
            </div>
          </div>
        </div>
      </motion.div>

      <SourceCitation>{ROUTE_SOURCE}</SourceCitation>
    </div>
  )
}
