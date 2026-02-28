import { motion } from 'motion/react'
import {
  Search,
  FileText,
  Send,
  CheckCircle,
  Truck,
  ChevronRight,
  Globe,
  Building2,
  Eye,
  Users,
  TrendingUp,
} from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { PIPELINE_STAGES, SOURCING_CHANNELS } from '../../data/strategy'

const STAGE_ICONS = [Search, FileText, Send, CheckCircle, Truck]
const CHANNEL_ICONS = [Globe, Building2, Eye, Users]

const CHANNEL_BADGES = [
  { text: 'BUILT', variant: 'text-emerald-700' },
  { text: 'FREE', variant: 'text-zinc-600' },
  { text: '$6.5K/YR', variant: 'text-zinc-600' },
  { text: 'FREE', variant: 'text-zinc-600' },
]

export default function HowItWorksSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      {/* ZONE 1: Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block text-xs font-medium uppercase tracking-widest text-zinc-400 mb-3"
        >
          Process
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          How Government Contracts Work
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          From opportunity identification to contract award — a systematic
          pipeline.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — 4 sourcing channels HORIZONTAL */}
      <div className="grid grid-cols-4 gap-4 mb-4 relative z-10">
        {SOURCING_CHANNELS.map((ch, i) => {
          const Icon = CHANNEL_ICONS[i]
          const isFirst = i === 0
          const accent = isFirst ? '#C9A84C' : '#1B7A8A'
          const badge = CHANNEL_BADGES[i]

          return (
            <motion.div
              key={ch.title}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
            >
              <div className="px-6 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500">{ch.title}</span>
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 ${badge.variant}`}
                  >
                    {isFirst && <TrendingUp className="w-3 h-3" />}
                    {badge.text}
                  </span>
                </div>
                <span
                  className="text-2xl font-semibold tabular-nums tracking-tight"
                  style={{ color: accent }}
                >
                  {ch.cost}
                </span>
              </div>
              <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
                <div className="flex items-center gap-2 font-medium text-zinc-900 line-clamp-1">
                  <Icon className="w-4 h-4 shrink-0" /> {ch.title.split(': ')[1] || ch.title}
                </div>
                <div className="text-zinc-500 text-xs line-clamp-2">
                  {ch.description}
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* ZONE 3: Pipeline card — FULL WIDTH (replaces chart) */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm relative overflow-hidden relative z-10"
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

        {/* CardHeader */}
        <div className="p-6 pb-0 pl-8">
          <h3 className="text-lg font-semibold text-zinc-950">
            Procurement Pipeline
          </h3>
          <p className="text-sm text-zinc-500 mt-1">
            5 stages from identification to delivery
          </p>
        </div>

        {/* CardContent — horizontal pipeline */}
        <div className="p-6 pt-4 pl-8">
          <div className="flex items-center justify-center gap-3">
            {PIPELINE_STAGES.map((stage, i) => {
              const Icon = STAGE_ICONS[i]
              return (
                <div key={stage.name} className="flex items-center gap-3">
                  <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.35 + i * 0.1, duration: 0.4 }}
                    className="flex flex-col items-center"
                  >
                    <div className="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center">
                      <Icon
                        className="w-5 h-5 text-zinc-600"
                        strokeWidth={1.5}
                      />
                    </div>
                    <span className="text-xs font-medium text-zinc-900 mt-2">
                      {stage.name}
                    </span>
                    <span className="text-[10px] text-zinc-400">
                      {stage.description}
                    </span>
                  </motion.div>
                  {i < PIPELINE_STAGES.length - 1 && (
                    <ChevronRight className="w-4 h-4 text-zinc-300 -mt-5" />
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* CardFooter */}
        <div className="px-6 py-3 pl-8 border-t border-zinc-100">
          <span className="text-xs text-zinc-400">
            Typical cycle: 30–180 days depending on contract size
          </span>
        </div>
      </motion.div>

      {/* ZONE 5: Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-[10px] text-zinc-300"
        >
          SAM.gov API | MyFloridaMarketPlace | GovSpend ($6.5K/yr) | CLEATUS
          ($3K/yr) | HigherGov ($3.5K/yr)
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
