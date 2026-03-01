import { motion } from 'motion/react'
import { Zap, MapPin } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine } from '../ui/DecorativeElements'
import { B2B_TARGETS, B2B_SOURCE } from '../../data/market'

export default function B2bFastTrackSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto relative overflow-hidden">
      {/* Hero stat */}
      <div className="flex items-end gap-6 mb-2">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <span className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-2 block">
            Revenue Accelerator
          </span>
          <span className="font-body text-5xl md:text-6xl font-semibold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
            2–8
          </span>
          <span className="font-body text-lg font-medium text-zinc-400 uppercase tracking-wide ml-2">
            Weeks
          </span>
        </motion.div>

        <div className="pb-1.5">
          <motion.h2
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
            className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-1"
          >
            The B2B Fast Track
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.25 }}
            className="font-body text-base text-zinc-600"
          >
            Private institutional buyers — no government procurement required. Revenue in weeks, not months.
          </motion.p>
        </div>
      </div>

      <GoldLine width={60} className="mb-4" delay={0.3} />

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.4 }}
        className="rounded-xl border border-zinc-200 shadow-sm overflow-hidden"
      >
        {/* Header */}
        <div className="grid grid-cols-[180px_100px_100px_1fr_160px] bg-zinc-50 px-4 py-3 gap-2">
          <span className="text-zinc-500 text-[13px] font-semibold">Organization</span>
          <span className="text-zinc-500 text-[13px] font-semibold">FL Beds/Scale</span>
          <span className="text-zinc-500 text-[13px] font-semibold">Est. Food $</span>
          <span className="text-zinc-500 text-[13px] font-semibold">Detail</span>
          <span className="text-zinc-500 text-[13px] font-semibold">Entry Path</span>
        </div>

        {B2B_TARGETS.map((t, i) => (
          <motion.div
            key={t.name}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 + i * 0.08, duration: 0.3 }}
            className={`grid grid-cols-[180px_100px_100px_1fr_160px] px-4 py-3 gap-2 border-t border-zinc-100 ${
              i === 0 ? 'bg-amber-50/50' : 'bg-white'
            }`}
          >
            <div>
              <span className={`text-sm font-semibold ${i === 0 ? 'text-amber-600' : 'text-zinc-950'}`}>
                {t.name}
              </span>
              {i === 0 && (
                <span className="flex items-center gap-1 text-[10px] text-amber-500 mt-0.5">
                  <MapPin className="w-3 h-3" /> 15 mi from Newport
                </span>
              )}
            </div>
            <span className="text-sm text-zinc-600">{t.flBeds}</span>
            <span className="text-sm font-semibold" style={{ color: '#1B7A8A' }}>{t.estFoodSpend}</span>
            <span className="text-xs text-zinc-600 leading-relaxed">{t.detail}</span>
            <span className="text-xs text-zinc-500">{t.path}</span>
          </motion.div>
        ))}
      </motion.div>

      {/* Key insight */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.4 }}
        className="mt-3 flex items-start gap-3 rounded-xl border border-amber-200/50 bg-amber-50/30 p-3 relative overflow-hidden"
      >
        <div className="absolute left-0 top-2 bottom-2 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
        <div className="pl-2 flex items-start gap-3">
          <div className="w-6 h-6 rounded-lg bg-amber-100/60 flex items-center justify-center shrink-0 mt-0.5">
            <Zap className="w-3.5 h-3.5" style={{ color: '#C9A84C' }} strokeWidth={1.5} />
          </div>
          <div>
            <span className="text-sm font-semibold" style={{ color: '#C9A84C' }}>Why this matters: </span>
            <span className="text-zinc-600 text-sm">
              B2B sales to private operators have a 2-8 week sales cycle (vs 3-12 months for gov bids),
              require no past performance, and build institutional food supply credentials that strengthen future government proposals.
              These targets feed the subcontracting tier in the financial model — Aramark, GEO, and FSMC primes are active buyers.
            </span>
          </div>
        </div>
      </motion.div>

      <SourceCitation>
        {B2B_SOURCE}
      </SourceCitation>
    </div>
  )
}
