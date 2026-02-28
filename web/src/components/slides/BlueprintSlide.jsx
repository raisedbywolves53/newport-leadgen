import { motion } from 'motion/react'
import { Truck, Brain, Handshake } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { RESPONSIBILITIES } from '../../data/strategy'

export default function BlueprintSlide() {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto relative overflow-hidden">
      {/* Background decorative rings */}
      <BackgroundRing size={600} className="-top-60 left-1/2 -translate-x-1/2" opacity={0.025} color="#C9A84C" />
      <BackgroundRing size={350} className="bottom-20 -left-40" opacity={0.02} />

      {/* Gold accent line above headline */}
      <GoldLine width={60} className="mb-6" delay={0.15} />

      {/* Headline */}
      <motion.h2
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.45 }}
        className="font-body text-3xl md:text-4xl font-semibold tracking-tight text-zinc-950 text-center leading-tight"
      >
        The Blueprint Is Yours
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-zinc-600 text-[15px] text-center mt-3 max-w-xl leading-relaxed"
      >
        Everything in this presentation — the market data, the competitive intelligence,
        the pipeline strategy — is yours whether we work together or not.
      </motion.p>

      {/* Partnership split */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.4 }}
        className="grid grid-cols-[1fr_auto_1fr] gap-6 mt-10 w-full max-w-4xl"
      >
        {/* Newport */}
        <div className="rounded-xl border border-zinc-200 bg-white shadow-sm p-7 relative overflow-hidden">
          <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
          <div className="pl-3">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#C9A84C15' }}>
                <Truck className="w-5 h-5" style={{ color: '#C9A84C' }} strokeWidth={1.5} />
              </div>
              <h4 className="font-semibold text-base" style={{ color: '#C9A84C' }}>Newport Owns</h4>
            </div>
            <ul className="space-y-2.5">
              {RESPONSIBILITIES.partnership.newport.map((item, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + i * 0.06 }}
                  className="text-zinc-600 text-sm leading-relaxed flex items-start gap-2"
                >
                  <span className="mt-0.5" style={{ color: '#C9A84C', opacity: 0.6 }}>-</span>
                  {item}
                </motion.li>
              ))}
            </ul>
          </div>
        </div>

        {/* Center connector */}
        <div className="flex flex-col items-center justify-center gap-2">
          <Handshake className="w-6 h-6 text-zinc-400" />
          <div className="w-px h-20" style={{ background: 'linear-gradient(to bottom, #C9A84C50, #a1a1aa60, #1B7A8A50)' }} />
        </div>

        {/* Still Mind */}
        <div className="rounded-xl border border-zinc-200 bg-white shadow-sm p-7 relative overflow-hidden">
          <div className="absolute right-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#1B7A8A' }} />
          <div className="pr-3">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#1B7A8A15' }}>
                <Brain className="w-5 h-5" style={{ color: '#1B7A8A' }} strokeWidth={1.5} />
              </div>
              <h4 className="font-semibold text-base" style={{ color: '#1B7A8A' }}>Still Mind Delivers</h4>
            </div>
            <ul className="space-y-2.5">
              {RESPONSIBILITIES.partnership.stillMind.map((item, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: 8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + i * 0.06 }}
                  className="text-zinc-600 text-sm leading-relaxed flex items-start gap-2"
                >
                  <span className="mt-0.5" style={{ color: '#1B7A8A', opacity: 0.6 }}>-</span>
                  {item}
                </motion.li>
              ))}
            </ul>
          </div>
        </div>
      </motion.div>

      {/* Soft close */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4 }}
        className="text-zinc-500 text-xs text-center mt-10 max-w-lg leading-relaxed"
      >
        No obligation, no pressure. If the opportunity makes sense for your business,
        we're ready to build it with you.
      </motion.p>

      {/* Compass star + credit */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6 }}
        className="mt-5 flex flex-col items-center gap-3"
      >
        <CompassStar size={20} opacity={0.3} delay={1.6} />
        <span className="text-zinc-400 text-[10px] tracking-wider uppercase">
          Prepared by Still Mind Creative LLC
        </span>
      </motion.div>
    </div>
  )
}
