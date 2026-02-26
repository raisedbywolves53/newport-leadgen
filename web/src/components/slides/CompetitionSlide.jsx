import { motion } from 'motion/react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { COMPETITORS } from '../../data/market'

function fmtM(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

const tierStyles = {
  top: { bg: 'bg-white/70', text: 'text-navy-800' },
  mid: { bg: 'bg-white/70', text: 'text-navy-800' },
  target: { bg: 'bg-teal-500/8', text: 'text-teal-300' },
}

export default function CompetitionSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 max-w-7xl mx-auto relative overflow-hidden">
      {/* Dramatic hero stat — Newport's entry position */}
      <div className="flex items-end gap-6 mb-2">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <span className="font-body text-xs font-semibold uppercase tracking-widest text-teal-500 block mb-2">
            Competition Landscape
          </span>
          <span className="font-body text-5xl md:text-6xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
            #5–10
          </span>
          <span className="font-body text-sm font-medium text-navy-800/40 uppercase tracking-wide ml-3">
            Entry Tier
          </span>
        </motion.div>

        <div className="pb-1.5">
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
            className="font-body text-3xl font-bold tracking-tight text-navy-950 mb-1"
          >
            Where Newport Fits
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.25 }}
            className="font-body text-base text-navy-800/60"
          >
            Top FL food distributors — Newport enters with superior infrastructure.
          </motion.p>
        </div>
      </div>

      <GoldLine width={60} className="mb-5" delay={0.3} />

      {/* Table */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.4 }}
        className="rounded-xl border border-black/[0.06] overflow-hidden"
      >
        <div className="grid grid-cols-[60px_1fr_120px_1fr] bg-white/70 px-4 py-2.5">
          <span className="text-navy-800/60 text-xs font-semibold">Rank</span>
          <span className="text-navy-800/60 text-xs font-semibold">Company</span>
          <span className="text-navy-800/60 text-xs font-semibold text-right">FL Gov Awards</span>
          <span className="text-navy-800/60 text-xs font-semibold pl-4">Notes</span>
        </div>

        {COMPETITORS.map((c, i) => {
          const style = tierStyles[c.tier]
          return (
            <motion.div
              key={c.rank}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + i * 0.06, duration: 0.3 }}
              className={`grid grid-cols-[60px_1fr_120px_1fr] px-4 py-2 border-t border-black/[0.06] ${style.bg}`}
            >
              <span className={`text-sm font-semibold ${c.tier === 'target' ? 'text-teal-400' : 'text-navy-800/50'}`}>
                #{c.rank}
              </span>
              <span className={`text-sm ${c.tier === 'target' ? 'font-semibold text-teal-300' : style.text}`}>
                {c.company}
              </span>
              <span className={`text-sm text-right font-mono ${c.tier === 'target' ? 'text-teal-400' : 'text-navy-800/60'}`}>
                {fmtM(c.amount)}
              </span>
              <span className="text-xs text-navy-800/50 pl-4 self-center">
                {c.notes}
              </span>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Newport callout — with gold accent strip */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.4 }}
        className="mt-4 rounded-xl border border-teal-500/30 bg-teal-500/8 p-4 relative overflow-hidden"
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
        <div className="pl-3">
          <h4 className="text-teal-400 font-body text-base font-bold mb-1">
            Newport's Entry Point: $1-5M Tier
          </h4>
          <p className="text-navy-800/70 text-sm">
            Competitors #5-10 are small FL companies with less infrastructure. Oakes ($26M) and US Foods ($24M)
            prove the model works at scale. Newport enters with superior distribution infrastructure and wholesale pricing.
          </p>
        </div>
      </motion.div>

      {/* Source + compass star */}
      <div className="flex items-center justify-between mt-3">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-[10px] text-navy-800/35"
        >
          USASpending API, FY2024 FL food contracts under $350K
        </motion.p>
        <CompassStar size={14} opacity={0.18} delay={1.3} />
      </div>
    </div>
  )
}
