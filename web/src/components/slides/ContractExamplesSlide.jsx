import { motion } from 'motion/react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { CONTRACT_EXAMPLES, CONTRACT_EXAMPLES_SOURCE } from '../../data/strategy'

const typeColors = {
  'Micro-purchase': 'text-teal-400 bg-teal-500/10',
  'Micro / Simplified': 'text-teal-300 bg-teal-400/10',
  'Simplified / SLED': 'text-amber-400 bg-amber-500/10',
  'B2B sub-supply': 'text-amber-300 bg-amber-400/10',
  'Disaster micro-purchase': 'text-slate-300 bg-slate-500/10',
  'B2B (private)': 'text-amber-400 bg-amber-500/10',
}

const fitColors = {
  HIGHEST: 'text-amber-400',
  HIGH: 'text-teal-400',
  MODERATE: 'text-slate-400',
}

export default function ContractExamplesSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>Real Contract Opportunities</SlideTitle>
      <SlideSubtitle>
        Representative examples of what hits Florida procurement channels — these are the kinds of deals Newport would bid on.
      </SlideSubtitle>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="rounded-xl border border-navy-700 overflow-hidden"
      >
        {/* Header */}
        <div className="grid grid-cols-[160px_1fr_110px_130px_130px_60px] bg-navy-800 px-3 py-2 gap-2">
          {['Agency', 'Description', 'Est. Value', 'Type', 'Competition', 'Fit'].map(h => (
            <span key={h} className="text-slate-400 text-[10px] font-semibold uppercase tracking-wider">{h}</span>
          ))}
        </div>

        {CONTRACT_EXAMPLES.map((c, i) => {
          const tc = typeColors[c.type] || 'text-slate-400 bg-slate-500/10'
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + i * 0.05, duration: 0.25 }}
              className={`grid grid-cols-[160px_1fr_110px_130px_130px_60px] px-3 py-2 gap-2 border-t border-navy-700/50 ${
                i % 2 === 0 ? 'bg-navy-900/30' : ''
              }`}
            >
              <span className="text-offwhite text-xs font-medium">{c.agency}</span>
              <span className="text-slate-400 text-xs">{c.description}</span>
              <span className="text-teal-400 text-xs font-mono font-semibold">{c.estValue}</span>
              <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded self-center w-fit ${tc}`}>
                {c.type}
              </span>
              <span className="text-slate-500 text-[11px]">{c.competition}</span>
              <span className={`text-xs font-semibold ${fitColors[c.fit]}`}>{c.fit}</span>
            </motion.div>
          )
        })}
      </motion.div>

      <SourceCitation>{CONTRACT_EXAMPLES_SOURCE}</SourceCitation>
    </SlideLayout>
  )
}
