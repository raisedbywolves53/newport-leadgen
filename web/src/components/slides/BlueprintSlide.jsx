import { motion } from 'motion/react'
import { Truck, Brain, Handshake } from 'lucide-react'
import SlideLayout from '../ui/SlideLayout'
import { RESPONSIBILITIES } from '../../data/strategy'

export default function BlueprintSlide() {
  return (
    <SlideLayout className="!py-8 flex flex-col items-center justify-center">
      {/* Headline */}
      <motion.h2
        initial={{ opacity: 0, y: -15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.5 }}
        className="font-body text-3xl font-bold tracking-tight text-white text-center leading-tight"
      >
        The Blueprint Is Yours
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-slate-400 text-sm text-center mt-2 max-w-xl leading-relaxed"
      >
        Everything in this presentation — the market data, the competitive intelligence,
        the pipeline strategy — is yours whether we work together or not.
      </motion.p>

      {/* Partnership split */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.4 }}
        className="grid grid-cols-[1fr_auto_1fr] gap-5 mt-8 w-full max-w-3xl"
      >
        {/* Newport */}
        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-amber-500/15 flex items-center justify-center">
              <Truck className="w-4 h-4 text-amber-400" />
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
                className="text-slate-400 text-xs leading-relaxed flex items-start gap-2"
              >
                <span className="text-amber-500/60 mt-1">-</span>
                {item}
              </motion.li>
            ))}
          </ul>
        </div>

        {/* Center connector */}
        <div className="flex flex-col items-center justify-center gap-2">
          <Handshake className="w-5 h-5 text-slate-600" />
          <div className="w-px h-16 bg-gradient-to-b from-amber-500/30 via-slate-600 to-teal-500/30" />
        </div>

        {/* Still Mind */}
        <div className="rounded-xl border border-teal-500/20 bg-teal-500/5 p-4">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-teal-500/15 flex items-center justify-center">
              <Brain className="w-4 h-4 text-teal-400" />
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
                className="text-slate-400 text-xs leading-relaxed flex items-start gap-2"
              >
                <span className="text-teal-500/60 mt-1">-</span>
                {item}
              </motion.li>
            ))}
          </ul>
        </div>
      </motion.div>

      {/* Soft close */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.4 }}
        className="text-slate-500 text-xs text-center mt-8 max-w-lg leading-relaxed"
      >
        No obligation, no pressure. If the opportunity makes sense for your business,
        we're ready to build it with you.
      </motion.p>

      {/* Branding */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.6 }}
        className="mt-6 text-center"
      >
        <span className="text-slate-600 text-[10px] tracking-wider uppercase">
          Prepared by Still Mind Creative LLC
        </span>
      </motion.div>
    </SlideLayout>
  )
}
