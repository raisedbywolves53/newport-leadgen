import { motion } from 'motion/react'
import { Eye, EyeOff, ArrowRight } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { ROUTE_COMPARISON, ROUTE_SOURCE } from '../../data/strategy'

export default function RecommendationSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>Two Routes — Our Recommendation</SlideTitle>
      <SlideSubtitle>
        You can enter this market for free. But full visibility into 90%+ of opportunities changes the math.
      </SlideSubtitle>

      {/* Comparison table */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="rounded-xl border border-navy-700 overflow-hidden"
      >
        {/* Header */}
        <div className="grid grid-cols-[180px_1fr_1fr] bg-navy-800 px-4 py-2.5 gap-3">
          <span className="text-slate-400 text-xs font-semibold" />
          <div className="flex items-center gap-2">
            <EyeOff className="w-3.5 h-3.5 text-slate-500" />
            <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Free Route</span>
          </div>
          <div className="flex items-center gap-2">
            <Eye className="w-3.5 h-3.5 text-teal-400" />
            <span className="text-teal-400 text-xs font-semibold uppercase tracking-wider">Full Visibility</span>
          </div>
        </div>

        {ROUTE_COMPARISON.map((row, i) => (
          <motion.div
            key={row.feature}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + i * 0.06, duration: 0.25 }}
            className={`grid grid-cols-[180px_1fr_1fr] px-4 py-2 gap-3 border-t border-navy-700/50 ${
              i % 2 === 0 ? 'bg-navy-900/30' : ''
            }`}
          >
            <span className="text-offwhite text-xs font-semibold">{row.feature}</span>
            <span className="text-slate-500 text-xs">{row.free}</span>
            <span className="text-slate-300 text-xs">{row.paid}</span>
          </motion.div>
        ))}
      </motion.div>

      {/* Bottom recommendation */}
      <div className="grid grid-cols-2 gap-4 mt-4">
        {/* Free */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.3 }}
          className="rounded-lg border border-navy-700 bg-navy-800/30 p-3.5"
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-slate-400 text-sm font-semibold">Free Route</span>
            <span className="text-slate-600 text-xs">$0/yr tools</span>
          </div>
          <p className="text-slate-500 text-xs leading-relaxed">
            SAM.gov + MFMP monitoring. Sees ~40-50% of FL opportunities.
            Viable start — but you're blind to the micro-purchase market where 83% of awards happen.
          </p>
        </motion.div>

        {/* Recommended */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.3 }}
          className="rounded-lg border border-teal-500/30 bg-teal-500/5 p-3.5 relative"
        >
          <span className="absolute -top-2.5 right-3 text-[10px] bg-teal-500 text-navy-950 px-2 py-0.5 rounded-full font-semibold uppercase tracking-wider">
            Recommended
          </span>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-teal-300 text-sm font-semibold">Full Visibility</span>
            <span className="text-teal-500/70 text-xs">~$13K/yr tools</span>
          </div>
          <p className="text-slate-400 text-xs leading-relaxed">
            GovSpend + CLEATUS + HigherGov. Sees 90%+ of FL opportunities across all channels.
            Micro-purchases, set-asides, state/local, and AI-assisted bid scoring.
          </p>
        </motion.div>
      </div>

      <SourceCitation>{ROUTE_SOURCE}</SourceCitation>
    </SlideLayout>
  )
}
