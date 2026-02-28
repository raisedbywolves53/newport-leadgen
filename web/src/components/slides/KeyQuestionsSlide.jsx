import { useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import { ChevronDown } from 'lucide-react'
import { GoldLine } from '../ui/DecorativeElements'
import { KEY_QUESTIONS } from '../../data/strategy'

const priorityColors = {
  HIGHEST: { bg: '#C9A84C', text: '#ffffff' },
  HIGH: { bg: '#1B7A8A', text: '#ffffff' },
  MEDIUM: { bg: '#e4e4e7', text: '#52525b' },
}

const sectionConfig = {
  'Will This Work?': { accent: '#1B7A8A', icon: '01' },
  'What Are the Risks?': { accent: '#C9A84C', icon: '02' },
  'How Much Bigger?': { accent: '#27272a', icon: '03' },
}

const priorityOrder = { HIGHEST: 0, HIGH: 1, MEDIUM: 2 }

export default function KeyQuestionsSlide() {
  const [openItems, setOpenItems] = useState(new Set())

  const categories = [...new Set(KEY_QUESTIONS.map(q => q.category))]

  function toggleItem(key) {
    setOpenItems(prev => {
      const next = new Set(prev)
      if (next.has(key)) next.delete(key)
      else next.add(key)
      return next
    })
  }

  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-3 pb-14 relative overflow-hidden">
      {/* Background number */}
      <div className="absolute -right-8 top-1/2 -translate-y-1/2 pointer-events-none">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.03 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="font-body text-[18rem] font-semibold leading-none"
          style={{ color: '#C9A84C' }}
        >
          10
        </motion.span>
      </div>

      {/* Header */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5 block"
        >
          Owner Decisions
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          Key Questions for Newport
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600"
        >
          We don't pretend to know your business. These answers shape the entire strategy.
        </motion.p>
        <GoldLine width={60} className="mt-1" delay={0.25} />
      </div>

      {/* Accordion sections */}
      <div className="flex-1 min-h-0 overflow-y-auto space-y-3 relative z-10 pr-1">
        {categories.map((cat, ci) => {
          const config = sectionConfig[cat]
          const questions = KEY_QUESTIONS
            .filter(q => q.category === cat)
            .sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority])

          return (
            <motion.div
              key={cat}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + ci * 0.1, duration: 0.35 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm overflow-hidden"
            >
              {/* Section header */}
              <div
                className="px-5 py-3 flex items-center gap-3"
                style={{
                  borderBottom: '2px solid',
                  borderColor: `${config.accent}25`,
                  backgroundColor: `${config.accent}06`,
                }}
              >
                <span
                  className="text-[11px] font-bold px-2 py-0.5 rounded"
                  style={{ backgroundColor: config.accent, color: '#fff' }}
                >
                  {config.icon}
                </span>
                <h4
                  className="text-sm font-bold uppercase tracking-wider"
                  style={{ color: config.accent }}
                >
                  {cat}
                </h4>
                <span className="text-xs text-zinc-400 ml-auto">
                  {questions.length} questions
                </span>
              </div>

              {/* Questions — accordion items */}
              <div>
                {questions.map((q, qi) => {
                  const key = `${ci}-${qi}`
                  const isOpen = openItems.has(key)
                  const pc = priorityColors[q.priority]
                  return (
                    <div
                      key={qi}
                      className="border-b border-zinc-100 last:border-b-0"
                    >
                      <button
                        onClick={() => toggleItem(key)}
                        className="w-full px-5 py-3 flex items-center gap-3 text-left hover:bg-zinc-50/50 transition-colors cursor-pointer"
                      >
                        <span
                          className="shrink-0 text-[9px] font-bold px-1.5 py-0.5 rounded"
                          style={{ backgroundColor: pc.bg, color: pc.text }}
                        >
                          {q.priority}
                        </span>
                        <span className="font-body text-sm font-medium text-zinc-900 flex-1 leading-snug">
                          {q.question}
                        </span>
                        <ChevronDown
                          className="w-4 h-4 text-zinc-400 shrink-0 transition-transform duration-200"
                          style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}
                        />
                      </button>
                      <AnimatePresence initial={false}>
                        {isOpen && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.2, ease: 'easeInOut' }}
                            className="overflow-hidden"
                          >
                            <div className="px-5 pb-3 pl-[52px]">
                              <p className="font-body text-sm text-zinc-600 leading-relaxed">
                                {q.whyItMatters}
                              </p>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
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
