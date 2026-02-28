import { motion } from 'motion/react'
import { Users, UserCheck, Utensils, ArrowDown } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'

const layers = [
  {
    icon: Users,
    title: 'Contracting Officers',
    subtitle: 'Formal procurement contacts',
    description: 'Manage the RFP process, evaluate bids, award contracts. Typically responsive only through official channels. Relationship value: medium (process-driven).',
    color: 'slate',
  },
  {
    icon: UserCheck,
    title: 'Program Managers',
    subtitle: 'Own the budget',
    description: 'Influence requirements, select vendors for simplified acquisitions, approve micro-purchases. More accessible than contracting officers. Relationship value: high.',
    color: 'teal',
  },
  {
    icon: Utensils,
    title: 'Front-Line Influencers',
    subtitle: 'Write the requirements',
    description: 'The kitchen head at a BOP facility writes the food specs. The food service manager at MacDill decides what goes on the purchase order. These people do vendor due diligence — meeting them face-to-face, providing samples, understanding their needs is marketing, not lobbying.',
    color: 'amber',
  },
]

const colorMap = {
  slate: { bg: 'bg-white', border: 'border-zinc-200', icon: 'text-zinc-400', iconBg: 'bg-zinc-100' },
  teal: { bg: 'bg-white', border: 'border-zinc-200', icon: 'text-teal-500', iconBg: 'bg-teal-500/10' },
  amber: { bg: 'bg-amber-50/30', border: 'border-amber-200/50', icon: 'text-amber-500', iconBg: 'bg-amber-100/60' },
}

const processSteps = [
  'Identify influencer (kitchen head, food service manager, commissary buyer)',
  'Research their facility needs and current vendors',
  'Face-to-face meeting — provide samples, discuss capabilities',
  'Build into vendor qualification pipeline',
  'Influencer references Newport in next requirement spec',
]

export default function BdStrategySlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto">
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-2"
      >
        Relationship Capital
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
      >
        Business Development Strategy
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-zinc-600 mb-1"
      >
        Government contracting is still a full-contact sport. Someone has to meet people, provide samples, and maintain relationships.
      </motion.p>
      <GoldLine width={60} className="mb-5" delay={0.25} />

      <div className="grid grid-cols-[1fr_1fr] gap-6 mt-2">
        {/* Left — Influence layers */}
        <div className="flex flex-col gap-2">
          {layers.map((layer, i) => {
            const c = colorMap[layer.color]
            return (
              <div key={layer.title}>
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + i * 0.12, duration: 0.4 }}
                  className={`rounded-xl border ${c.border} ${c.bg} shadow-sm p-3.5`}
                >
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <div className={`w-7 h-7 rounded-lg ${c.iconBg} flex items-center justify-center`}>
                      <layer.icon className={`w-4 h-4 ${c.icon}`} strokeWidth={1.5} />
                    </div>
                    <div>
                      <h4 className="text-zinc-950 font-semibold text-sm">{layer.title}</h4>
                      <span className="text-zinc-500 text-[11px]">{layer.subtitle}</span>
                    </div>
                  </div>
                  <p className="text-zinc-600 text-xs leading-relaxed">{layer.description}</p>
                </motion.div>
                {i < layers.length - 1 && (
                  <div className="flex justify-center py-0.5">
                    <ArrowDown className="w-3.5 h-3.5 text-zinc-300" />
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Right — Process flow */}
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
        >
          <h4 className="font-semibold text-sm mb-3 uppercase tracking-wider" style={{ color: '#C9A84C' }}>
            Front-Line Sourcing Process
          </h4>
          <div className="space-y-2.5">
            {processSteps.map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + i * 0.1, duration: 0.3 }}
                className="flex items-start gap-3"
              >
                <span className="w-5 h-5 rounded-full bg-amber-100/60 border border-amber-200 flex items-center justify-center shrink-0 mt-0.5">
                  <span className="text-[10px] font-semibold" style={{ color: '#C9A84C' }}>{i + 1}</span>
                </span>
                <span className="text-zinc-600 text-sm leading-relaxed">{step}</span>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            className="mt-4 rounded-xl border border-zinc-200 bg-white shadow-sm p-3 relative overflow-hidden"
          >
            <div className="absolute left-0 top-2 bottom-2 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
            <p className="text-zinc-600 text-xs leading-relaxed pl-3">
              <strong className="text-zinc-950">The creative insight:</strong> Most competitors only monitor portals. Sourcing front-line influencers
              — the people who actually write the requirements — is where real competitive advantage lives.
            </p>
          </motion.div>
        </motion.div>
      </div>

      <SourceCitation>
        FAR 13.106 (simplified acquisition procedures) | BOP procurement research | DoD commissary vendor programs
      </SourceCitation>
    </div>
  )
}
