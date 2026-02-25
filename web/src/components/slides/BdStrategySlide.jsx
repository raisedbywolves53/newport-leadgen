import { motion } from 'motion/react'
import { Users, UserCheck, Utensils, ArrowDown } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'

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
  slate: { bg: 'bg-white/70', border: 'border-black/[0.06]', icon: 'text-slate-400', iconBg: 'bg-slate-500/15' },
  teal: { bg: 'bg-teal-500/5', border: 'border-teal-500/20', icon: 'text-teal-400', iconBg: 'bg-teal-500/15' },
  amber: { bg: 'bg-amber-500/8', border: 'border-amber-500/20', icon: 'text-amber-400', iconBg: 'bg-amber-500/15' },
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
    <SlideLayout className="!py-8">
      <SlideTitle>Business Development & Relationship Strategy</SlideTitle>
      <SlideSubtitle>
        Government contracting is still a full-contact sport. Someone has to meet people, provide samples, and maintain relationships.
      </SlideSubtitle>

      <div className="grid grid-cols-[1fr_1fr] gap-6 mt-2">
        {/* Left — Influence layers */}
        <div className="flex flex-col gap-2">
          {layers.map((layer, i) => {
            const c = colorMap[layer.color]
            return (
              <div key={layer.title}>
                <motion.div
                  initial={{ opacity: 0, x: -15 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + i * 0.15, duration: 0.4 }}
                  className={`rounded-lg border ${c.border} ${c.bg} p-3.5`}
                >
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <div className={`w-7 h-7 rounded-md ${c.iconBg} flex items-center justify-center`}>
                      <layer.icon className={`w-4 h-4 ${c.icon}`} />
                    </div>
                    <div>
                      <h4 className="text-navy-950 font-semibold text-sm">{layer.title}</h4>
                      <span className="text-navy-800/50 text-[10px]">{layer.subtitle}</span>
                    </div>
                  </div>
                  <p className="text-navy-800/60 text-xs leading-relaxed">{layer.description}</p>
                </motion.div>
                {i < layers.length - 1 && (
                  <div className="flex justify-center py-0.5">
                    <ArrowDown className="w-3.5 h-3.5 text-navy-800/40" />
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Right — Process flow */}
        <motion.div
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
        >
          <h4 className="text-amber-400 font-semibold text-sm mb-3 uppercase tracking-wider">
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
                <span className="w-5 h-5 rounded-full bg-amber-500/15 border border-amber-500/30 flex items-center justify-center shrink-0 mt-0.5">
                  <span className="text-amber-400 text-[10px] font-semibold">{i + 1}</span>
                </span>
                <span className="text-navy-800 text-sm leading-relaxed">{step}</span>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            className="mt-4 rounded-lg border border-teal-500/20 bg-teal-500/5 p-3"
          >
            <p className="text-teal-300 text-xs leading-relaxed">
              <strong>The creative insight:</strong> Most competitors only monitor portals. Sourcing front-line influencers
              — the people who actually write the requirements — is where real competitive advantage lives.
            </p>
          </motion.div>
        </motion.div>
      </div>

      <SourceCitation>
        FAR 13.106 (simplified acquisition procedures) | BOP procurement research | DoD commissary vendor programs
      </SourceCitation>
    </SlideLayout>
  )
}
