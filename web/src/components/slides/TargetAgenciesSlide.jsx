import { motion } from 'motion/react'
import { Building2, Shield, CloudLightning, GraduationCap } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { TARGET_AGENCIES } from '../../data/market'

const agencyIcons = [Building2, Shield, CloudLightning, GraduationCap]

export default function TargetAgenciesSlide() {
  const doj = TARGET_AGENCIES[0]
  const military = TARGET_AGENCIES[1]
  const fema = TARGET_AGENCIES[2]
  const schools = TARGET_AGENCIES[3]

  return (
    <div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
      <BackgroundRing size={450} className="-bottom-40 -left-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-6 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-3"
        >
          Procurement Channels
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          Your First Customers
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-zinc-600 max-w-2xl"
        >
          Ranked by contract value and accessibility — your first calls.
        </motion.p>

        <GoldLine width={60} className="mt-4" delay={0.25} />
      </div>

      {/* Bento grid */}
      <div className="grid grid-cols-2 gap-4 relative z-10" style={{ height: '460px' }}>

        {/* DOJ — Hero card */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.3 }}
          className="rounded-xl bg-white p-10 shadow-sm border border-zinc-200 flex flex-col justify-center relative overflow-hidden"
        >
          <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#1B7A8A' }} />

          <div className="pl-4">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
              style={{ backgroundColor: '#1B7A8A15' }}
            >
              <Building2 className="w-6 h-6" style={{ color: '#1B7A8A' }} strokeWidth={1.8} />
            </div>

            <div className="flex items-baseline gap-3 mb-2">
              <span className="font-body text-5xl font-semibold tracking-tighter leading-none" style={{ color: '#1B7A8A' }}>
                $3.7M
              </span>
              <span className="font-body text-lg font-medium text-zinc-400 uppercase tracking-wide">
                71 contracts
              </span>
            </div>

            <h3 className="font-body text-xl font-semibold text-zinc-950 mt-4 mb-3">
              {doj.name}
            </h3>

            <p className="font-body text-[15px] leading-relaxed text-zinc-600">
              {doj.description}
            </p>

            <div className="flex items-center gap-2 mt-5 pt-5 border-t border-zinc-100">
              <span className="font-body text-xs font-medium text-zinc-400">#1 FL Food Buyer</span>
              <span className="text-zinc-300">·</span>
              <span className="font-body text-xs font-medium text-zinc-400">Direct Competitive Target</span>
            </div>
          </div>
        </motion.div>

        {/* Right column — Military + FEMA + Schools stacked */}
        <div className="flex flex-col gap-4">

          {/* Military */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.4 }}
            className="rounded-xl bg-white p-6 shadow-sm border border-zinc-200 flex-1 flex flex-col justify-center"
          >
            <div className="flex items-start gap-4">
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                style={{ backgroundColor: '#1B7A8A15' }}
              >
                <Shield className="w-5 h-5" style={{ color: '#1B7A8A' }} strokeWidth={1.5} />
              </div>
              <div className="flex-1">
                <div className="flex items-baseline gap-2 mb-1">
                  <span className="font-body text-2xl font-semibold tracking-tight leading-none" style={{ color: '#1B7A8A' }}>
                    $2.3M
                  </span>
                  <span className="font-body text-[11px] font-medium text-zinc-400 uppercase tracking-wide">
                    43 contracts
                  </span>
                </div>
                <h3 className="font-body text-base font-semibold text-zinc-950 mb-1.5">
                  {military.name}
                </h3>
                <p className="font-body text-sm leading-relaxed text-zinc-600">
                  {military.description}
                </p>
              </div>
            </div>
          </motion.div>

          {/* FEMA */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.5 }}
            className="rounded-xl bg-white p-6 shadow-sm border border-zinc-200 flex-1 flex flex-col justify-center"
          >
            <div className="flex items-start gap-4">
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                style={{ backgroundColor: '#C9A84C15' }}
              >
                <CloudLightning className="w-5 h-5" style={{ color: '#C9A84C' }} strokeWidth={1.5} />
              </div>
              <div className="flex-1">
                <div className="flex items-baseline gap-2 mb-1">
                  <span className="font-body text-2xl font-semibold tracking-tight leading-none" style={{ color: '#C9A84C' }}>
                    $25K
                  </span>
                  <span className="font-body text-[11px] font-medium text-zinc-400 uppercase tracking-wide">
                    Emergency Threshold
                  </span>
                </div>
                <h3 className="font-body text-base font-semibold text-zinc-950 mb-1.5">
                  {fema.name}
                </h3>
                <p className="font-body text-sm leading-relaxed text-zinc-600">
                  {fema.description}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Schools */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.6 }}
            className="rounded-xl bg-white p-6 shadow-sm border border-zinc-200 flex-1 flex flex-col justify-center"
          >
            <div className="flex items-start gap-4">
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                style={{ backgroundColor: '#C9A84C15' }}
              >
                <GraduationCap className="w-5 h-5" style={{ color: '#C9A84C' }} strokeWidth={1.5} />
              </div>
              <div className="flex-1">
                <div className="flex items-baseline gap-2 mb-1">
                  <span className="font-body text-2xl font-semibold tracking-tight leading-none" style={{ color: '#C9A84C' }}>
                    $750M+
                  </span>
                  <span className="font-body text-[11px] font-medium text-zinc-400 uppercase tracking-wide">
                    FL Market
                  </span>
                </div>
                <h3 className="font-body text-base font-semibold text-zinc-950 mb-1.5">
                  {schools.name}
                </h3>
                <p className="font-body text-sm leading-relaxed text-zinc-600">
                  {schools.description}
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="text-[10px] text-zinc-300"
        >
          FPDS FY2024 · USASpending API · FL DOE 2024-25 · FEMA Disaster Declarations · FAR 13.201
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
