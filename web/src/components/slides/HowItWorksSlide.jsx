import { motion } from 'motion/react'
import { Search, BarChart3, FileText, Send, Award, ChevronRight, Globe, Building2, Eye, Users, Check } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { SOURCING_CHANNELS } from '../../data/strategy'

const STAGES = [
  { name: 'Identify', sub: 'Daily monitoring', icon: Search, accent: '#1B7A8A' },
  { name: 'Score', sub: 'Bid/no-bid (0-100)', icon: BarChart3, accent: '#1B7A8A' },
  { name: 'Pursue', sub: 'Proposal in progress', icon: FileText, accent: '#C9A84C' },
  { name: 'Submit', sub: 'Bid delivered', icon: Send, accent: '#C9A84C' },
  { name: 'Win', sub: 'Contract awarded', icon: Award, accent: '#1B7A8A' },
]

const CHANNEL_ICONS = [Globe, Building2, Eye, Users]

const CHANNEL_BULLETS = [
  ['Food/grocery NAICS filter', 'Automated bid/no-bid scoring', 'Daily email digest to team'],
  ['School district contracts', 'State corrections facilities', 'FL agency purchase orders'],
  ['Reveals micro-purchase spend', '$8-15M/yr FL food transactions', 'Historical award intelligence'],
  ['SDB & HUBZone set-asides', 'BidNet & DemandStar portals', 'BOP reverse auction access'],
]

function channelAccent(cost) {
  if (cost.toLowerCase().includes('free')) return '#1B7A8A'
  return '#C9A84C'
}

export default function HowItWorksSlide() {
  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-3 pb-14 relative overflow-hidden">
      <BackgroundRing size={400} className="-top-28 -right-28" opacity={0.03} />

      {/* Header — compact */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-1"
        >
          Process
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          How It Works
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600 max-w-2xl"
        >
          From opportunity identification to contract award — a systematic pipeline.
        </motion.p>
        <GoldLine width={60} className="mt-1.5" delay={0.25} />
      </div>

      {/* Pipeline stages — horizontal strip */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm px-8 py-4 mb-3 relative z-10"
      >
        <div className="flex items-center justify-between">
          {STAGES.map((stage, i) => {
            const Icon = stage.icon
            return (
              <div key={stage.name} className="flex items-center">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.35 + i * 0.08, duration: 0.35 }}
                  className="flex items-center gap-3"
                >
                  <div
                    className="w-11 h-11 rounded-lg flex items-center justify-center shrink-0"
                    style={{ backgroundColor: `${stage.accent}12` }}
                  >
                    <Icon
                      className="w-5 h-5"
                      style={{ color: stage.accent }}
                      strokeWidth={1.5}
                    />
                  </div>
                  <div>
                    <span className="font-body text-sm font-semibold text-zinc-900 block leading-tight">
                      {stage.name}
                    </span>
                    <span className="font-body text-xs text-zinc-500 leading-tight">
                      {stage.sub}
                    </span>
                  </div>
                </motion.div>
                {i < STAGES.length - 1 && (
                  <ChevronRight className="w-4 h-4 text-zinc-300 mx-4 shrink-0" />
                )}
              </div>
            )
          })}
        </div>
      </motion.div>

      {/* Sourcing channel cards — flex-1 to stretch into remaining space */}
      <div className="grid grid-cols-4 gap-3 flex-1 min-h-0 relative z-10">
        {SOURCING_CHANNELS.map((ch, i) => {
          const accent = channelAccent(ch.cost)
          const Icon = CHANNEL_ICONS[i]
          const bullets = CHANNEL_BULLETS[i]
          return (
            <motion.div
              key={ch.title}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1, duration: 0.4 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm p-5 flex flex-col relative overflow-hidden"
            >
              {/* Top accent bar */}
              <div
                className="absolute top-0 left-4 right-4 h-[2px] rounded-full"
                style={{ backgroundColor: accent }}
              />

              {/* Icon + title row */}
              <div className="flex items-start gap-3 mt-1 mb-3">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ backgroundColor: `${accent}12` }}
                >
                  <Icon className="w-5 h-5" style={{ color: accent }} strokeWidth={1.5} />
                </div>
                <h4 className="font-body text-base font-semibold text-zinc-950 pt-1.5 leading-tight">
                  {ch.title}
                </h4>
              </div>

              {/* Description */}
              <p className="font-body text-sm leading-relaxed text-zinc-600 mb-3">
                {ch.description}
              </p>

              {/* Feature bullets */}
              <div className="space-y-2 mb-3">
                {bullets.map((b, j) => (
                  <div key={j} className="flex items-start gap-2">
                    <Check
                      className="w-4 h-4 shrink-0 mt-0.5"
                      style={{ color: accent }}
                      strokeWidth={2}
                    />
                    <span className="font-body text-sm text-zinc-600 leading-snug">{b}</span>
                  </div>
                ))}
              </div>

              {/* Cost badge at bottom */}
              <div className="mt-auto pt-3 border-t border-zinc-100">
                <span
                  className="font-body text-sm font-semibold inline-flex items-center px-3 py-1.5 rounded"
                  style={{
                    backgroundColor: `${accent}10`,
                    color: accent,
                  }}
                >
                  {ch.cost}
                </span>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Pipeline conversion metrics */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.4 }}
        className="grid grid-cols-5 gap-3 mt-2 relative z-10"
      >
        {[
          { label: 'Opportunities Tracked', value: '200+', sub: 'per quarter', accent: '#1B7A8A' },
          { label: 'Scored & Filtered', value: '40-60', sub: 'pass bid/no-bid', accent: '#1B7A8A' },
          { label: 'Proposals Submitted', value: '15-25', sub: 'per quarter', accent: '#C9A84C' },
          { label: 'Expected Win Rate', value: '35-50%', sub: 'micro-purchase tier', accent: '#C9A84C' },
          { label: 'Annual Wins Target', value: '20-30', sub: 'Year 1 goal', accent: '#1B7A8A' },
        ].map((metric, i) => (
          <div
            key={metric.label}
            className="rounded-xl bg-white border border-zinc-200 shadow-sm px-4 py-3.5 text-center"
          >
            <span className="font-body text-[10px] font-semibold uppercase tracking-wider text-zinc-500 block mb-1">
              {metric.label}
            </span>
            <span
              className="font-body text-2xl font-bold block leading-tight"
              style={{ color: metric.accent }}
            >
              {metric.value}
            </span>
            <span className="font-body text-[11px] text-zinc-500 block mt-0.5">
              {metric.sub}
            </span>
          </div>
        ))}
      </motion.div>

      {/* Source */}
      <div className="flex items-center justify-between mt-1 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-[10px] text-zinc-300"
        >
          SAM.gov API | MyFloridaMarketPlace | GovSpend ($6.5K/yr) | CLEATUS ($3K/yr) | HigherGov ($3.5K/yr)
        </motion.p>
      </div>
    </div>
  )
}
