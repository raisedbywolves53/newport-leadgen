import { motion } from 'motion/react'
import { Building2, Shield, CloudLightning, GraduationCap } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { TARGET_AGENCIES } from '../../data/market'

const agencyIcons = [Building2, Shield, CloudLightning, GraduationCap]
const colorMap = {
  teal: { accent: 'bg-teal-500', text: 'text-teal-400', border: 'border-teal-500/20', iconBg: 'bg-teal-500/15' },
  amber: { accent: 'bg-amber-500', text: 'text-amber-400', border: 'border-amber-500/20', iconBg: 'bg-amber-500/15' },
}

export default function TargetAgenciesSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 max-w-7xl mx-auto relative overflow-hidden">
      <BackgroundRing size={450} className="-bottom-40 -left-40" opacity={0.02} />

      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-teal-500 mb-2"
      >
        Procurement Channels
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
      >
        Who's Buying: Target Agencies
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-navy-800/60 mb-1"
      >
        Four procurement channels — each with distinct entry paths and competitive dynamics.
      </motion.p>
      <GoldLine width={60} className="mb-6" delay={0.25} />

      <div className="grid grid-cols-2 gap-4 mt-2">
        {TARGET_AGENCIES.map((agency, i) => {
          const Icon = agencyIcons[i]
          const c = colorMap[agency.color]
          return (
            <motion.div
              key={agency.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.3 + i * 0.1 }}
              className={`rounded-xl border ${c.border} bg-white/70 backdrop-blur-sm shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-5 relative overflow-hidden`}
            >
              {/* Top accent */}
              <div className={`absolute top-0 left-0 right-0 h-0.5 ${c.accent}`} />

              <div className="flex items-start gap-3 mb-2">
                <div className={`w-7 h-7 rounded-lg ${c.iconBg} flex items-center justify-center shrink-0`}>
                  <Icon className={`w-4 h-4 ${c.text}`} strokeWidth={1.5} />
                </div>
                <div>
                  <h3 className="text-navy-950 font-semibold text-sm">{agency.name}</h3>
                  <span className={`${c.text} font-body text-base font-bold`}>{agency.stat}</span>
                </div>
              </div>
              <p className="text-navy-800/60 text-xs leading-relaxed">{agency.description}</p>
            </motion.div>
          )
        })}
      </div>

      <SourceCitation>
        FPDS FY2024 | USASpending API | FL DOE 2024-25 | FEMA Disaster Declarations Database | FAR 13.201
      </SourceCitation>
    </div>
  )
}
