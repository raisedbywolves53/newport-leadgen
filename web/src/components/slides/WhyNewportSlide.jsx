import { motion } from 'motion/react'
import { Clock, Shield, Truck, FileCheck } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'

const cards = [
  {
    icon: Clock,
    title: '30 Years of Continuous Operations',
    body: 'Three decades of uninterrupted wholesale distribution in Florida. Real warehouse, real fleet, real W-2 workforce. The kind of audit trail agencies need — and can\'t be manufactured.',
    color: 'teal',
  },
  {
    icon: Shield,
    title: 'Post-Fraud Competitive Moat',
    body: 'SBA suspended 1,091 firms from the 8(a) program in January 2026 — 25% of the entire program. DOJ uncovered a $550M bribery scheme. Agencies need vendors with verifiable, transparent histories. Newport is exactly that.',
    color: 'amber',
  },
  {
    icon: Truck,
    title: 'Infrastructure Already in Place',
    body: 'Trucks, routes, cold chain, warehouse — all operating. Government delivery is incremental volume on existing routes. Competitors #5-10 in FL are doing $1-5M with less infrastructure.',
    color: 'teal',
  },
  {
    icon: FileCheck,
    title: 'No Past Performance Required (Year 1)',
    body: '83% of FL food contracts fall below the $15K micro-purchase threshold — agencies can buy from any SAM-registered vendor without competitive bidding. Commercial experience qualifies for entry.',
    color: 'teal',
  },
]

const colorMap = {
  teal: { bg: 'bg-teal-500/8', border: 'border-teal-500/20', icon: 'text-teal-400', iconBg: 'bg-teal-500/15' },
  amber: { bg: 'bg-amber-500/8', border: 'border-amber-500/20', icon: 'text-amber-400', iconBg: 'bg-amber-500/15' },
}

export default function WhyNewportSlide() {
  return (
    <SlideLayout>
      <SlideTitle>Why Newport Wins</SlideTitle>
      <SlideSubtitle>
        A competitive moat built over three decades — exactly what agencies need right now.
      </SlideSubtitle>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mt-2">
        {cards.map((card, i) => {
          const c = colorMap[card.color]
          return (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 + i * 0.1 }}
              className={`rounded-xl border ${c.border} ${c.bg} p-5`}
            >
              <div className={`inline-flex items-center justify-center w-9 h-9 rounded-lg ${c.iconBg} mb-3`}>
                <card.icon className={`w-4.5 h-4.5 ${c.icon}`} />
              </div>
              <h3 className="font-body text-lg font-semibold text-white mb-2">
                {card.title}
              </h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                {card.body}
              </p>
            </motion.div>
          )
        })}
      </div>

      <SourceCitation>
        SBA.gov (Jan 28, 2026) — 1,091 firms suspended | DOJ OPA (Jun 12, 2025) — $550M scheme | USASpending FY2024 — contract size distribution
      </SourceCitation>
    </SlideLayout>
  )
}
