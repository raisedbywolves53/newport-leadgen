import { motion } from 'motion/react'
import { MessageCircleQuestion } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import { KEY_QUESTIONS } from '../../data/strategy'

const priorityColors = {
  HIGHEST: 'text-amber-400 bg-amber-500/15 border-amber-500/30',
  HIGH: 'text-teal-400 bg-teal-500/15 border-teal-500/30',
  MEDIUM: 'text-navy-800/60 bg-slate-500/15 border-slate-500/30',
}

const categoryColors = {
  'Will This Work?': 'text-teal-400',
  'What Are the Risks?': 'text-amber-400',
  'How Much Bigger?': 'text-navy-800',
}

export default function KeyQuestionsSlide() {
  // Group questions by category
  const categories = [...new Set(KEY_QUESTIONS.map(q => q.category))]

  return (
    <SlideLayout className="!py-7">
      <SlideTitle>Key Questions for Newport</SlideTitle>
      <SlideSubtitle>
        We don't pretend to know your business. These are the questions whose answers shape the entire strategy.
      </SlideSubtitle>

      <div className="space-y-4 mt-1">
        {categories.map((cat, ci) => {
          const questions = KEY_QUESTIONS.filter(q => q.category === cat)
          return (
            <motion.div
              key={cat}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + ci * 0.15, duration: 0.35 }}
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
                      transition={{ delay: 0.3 + ci * 0.15 + qi * 0.06, duration: 0.2 }}
                      className="rounded-lg border border-black/[0.06] bg-white/70 p-2.5 flex items-start gap-3"
                    >
                      <span className={`shrink-0 text-[9px] font-bold px-1.5 py-0.5 rounded border ${pc} mt-0.5`}>
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
    </SlideLayout>
  )
}
