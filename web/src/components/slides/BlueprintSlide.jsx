import { motion } from 'motion/react'
import { Truck, Brain, Handshake } from 'lucide-react'
import SlideLayout from '../ui/SlideLayout'
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
        initial={{ opacity: 0, y: -15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="font-body text-4xl md:text-5xl font-bold tracking-tight text-navy-950 text-center leading-tight"
      >
        The Blueprint Is Yours
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-navy-800/60 text-[15px] text-center mt-3 max-w-xl leading-relaxed"
      >
        Everything in this presentation — the market data, the competitive intelligence,
        the pipeline strategy — is yours whether we work together or not.
      </motion.p>

      {/* Partnership split */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.4 }}
        className="grid grid-cols-[1fr_auto_1fr] gap-5 mt-10 w-full max-w-3xl"
      >
        {/* Newport */}
        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-5 relative overflow-hidden">
          <div className="absolute left-0 top-4 bottom-4 w-1 rounded-full" style={{ backgroundColor: '#E8913A' }} />
          <div className="pl-2">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 rounded-lg bg-amber-500/15 flex items-center justify-center">
                <Truck className="w-4 h-4 text-amber-400" strokeWidth={1.5} />
              </div>
              <h4 className="text-amber-400 font-semibold text-sm">Newport Owns</h4>
            </div>
            <ul className="space-y-1.5">
              {RESPONSIBILITIES.partnership.newport.map((item, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + i * 0.06 }}
                  className="text-navy-800/65 text-xs leading-relaxed flex items-start gap-2"
                >
                  <span className="text-amber-500/60 mt-1">-</span>
                  {item}
                </motion.li>
              ))}
            </ul>
          </div>
        </div>

        {/* Center connector */}
        <div className="flex flex-col items-center justify-center gap-2">
          <Handshake className="w-5 h-5 text-navy-800/40" />
          <div className="w-px h-16 bg-gradient-to-b from-amber-500/30 via-navy-800/40 to-teal-500/30" />
        </div>

        {/* Still Mind */}
        <div className="rounded-xl border border-teal-500/20 bg-teal-500/5 p-5 relative overflow-hidden">
          <div className="absolute right-0 top-4 bottom-4 w-1 rounded-full" style={{ backgroundColor: '#1B7A8A' }} />
          <div className="pr-2">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-7 h-7 rounded-lg bg-teal-500/15 flex items-center justify-center">
                <Brain className="w-4 h-4 text-teal-400" strokeWidth={1.5} />
              </div>
              <h4 className="text-teal-400 font-semibold text-sm">Still Mind Delivers</h4>
            </div>
            <ul className="space-y-1.5">
              {RESPONSIBILITIES.partnership.stillMind.map((item, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: 8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + i * 0.06 }}
                  className="text-navy-800/65 text-xs leading-relaxed flex items-start gap-2"
                >
                  <span className="text-teal-500/60 mt-1">-</span>
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
        className="text-navy-800/50 text-xs text-center mt-10 max-w-lg leading-relaxed"
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
        <span className="text-navy-800/40 text-[10px] tracking-wider uppercase">
          Prepared by Still Mind Creative LLC
        </span>
      </motion.div>
    </div>
  )
}
