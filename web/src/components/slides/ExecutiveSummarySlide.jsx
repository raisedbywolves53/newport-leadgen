import { motion } from 'motion/react'
import { MapPin, ShieldCheck, RefreshCw, FileStack } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { useCountUp } from '../../hooks/useCountUp'
import { HEADLINE_STATS } from '../../data/market'

const icons = [MapPin, ShieldCheck, FileStack, RefreshCw]
const colors = [
  { text: 'text-teal-400', bg: 'bg-teal-500/10', border: 'border-teal-500/20' },
  { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
  { text: 'text-teal-300', bg: 'bg-teal-400/10', border: 'border-teal-400/20' },
  { text: 'text-amber-300', bg: 'bg-amber-400/10', border: 'border-amber-400/20' },
]

function StatCard({ stat, index }) {
  const Icon = icons[index]
  const color = colors[index]
  const count = useCountUp(stat.value, 1200, 300 + index * 150)

  const display = stat.prefix
    ? `${stat.prefix}${count.toLocaleString()}${stat.suffix || ''}`
    : `${count.toLocaleString()}${stat.suffix || ''}`

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
      className={`rounded-xl border ${color.border} ${color.bg} p-6 flex flex-col`}
    >
      <div className={`inline-flex items-center justify-center w-10 h-10 rounded-lg ${color.bg} mb-4`}>
        <Icon className={`w-5 h-5 ${color.text}`} />
      </div>
      <span className={`font-display text-3xl font-semibold ${color.text} mb-1`}>
        {display}
      </span>
      <span className="text-offwhite font-medium text-sm mb-1">
        {stat.label}
      </span>
      <span className="text-slate-400 text-xs">
        {stat.detail}
      </span>
    </motion.div>
  )
}

export default function ExecutiveSummarySlide() {
  return (
    <SlideLayout>
      <SlideTitle>The Opportunity at a Glance</SlideTitle>
      <SlideSubtitle>
        Newport's 30-year operating history is a competitive moat in today's post-fraud procurement environment.
      </SlideSubtitle>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mt-4">
        {HEADLINE_STATS.map((stat, i) => (
          <StatCard key={stat.label} stat={stat} index={i} />
        ))}
      </div>

      <SourceCitation>
        Sources: USASpending API FY2024 (Feb 2026 query) | FPDS competition analysis | Fed-Spend recompete analysis
      </SourceCitation>
    </SlideLayout>
  )
}
