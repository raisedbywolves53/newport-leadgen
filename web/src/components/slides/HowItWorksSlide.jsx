import { motion } from 'motion/react'
import { Search, BarChart3, Send, Award, ArrowRight } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine } from '../ui/DecorativeElements'
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
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto">
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-amber-500 mb-2"
      >
        Pipeline Engine
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
      >
        How It Works
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-navy-800/60 mb-1"
      >
        Sourcing, scoring, and winning — a systematic pipeline from opportunity to contract.
      </motion.p>
      <GoldLine width={60} className="mb-6" delay={0.25} />

      {/* Pipeline stages */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
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
                transition={{ delay: 0.35 + i * 0.1 }}
                className={`rounded-xl border px-4 py-2.5 text-center ${colorClass}`}
              >
                <Icon className="w-4 h-4 mx-auto mb-1" strokeWidth={1.5} />
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
            transition={{ delay: 0.5 + i * 0.1, duration: 0.4 }}
            className="rounded-xl border border-black/[0.06] bg-white/70 backdrop-blur-sm shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-3.5"
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
    </div>
  )
}
