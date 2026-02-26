import { motion } from 'motion/react'
import { Search, BarChart3, FileText, Send, Award, ArrowRight, Globe, Building2, Eye, Users } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { SOURCING_CHANNELS } from '../../data/strategy'

// Pipeline stages with design-system-compliant colors
const STAGES = [
  { name: 'Identify', sub: 'Daily monitoring', icon: Search, accent: '#1B7A8A' },
  { name: 'Score', sub: 'Bid/no-bid (0-100)', icon: BarChart3, accent: '#1B7A8A' },
  { name: 'Pursue', sub: 'Proposal in progress', icon: FileText, accent: '#C9A84C' },
  { name: 'Submit', sub: 'Bid delivered', icon: Send, accent: '#C9A84C' },
  { name: 'Win', sub: 'Contract awarded', icon: Award, accent: '#1B7A8A' },
]

// Icons for sourcing channels
const CHANNEL_ICONS = [Globe, Building2, Eye, Users]

// Determine card accent: free channels get teal, paid get gold
function channelAccent(cost) {
  if (cost.toLowerCase().includes('free')) return '#1B7A8A'
  return '#C9A84C'
}

export default function HowItWorksSlide() {
  return (
    <div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
      <BackgroundRing size={400} className="-top-28 -right-28" opacity={0.03} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-navy-800/40 mb-3"
        >
          Process
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          How It Works
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-navy-800/60 max-w-2xl"
        >
          From opportunity identification to contract award — a systematic pipeline.
        </motion.p>
        <GoldLine width={60} className="mt-3" delay={0.25} />
      </div>

      {/* Pipeline row — circular badges with arrows */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="flex items-center justify-center gap-2 mb-6 relative z-10"
      >
        {STAGES.map((stage, i) => {
          const Icon = stage.icon
          return (
            <div key={stage.name} className="flex items-center gap-2">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.35 + i * 0.1, duration: 0.4 }}
                className="flex flex-col items-center"
              >
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center"
                  style={{ backgroundColor: `${stage.accent}15` }}
                >
                  <Icon
                    className="w-5 h-5"
                    style={{ color: stage.accent }}
                    strokeWidth={1.5}
                  />
                </div>
                <span className="font-body text-[11px] font-semibold text-navy-950 mt-2">
                  {stage.name}
                </span>
                <span className="font-body text-[10px] text-navy-800/40">
                  {stage.sub}
                </span>
              </motion.div>
              {i < STAGES.length - 1 && (
                <ArrowRight className="w-4 h-4 text-navy-800/15 -mt-5" />
              )}
            </div>
          )
        })}
      </motion.div>

      {/* Sourcing channel cards — grid-cols-4 */}
      <div className="grid grid-cols-4 gap-3 flex-1 min-h-0 relative z-10">
        {SOURCING_CHANNELS.map((ch, i) => {
          const accent = channelAccent(ch.cost)
          const Icon = CHANNEL_ICONS[i]
          return (
            <motion.div
              key={ch.title}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 + i * 0.1, duration: 0.45 }}
              className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-5 flex flex-col relative overflow-hidden"
            >
              {/* Top accent bar */}
              <div
                className="absolute top-0 left-4 right-4 h-[2px] rounded-full"
                style={{ backgroundColor: accent }}
              />

              {/* Icon pill */}
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center mb-3 mt-1"
                style={{ backgroundColor: `${accent}15` }}
              >
                <Icon className="w-5 h-5" style={{ color: accent }} strokeWidth={1.5} />
              </div>

              <h4 className="font-body text-sm font-semibold text-navy-950 mb-2">
                {ch.title}
              </h4>
              <p className="font-body text-[13px] leading-relaxed text-navy-800/65 flex-1">
                {ch.description}
              </p>
              <span
                className="font-body text-xs font-semibold mt-3 block"
                style={{ color: accent }}
              >
                {ch.cost}
              </span>
            </motion.div>
          )
        })}
      </div>

      {/* Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-[10px] text-navy-800/35"
        >
          SAM.gov API | MyFloridaMarketPlace | GovSpend ($6.5K/yr) | CLEATUS ($3K/yr) | HigherGov ($3.5K/yr)
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.4} />
      </div>
    </div>
  )
}
