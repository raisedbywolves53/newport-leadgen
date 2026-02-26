import { motion } from 'motion/react'
import { ShieldCheck, ShieldOff } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { COMPLIANCE_REQUIRED, COMPLIANCE_NOT_NEEDED } from '../../data/strategy'

export default function RiskComplianceSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-8 max-w-7xl mx-auto relative overflow-hidden">
      {/* Background ring */}
      <BackgroundRing size={500} className="-top-40 -right-60" opacity={0.025} />

      {/* Dramatic cost contrast — the visual anchor */}
      <div className="flex items-end gap-8 mb-2 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <span className="font-body text-xs font-semibold uppercase tracking-widest text-teal-500 block mb-2">
            Compliance
          </span>
          <div className="flex items-baseline gap-3">
            <span className="font-body text-5xl md:text-6xl font-bold tracking-tighter leading-none" style={{ color: '#1B7A8A' }}>
              $4K
            </span>
            <span className="font-body text-xl text-navy-800/30 font-light">vs</span>
            <span className="font-body text-5xl md:text-6xl font-bold tracking-tighter leading-none" style={{ color: '#E8913A' }}>
              $360K
            </span>
          </div>
          <span className="font-body text-xs text-navy-800/50 mt-1 block">
            Entry cost vs. typical government compliance burden avoided
          </span>
        </motion.div>
      </div>

      <div className="flex items-center gap-4 mb-4 relative z-10">
        <GoldLine width={60} delay={0.25} />
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="font-body text-base text-navy-800/60"
        >
          Food supply contracting has a lighter compliance burden than most government work.
        </motion.p>
      </div>

      <div className="grid grid-cols-2 gap-5 relative z-10">
        {/* Left — Required */}
        <motion.div
          initial={{ opacity: 0, x: -15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-teal-500/15 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4 text-teal-400" strokeWidth={1.5} />
            </div>
            <h4 className="text-teal-400 font-semibold text-sm uppercase tracking-wider">
              Required
            </h4>
          </div>

          <div className="space-y-1.5">
            {COMPLIANCE_REQUIRED.map((r, i) => (
              <motion.div
                key={r.item}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 + i * 0.08, duration: 0.25 }}
                className="rounded-xl border border-black/[0.06] bg-white/70 backdrop-blur-sm shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-2.5"
              >
                <div className="flex items-center justify-between mb-0.5">
                  <span className="text-navy-950 text-xs font-semibold">{r.item}</span>
                  <span className="text-teal-400 text-xs font-mono font-semibold">{r.cost}</span>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                  <span className="text-navy-800/50">{r.timeline}</span>
                  <span className="text-navy-800/40">|</span>
                  <span className="text-navy-800/60">{r.note}</span>
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="mt-3 rounded-xl border border-teal-500/20 bg-teal-500/5 p-2.5"
          >
            <p className="text-teal-300 text-xs font-semibold">
              Total Entry Cost: $4K-$31.5K
            </p>
            <p className="text-navy-800/60 text-[10px] mt-0.5">
              $0 if food safety certs already held. Legal review + insurance may already be in place.
            </p>
          </motion.div>
        </motion.div>

        {/* Right — NOT Required */}
        <motion.div
          initial={{ opacity: 0, x: 15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <div className="w-7 h-7 rounded-lg bg-amber-500/15 flex items-center justify-center">
              <ShieldOff className="w-4 h-4 text-amber-400" strokeWidth={1.5} />
            </div>
            <h4 className="text-amber-400 font-semibold text-sm uppercase tracking-wider">
              Not Required
            </h4>
          </div>

          <div className="space-y-1.5">
            {COMPLIANCE_NOT_NEEDED.map((r, i) => (
              <motion.div
                key={r.item}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.08, duration: 0.25 }}
                className="rounded-xl border border-black/[0.06] bg-white/50 backdrop-blur-sm p-2.5"
              >
                <div className="flex items-center justify-between mb-0.5">
                  <span className="text-navy-800/50 text-xs font-semibold">{r.item}</span>
                  <span className="text-navy-800/50 text-xs font-mono">{r.cost}</span>
                </div>
                <p className="text-navy-800/50 text-[10px]">{r.note}</p>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="mt-3 rounded-xl border border-amber-500/20 bg-amber-500/5 p-2.5"
          >
            <p className="text-amber-300 text-xs font-semibold">
              Avoided: $120K-$360K+
            </p>
            <p className="text-navy-800/60 text-[10px] mt-0.5">
              These are common government compliance costs that don't apply to food supply contracts.
            </p>
          </motion.div>
        </motion.div>
      </div>

      <SourceCitation>
        FAR 13/30/31 | CMMC 2.0 rule | SQF Institute pricing | Industry compliance estimates
      </SourceCitation>
    </div>
  )
}
