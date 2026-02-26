import { motion } from 'motion/react'
import { Eye, EyeOff } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { ROUTE_COMPARISON, ROUTE_SOURCE } from '../../data/strategy'

export default function RecommendationSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto relative overflow-hidden">
      <BackgroundRing size={400} className="-bottom-32 -right-32" opacity={0.02} />

      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-teal-500 mb-2"
      >
        Investment Decision
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
      >
        Two Routes — Our Recommendation
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-navy-800/60 mb-1"
      >
        You can enter this market for free. But full visibility into 90%+ of opportunities changes the math.
      </motion.p>
      <GoldLine width={60} className="mb-5" delay={0.25} />

      {/* Comparison table */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl border border-black/[0.06] overflow-hidden"
      >
        <div className="grid grid-cols-[180px_1fr_1fr] bg-white/70 px-4 py-2.5 gap-3">
          <span className="text-navy-800/60 text-xs font-semibold" />
          <div className="flex items-center gap-2">
            <EyeOff className="w-3.5 h-3.5 text-navy-800/50" />
            <span className="text-navy-800/60 text-xs font-semibold uppercase tracking-wider">Free Route</span>
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
            transition={{ delay: 0.35 + i * 0.06, duration: 0.25 }}
            className={`grid grid-cols-[180px_1fr_1fr] px-4 py-2 gap-3 border-t border-black/[0.06] ${
              i % 2 === 0 ? 'bg-white/50' : ''
            }`}
          >
            <span className="text-navy-950 text-xs font-semibold">{row.feature}</span>
            <span className="text-navy-800/50 text-xs">{row.free}</span>
            <span className="text-navy-800/70 text-xs">{row.paid}</span>
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
          className="rounded-xl border border-black/[0.06] bg-white/70 backdrop-blur-sm shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-3.5"
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-navy-800/60 text-sm font-semibold">Free Route</span>
            <span className="text-navy-800/40 text-xs">$0/yr tools</span>
          </div>
          <p className="text-navy-800/50 text-xs leading-relaxed">
            SAM.gov + MFMP monitoring. Sees ~40-50% of FL opportunities.
            Viable start — but you're blind to the micro-purchase market where 83% of awards happen.
          </p>
        </motion.div>

        {/* Recommended — dramatic treatment */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.3 }}
          className="rounded-xl border border-teal-500/30 bg-teal-500/5 p-3.5 relative overflow-hidden"
        >
          {/* Gold accent strip */}
          <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
          <span className="absolute -top-2.5 right-3 text-[10px] bg-teal-500 text-white px-2 py-0.5 rounded-full font-semibold uppercase tracking-wider">
            Recommended
          </span>
          <div className="pl-2">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-teal-300 text-sm font-semibold">Full Visibility</span>
              <span className="text-teal-500/70 text-xs">~$13K/yr tools</span>
            </div>
            <p className="text-navy-800/65 text-xs leading-relaxed">
              GovSpend + CLEATUS + HigherGov. Sees 90%+ of FL opportunities across all channels.
              Micro-purchases, set-asides, state/local, and AI-assisted bid scoring.
            </p>
          </div>
        </motion.div>
      </div>

      <SourceCitation>{ROUTE_SOURCE}</SourceCitation>
    </div>
  )
}
