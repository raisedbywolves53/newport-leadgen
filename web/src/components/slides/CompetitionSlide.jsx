import { motion } from 'motion/react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { COMPETITORS } from '../../data/market'

function fmtM(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

const tierStyles = {
  top: { bg: 'bg-navy-800/30', text: 'text-slate-300' },
  mid: { bg: 'bg-navy-800/30', text: 'text-slate-300' },
  target: { bg: 'bg-teal-500/8', text: 'text-teal-300' },
}

export default function CompetitionSlide() {
  return (
    <SlideLayout>
      <SlideTitle>The Competition: Where Newport Fits</SlideTitle>
      <SlideSubtitle>
        Top FL food distributors — Newport enters at the #5-10 tier with superior infrastructure.
      </SlideSubtitle>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl border border-navy-700 overflow-hidden"
      >
        {/* Header */}
        <div className="grid grid-cols-[60px_1fr_120px_1fr] bg-navy-800 px-4 py-2.5">
          <span className="text-slate-400 text-xs font-semibold">Rank</span>
          <span className="text-slate-400 text-xs font-semibold">Company</span>
          <span className="text-slate-400 text-xs font-semibold text-right">FL Gov Awards</span>
          <span className="text-slate-400 text-xs font-semibold pl-4">Notes</span>
        </div>

        {/* Rows */}
        {COMPETITORS.map((c, i) => {
          const style = tierStyles[c.tier]
          return (
            <motion.div
              key={c.rank}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + i * 0.06, duration: 0.3 }}
              className={`grid grid-cols-[60px_1fr_120px_1fr] px-4 py-2 border-t border-navy-700/50 ${style.bg}`}
            >
              <span className={`text-sm font-semibold ${c.tier === 'target' ? 'text-teal-400' : 'text-slate-500'}`}>
                #{c.rank}
              </span>
              <span className={`text-sm ${c.tier === 'target' ? 'font-semibold text-teal-300' : style.text}`}>
                {c.company}
              </span>
              <span className={`text-sm text-right font-mono ${c.tier === 'target' ? 'text-teal-400' : 'text-slate-400'}`}>
                {fmtM(c.amount)}
              </span>
              <span className="text-xs text-slate-500 pl-4 self-center">
                {c.notes}
              </span>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Newport callout */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.4 }}
        className="mt-4 rounded-xl border border-teal-500/30 bg-teal-500/8 p-4"
      >
        <h4 className="text-teal-400 font-body text-base font-bold mb-1">
          Newport's Entry Point: $1-5M Tier
        </h4>
        <p className="text-slate-300 text-sm">
          Competitors #5-10 are small FL companies with less infrastructure. Oakes ($26M) and US Foods ($24M)
          prove the model works at scale. Newport enters with superior distribution infrastructure and wholesale pricing.
        </p>
      </motion.div>

      <SourceCitation>
        USASpending API, FY2024 FL food contracts under $350K
      </SourceCitation>
    </SlideLayout>
  )
}
