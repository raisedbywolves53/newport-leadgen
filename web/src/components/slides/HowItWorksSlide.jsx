import { motion } from 'motion/react'
import { Search, BarChart3, Send, Award, ArrowRight } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { PIPELINE_STAGES, SOURCING_CHANNELS } from '../../data/strategy'

const stageIcons = [Search, BarChart3, Send, Send, Award]
const stageColors = {
  slate: 'bg-slate-500/20 border-slate-500/30 text-slate-400',
  teal: 'bg-teal-500/15 border-teal-500/30 text-teal-400',
  amber: 'bg-amber-500/15 border-amber-500/30 text-amber-400',
  green: 'bg-green-500/15 border-green-500/30 text-green-400',
}

export default function HowItWorksSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>How It Works</SlideTitle>
      <SlideSubtitle>
        Sourcing, scoring, and winning — a systematic pipeline from opportunity to contract.
      </SlideSubtitle>

      {/* Pipeline stages */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="flex items-center justify-center gap-1 mb-6"
      >
        {PIPELINE_STAGES.map((stage, i) => {
          const Icon = stageIcons[i]
          const colorClass = stageColors[stage.color]
          return (
            <div key={stage.name} className="flex items-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + i * 0.1 }}
                className={`rounded-lg border px-4 py-2.5 text-center ${colorClass}`}
              >
                <Icon className="w-4 h-4 mx-auto mb-1" />
                <span className="text-xs font-semibold block">{stage.name}</span>
                <span className="text-[10px] text-navy-800/50 block">{stage.description}</span>
              </motion.div>
              {i < PIPELINE_STAGES.length - 1 && (
                <ArrowRight className="w-3.5 h-3.5 text-navy-800/40 mx-1" />
              )}
            </div>
          )
        })}
      </motion.div>

      {/* Sourcing channels */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {SOURCING_CHANNELS.map((ch, i) => (
          <motion.div
            key={ch.title}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 + i * 0.1, duration: 0.3 }}
            className="rounded-lg border border-black/[0.06] bg-white/70 p-3.5"
          >
            <h4 className="text-navy-950 font-semibold text-xs mb-1.5">{ch.title}</h4>
            <p className="text-navy-800/60 text-[11px] leading-relaxed mb-2">{ch.description}</p>
            <span className="text-teal-400 text-xs font-semibold">{ch.cost}</span>
          </motion.div>
        ))}
      </div>

      <SourceCitation>
        SAM.gov API | MyFloridaMarketPlace | GovSpend ($6.5K/yr) | CLEATUS ($3K/yr) | HigherGov ($3.5K/yr) — pricing per specs/09-INTEGRATIONS.md
      </SourceCitation>
    </SlideLayout>
  )
}
