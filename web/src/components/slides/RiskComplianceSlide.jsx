import { motion } from 'motion/react'
import { ShieldCheck, ShieldOff } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { COMPLIANCE_REQUIRED, COMPLIANCE_NOT_NEEDED } from '../../data/strategy'

export default function RiskComplianceSlide() {
  return (
    <SlideLayout className="!py-8">
      <SlideTitle>Risk & Compliance</SlideTitle>
      <SlideSubtitle>
        Food supply contracting has a lighter compliance burden than most government work.
        Here's exactly what's required — and what isn't.
      </SlideSubtitle>

      <div className="grid grid-cols-2 gap-5 mt-1">
        {/* Left — Required */}
        <motion.div
          initial={{ opacity: 0, x: -15 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck className="w-4.5 h-4.5 text-teal-400" />
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
                transition={{ delay: 0.3 + i * 0.08, duration: 0.25 }}
                className="rounded-lg border border-navy-700 bg-navy-800/40 p-2.5"
              >
                <div className="flex items-center justify-between mb-0.5">
                  <span className="text-offwhite text-xs font-semibold">{r.item}</span>
                  <span className="text-teal-400 text-xs font-mono font-semibold">{r.cost}</span>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                  <span className="text-slate-500">{r.timeline}</span>
                  <span className="text-slate-600">|</span>
                  <span className="text-slate-400">{r.note}</span>
                </div>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="mt-3 rounded-lg border border-teal-500/20 bg-teal-500/5 p-2.5"
          >
            <p className="text-teal-300 text-xs font-semibold">
              Total Entry Cost: $4K-$31.5K
            </p>
            <p className="text-slate-400 text-[10px] mt-0.5">
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
            <ShieldOff className="w-4.5 h-4.5 text-amber-400" />
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
                className="rounded-lg border border-navy-700/50 bg-navy-900/30 p-2.5"
              >
                <div className="flex items-center justify-between mb-0.5">
                  <span className="text-slate-400 text-xs font-semibold line-through decoration-slate-600">{r.item}</span>
                  <span className="text-slate-500 text-xs font-mono">{r.cost}</span>
                </div>
                <p className="text-slate-500 text-[10px]">{r.note}</p>
              </motion.div>
            ))}
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="mt-3 rounded-lg border border-amber-500/20 bg-amber-500/5 p-2.5"
          >
            <p className="text-amber-300 text-xs font-semibold">
              Avoided: $120K-$360K+
            </p>
            <p className="text-slate-400 text-[10px] mt-0.5">
              These are common government compliance costs that don't apply to food supply contracts.
            </p>
          </motion.div>
        </motion.div>
      </div>

      <SourceCitation>
        FAR 13/30/31 | CMMC 2.0 rule | SQF Institute pricing | Industry compliance estimates
      </SourceCitation>
    </SlideLayout>
  )
}
