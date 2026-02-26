import { motion } from 'motion/react'
import { Building2, Shield, CloudLightning, GraduationCap } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { TARGET_AGENCIES } from '../../data/market'

const agencyIcons = [Building2, Shield, CloudLightning, GraduationCap]

function agencyAccent(color) {
  return color === 'teal' ? '#1B7A8A' : '#C9A84C'
}

export default function TargetAgenciesSlide() {
  const primaryAgencies = TARGET_AGENCIES.slice(0, 2)   // DOJ, Military
  const secondaryAgencies = TARGET_AGENCIES.slice(2)      // FEMA, Schools

  return (
    <div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
      <BackgroundRing size={450} className="-bottom-40 -left-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-navy-800/40 mb-3"
        >
          Procurement Channels
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          Your First Customers
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-navy-800/60 max-w-2xl"
        >
          Ranked by contract value and accessibility — your first calls.
        </motion.p>
        <GoldLine width={60} className="mt-3" delay={0.25} />
      </div>

      {/* Primary targets — larger cards */}
      <div className="grid grid-cols-2 gap-4 mb-4 relative z-10">
        {primaryAgencies.map((agency, i) => {
          const Icon = agencyIcons[i]
          const accent = agencyAccent(agency.color)
          return (
            <motion.div
              key={agency.name}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.3 + i * 0.1 }}
              className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-6 relative overflow-hidden"
            >
              {/* Left accent strip */}
              <div
                className="absolute left-0 top-3 bottom-3 w-[3px] rounded-full"
                style={{ backgroundColor: accent }}
              />
              <div className="flex items-start gap-4 pl-2">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ backgroundColor: `${accent}15` }}
                >
                  <Icon className="w-5 h-5" style={{ color: accent }} strokeWidth={1.5} />
                </div>
                <div className="flex-1">
                  <h3 className="font-body text-lg font-semibold text-navy-950">{agency.name}</h3>
                  <span className="font-body text-2xl font-bold block mt-1" style={{ color: accent }}>
                    {agency.stat}
                  </span>
                  <p className="font-body text-sm text-navy-800/60 leading-relaxed mt-2">
                    {agency.description}
                  </p>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Section label between rows */}
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.55 }}
        className="font-body text-[11px] font-semibold uppercase tracking-widest text-navy-800/30 mb-3 relative z-10"
      >
        Expansion Channels
      </motion.span>

      {/* Secondary targets — compact cards */}
      <div className="grid grid-cols-2 gap-4 relative z-10">
        {secondaryAgencies.map((agency, i) => {
          const Icon = agencyIcons[i + 2]
          const accent = agencyAccent(agency.color)
          return (
            <motion.div
              key={agency.name}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.5 + i * 0.1 }}
              className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] px-5 py-4 relative overflow-hidden"
            >
              {/* Left accent strip — thinner for secondary */}
              <div
                className="absolute left-0 top-3 bottom-3 w-[2px] rounded-full"
                style={{ backgroundColor: accent, opacity: 0.5 }}
              />
              <div className="flex items-start gap-3 pl-2">
                <div
                  className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
                  style={{ backgroundColor: `${accent}10` }}
                >
                  <Icon className="w-4 h-4" style={{ color: accent }} strokeWidth={1.5} />
                </div>
                <div className="flex-1">
                  <div className="flex items-baseline gap-2">
                    <h3 className="font-body text-base font-semibold text-navy-950">{agency.name}</h3>
                    <span className="font-body text-xs font-semibold uppercase tracking-wide" style={{ color: accent }}>
                      {agency.stat}
                    </span>
                  </div>
                  <p className="font-body text-[13px] text-navy-800/50 leading-relaxed mt-1.5">
                    {agency.description}
                  </p>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Source */}
      <div className="flex items-center justify-between mt-auto pt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="text-[10px] text-navy-800/35"
        >
          FPDS FY2024 | USASpending API | FL DOE 2024-25 | FEMA Disaster Declarations Database | FAR 13.201
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
