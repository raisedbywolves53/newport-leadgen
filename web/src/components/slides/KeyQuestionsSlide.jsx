import { motion } from 'motion/react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { KEY_QUESTIONS } from '../../data/strategy'

const priorityColors = {
  HIGHEST: 'text-white bg-amber-500 border-amber-500',
  HIGH: 'text-white bg-teal-500 border-teal-500',
  MEDIUM: 'text-navy-800/60 bg-slate-500/15 border-slate-500/30',
}

const categoryColors = {
  'Will This Work?': 'text-teal-400',
  'What Are the Risks?': 'text-amber-400',
  'How Much Bigger?': 'text-navy-800',
}

export default function KeyQuestionsSlide() {
  const categories = [...new Set(KEY_QUESTIONS.map(q => q.category))]

  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-7 max-w-7xl mx-auto relative overflow-hidden">
      {/* Oversized "10" as visual anchor */}
      <div className="absolute -right-8 top-1/2 -translate-y-1/2 pointer-events-none">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.03 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="font-body text-[20rem] font-bold leading-none"
          style={{ color: '#C9A84C' }}
        >
          10
        </motion.span>
      </div>

      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-amber-500 mb-2"
      >
        Owner Decisions
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
      >
        Key Questions for Newport
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-navy-800/60 mb-1"
      >
        We don't pretend to know your business. These are the questions whose answers shape the entire strategy.
      </motion.p>
      <GoldLine width={60} className="mb-5" delay={0.25} />

      <div className="space-y-4 mt-1 relative z-10">
        {categories.map((cat, ci) => {
          const questions = KEY_QUESTIONS.filter(q => q.category === cat)
          return (
            <motion.div
              key={cat}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + ci * 0.15, duration: 0.35 }}
            >
              <h4 className={`text-xs font-semibold uppercase tracking-wider mb-1.5 ${categoryColors[cat]}`}>
                {cat}
              </h4>
              <div className="space-y-1.5">
                {questions.map((q, qi) => {
                  const pc = priorityColors[q.priority]
                  return (
                    <motion.div
                      key={qi}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.35 + ci * 0.15 + qi * 0.06, duration: 0.2 }}
                      className="rounded-xl border border-black/[0.06] bg-white/70 backdrop-blur-sm shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-2.5 flex items-start gap-3"
                    >
                      <span className={`shrink-0 text-[9px] font-bold px-1.5 py-0.5 rounded-md border ${pc} mt-0.5`}>
                        {q.priority}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="text-navy-950 text-xs font-medium leading-relaxed">{q.question}</p>
                        <p className="text-navy-800/50 text-[10px] leading-relaxed mt-0.5">{q.whyItMatters}</p>
                      </div>
                    </motion.div>
                  )
                })}
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
