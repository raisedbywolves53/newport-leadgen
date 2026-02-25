import { motion } from 'motion/react'
import { MapPin, ShieldCheck, RefreshCw, FileStack } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { useCountUp } from '../../hooks/useCountUp'
import { HEADLINE_STATS } from '../../data/market'

const icons = [MapPin, ShieldCheck, FileStack, RefreshCw]

const accentColors = ['#C9A84C', '#1B7A8A', '#1B7A8A', '#1B7A8A']

function StatCard({ stat, index }) {
  const Icon = icons[index]
  const accent = accentColors[index]
  const count = useCountUp(stat.value, 1200, 600 + index * 200)
  const isHero = index === 0

  const display = stat.prefix
    ? `${stat.prefix}${count.toLocaleString()}${stat.suffix || ''}`
    : `${count.toLocaleString()}${stat.suffix || ''}`

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 + index * 0.12 }}
      className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] p-5 h-full flex flex-col shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
    >
      <div className="flex items-center gap-3 mb-3">
        <Icon
          className="w-5 h-5"
          style={{ color: isHero ? accent : '#0F1A2E50' }}
          strokeWidth={1.5}
        />
        <span className="text-navy-950 font-semibold text-xs tracking-[-0.02em] leading-snug">
          {stat.label}
        </span>
      </div>

      <span
        className={`font-body font-bold tracking-tight leading-none mb-2 ${
          isHero ? 'text-4xl' : 'text-3xl text-navy-950'
        }`}
        style={isHero ? { color: accent } : undefined}
      >
        {display}
      </span>

      <span className="text-navy-800/50 font-medium text-[11px] leading-relaxed mt-auto">
        {stat.detail}
      </span>
    </motion.div>
  )
}

export default function ExecutiveSummarySlide() {
  return (
    <div className="w-full h-full relative overflow-hidden">
      {/* Tree illustration — slide background matches image gray */}
      <div className="absolute inset-0">
        <motion.img
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1.2, delay: 0.1 }}
          src="/animated_under_tree.png"
          alt=""
          className="absolute -left-[15%] top-1/2 -translate-y-1/2 h-[90%] object-contain"
        />
      </div>

      <div className="relative z-10 h-full grid grid-cols-[45%_55%]">
        {/* Left — breathing room for the tree */}
        <div />

        {/* Right — Content */}
        <div className="flex flex-col justify-center px-10 py-12">
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
            className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
          >
            The Opportunity
          </motion.h2>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.35 }}
            className="font-body text-sm text-navy-800/60 mb-8 max-w-md"
          >
            Newport's 30-year operating history is a competitive moat in today's post-fraud procurement environment.
          </motion.p>

          <div className="grid grid-cols-2 gap-4">
            {HEADLINE_STATS.map((stat, i) => (
              <StatCard key={stat.label} stat={stat} index={i} />
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.4 }}
            className="mt-6"
          >
            <p className="text-[10px] text-navy-800/40">
              Sources: USASpending API FY2024 (Feb 2026 query) | FPDS competition analysis | Fed-Spend recompete analysis
            </p>
          </motion.div>
        </div>
      </div>
    </div>
  )
}
