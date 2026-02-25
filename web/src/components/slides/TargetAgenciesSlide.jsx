import { motion } from 'motion/react'
import { Building2, Shield, CloudLightning, GraduationCap } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { TARGET_AGENCIES } from '../../data/market'

const agencyIcons = [Building2, Shield, CloudLightning, GraduationCap]
const colorMap = {
  teal: { accent: 'bg-teal-500', text: 'text-teal-400', border: 'border-teal-500/20' },
  amber: { accent: 'bg-amber-500', text: 'text-amber-400', border: 'border-amber-500/20' },
}

export default function TargetAgenciesSlide() {
  return (
    <SlideLayout>
      <SlideTitle>Who's Buying: Target Agencies</SlideTitle>
      <SlideSubtitle>
        Four procurement channels — each with distinct entry paths and competitive dynamics.
      </SlideSubtitle>

      <div className="grid grid-cols-2 gap-4 mt-2">
        {TARGET_AGENCIES.map((agency, i) => {
          const Icon = agencyIcons[i]
          const c = colorMap[agency.color]
          return (
            <motion.div
              key={agency.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 + i * 0.1 }}
              className={`rounded-xl border ${c.border} bg-white/70 p-5 relative overflow-hidden`}
            >
              {/* Top accent */}
              <div className={`absolute top-0 left-0 right-0 h-0.5 ${c.accent}`} />

              <div className="flex items-start gap-3 mb-2">
                <Icon className={`w-5 h-5 ${c.text} mt-0.5`} />
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
    </SlideLayout>
  )
}
