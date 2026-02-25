import { motion } from 'motion/react'
import { Zap, MapPin } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { B2B_TARGETS, B2B_SOURCE } from '../../data/market'

export default function B2bFastTrackSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>The B2B Fast Track</SlideTitle>
      <SlideSubtitle>
        Private institutional buyers — no government procurement required. Revenue in weeks, not months.
      </SlideSubtitle>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="rounded-xl border border-navy-700 overflow-hidden"
      >
        {/* Header */}
        <div className="grid grid-cols-[180px_100px_100px_1fr_160px] bg-navy-800 px-4 py-2.5 gap-2">
          <span className="text-slate-400 text-xs font-semibold">Organization</span>
          <span className="text-slate-400 text-xs font-semibold">FL Beds/Scale</span>
          <span className="text-slate-400 text-xs font-semibold">Est. Food $</span>
          <span className="text-slate-400 text-xs font-semibold">Detail</span>
          <span className="text-slate-400 text-xs font-semibold">Entry Path</span>
        </div>

        {B2B_TARGETS.map((t, i) => (
          <motion.div
            key={t.name}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + i * 0.08, duration: 0.3 }}
            className={`grid grid-cols-[180px_100px_100px_1fr_160px] px-4 py-2.5 gap-2 border-t border-navy-700/50 ${
              i === 0 ? 'bg-amber-500/8' : 'bg-navy-800/20'
            }`}
          >
            <div>
              <span className={`text-sm font-semibold ${i === 0 ? 'text-amber-300' : 'text-offwhite'}`}>
                {t.name}
              </span>
              {i === 0 && (
                <span className="flex items-center gap-1 text-[10px] text-amber-400 mt-0.5">
                  <MapPin className="w-3 h-3" /> 15 mi from Newport
                </span>
              )}
            </div>
            <span className="text-sm text-slate-400">{t.flBeds}</span>
            <span className="text-sm text-teal-400 font-semibold">{t.estFoodSpend}</span>
            <span className="text-xs text-slate-400 leading-relaxed">{t.detail}</span>
            <span className="text-xs text-slate-500">{t.path}</span>
          </motion.div>
        ))}
      </motion.div>

      {/* Key insight */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.4 }}
        className="mt-3 flex items-start gap-3 rounded-lg border border-amber-500/20 bg-amber-500/5 p-3"
      >
        <Zap className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
        <div>
          <span className="text-amber-400 text-sm font-semibold">Why this matters: </span>
          <span className="text-slate-300 text-sm">
            B2B sales to private operators have a 2-8 week sales cycle (vs 3-12 months for gov bids),
            require no past performance, and build institutional food supply credentials that strengthen future government proposals.
          </span>
        </div>
      </motion.div>

      <SourceCitation>
        {B2B_SOURCE}
      </SourceCitation>
    </SlideLayout>
  )
}
