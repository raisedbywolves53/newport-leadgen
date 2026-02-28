import { motion } from 'motion/react'
import { ShieldCheck, ShieldOff } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { COMPLIANCE_REQUIRED, COMPLIANCE_NOT_NEEDED } from '../../data/strategy'

export default function RiskComplianceSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-10 lg:px-14 pb-14 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-60" opacity={0.025} />

      {/* Header — full width, clear hierarchy */}
      <div className="mb-2 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5 block"
        >
          Risk & Compliance
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-1"
        >
          Low Barrier to Entry
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600"
        >
          Food supply contracting has a lighter compliance burden than most government work.
        </motion.p>
        <GoldLine width={60} className="mt-2" delay={0.25} />
      </div>

      {/* Two-column: Required vs Not Required */}
      <div className="grid grid-cols-2 gap-5 relative z-10">

        {/* LEFT — Required */}
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.4 }}
          className="rounded-xl border border-zinc-200 shadow-sm overflow-hidden bg-white flex flex-col"
        >
          {/* Column header */}
          <div className="px-4 py-3 flex items-center gap-3" style={{ backgroundColor: '#f0fdfa', borderBottom: '2px solid #d1fae5' }}>
            <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#1B7A8A18' }}>
              <ShieldCheck className="w-5 h-5" style={{ color: '#1B7A8A' }} strokeWidth={1.5} />
            </div>
            <div>
              <h4 className="font-body text-base font-bold" style={{ color: '#1B7A8A' }}>Required</h4>
              <span className="font-body text-[11px] text-zinc-500">What Newport needs to get started</span>
            </div>
          </div>

          {/* Rows */}
          <div className="flex flex-col">
            {COMPLIANCE_REQUIRED.map((r, i) => (
              <motion.div
                key={r.item}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.35 + i * 0.08, duration: 0.25 }}
                className="px-4 py-2.5 border-b border-zinc-100 flex items-start justify-between gap-4"
                style={{ backgroundColor: i % 2 === 0 ? '#ffffff' : '#fafafa' }}
              >
                <div className="flex-1">
                  <span className="font-body text-sm font-semibold text-zinc-900 block">{r.item}</span>
                  <span className="font-body text-xs text-zinc-600">{r.note}</span>
                </div>
                <div className="text-right shrink-0">
                  <span className="font-body text-sm font-bold font-mono block" style={{ color: '#1B7A8A' }}>{r.cost}</span>
                  <span className="font-body text-[11px] text-zinc-400">{r.timeline}</span>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Total footer */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="px-4 py-3 flex items-center justify-between"
            style={{ backgroundColor: '#f0fdfa', borderTop: '2px solid #d1fae5' }}
          >
            <div>
              <span className="font-body text-base font-bold block" style={{ color: '#1B7A8A' }}>Total Entry Cost</span>
              <span className="font-body text-xs text-zinc-500">$0 if food safety certs already held</span>
            </div>
            <span className="font-body text-2xl font-bold font-mono" style={{ color: '#1B7A8A' }}>$4K–$31.5K</span>
          </motion.div>
        </motion.div>

        {/* RIGHT — Not Required */}
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.4 }}
          className="rounded-xl border border-zinc-200 shadow-sm overflow-hidden bg-white flex flex-col"
        >
          {/* Column header */}
          <div className="px-4 py-3 flex items-center gap-3" style={{ backgroundColor: '#fffbeb', borderBottom: '2px solid #fde68a' }}>
            <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#E8913A18' }}>
              <ShieldOff className="w-5 h-5" style={{ color: '#E8913A' }} strokeWidth={1.5} />
            </div>
            <div>
              <h4 className="font-body text-base font-bold" style={{ color: '#E8913A' }}>Not Required</h4>
              <span className="font-body text-[11px] text-zinc-500">Costs Newport avoids entirely</span>
            </div>
          </div>

          {/* Rows */}
          <div className="flex flex-col">
            {COMPLIANCE_NOT_NEEDED.map((r, i) => (
              <motion.div
                key={r.item}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + i * 0.08, duration: 0.25 }}
                className="px-4 py-2.5 border-b border-zinc-100 flex items-start justify-between gap-4"
                style={{ backgroundColor: i % 2 === 0 ? '#ffffff' : '#fafafa' }}
              >
                <div className="flex-1">
                  <span className="font-body text-sm font-semibold text-zinc-900 block">{r.item}</span>
                  <span className="font-body text-xs text-zinc-600">{r.note}</span>
                </div>
                <span className="font-body text-sm font-bold font-mono shrink-0" style={{ color: '#E8913A' }}>{r.cost}</span>
              </motion.div>
            ))}
          </div>

          {/* Total footer */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="px-4 py-3 flex items-center justify-between"
            style={{ backgroundColor: '#fffbeb', borderTop: '2px solid #fde68a' }}
          >
            <div>
              <span className="font-body text-base font-bold block" style={{ color: '#E8913A' }}>Total Avoided</span>
              <span className="font-body text-xs text-zinc-500">Doesn't apply to food supply</span>
            </div>
            <span className="font-body text-2xl font-bold font-mono" style={{ color: '#E8913A' }}>$120K–$360K+</span>
          </motion.div>
        </motion.div>
      </div>

      <SourceCitation>
        FAR 13/30/31 | CMMC 2.0 rule | SQF Institute pricing | Industry compliance estimates
      </SourceCitation>
    </div>
  )
}
