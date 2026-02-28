import { motion } from 'motion/react'
import { TrendingDown, Shield, Lightbulb } from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'

const STATS = [
  {
    label: 'Continuous FL Operations',
    value: '30 Years',
    accent: '#C9A84C',
    badge: { text: 'Since 1996', variant: 'text-zinc-600' },
    footerHighlight: 'Real warehouse, fleet, W-2 workforce',
    footerDescription: 'Plantation, FL',
  },
  {
    label: 'Post-Fraud Vacuum',
    value: '1,091',
    accent: '#C9A84C',
    badge: { icon: TrendingDown, text: '25% cleared', variant: 'text-red-600' },
    footerHighlight: 'SBA cleared Jan 2026',
    footerDescription: 'DOJ prosecuted $550M scheme',
  },
  {
    label: 'Micro-Purchase Threshold',
    value: '83%',
    accent: '#1B7A8A',
    badge: { icon: Shield, text: 'Below $15K', variant: 'text-zinc-600' },
    footerHighlight: 'No bid, no past performance needed',
    footerDescription: 'Fastest path to first contract',
  },
  {
    label: 'Infrastructure Edge',
    value: '$5M',
    accent: '#1B7A8A',
    badge: { text: 'Entry Tier', variant: 'text-zinc-600' },
    footerHighlight: 'FL competitors #5–10 at $1–5M',
    footerDescription: 'Less capability than Newport',
  },
]

export default function WhyNewportSlide() {
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
          Competitive Moat
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          Why Newport Wins
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          A 30-year track record can't be manufactured. In the current
          post-fraud environment, agencies need vendors with auditable,
          transparent histories.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — 4 pillars HORIZONTAL */}
      <div className="grid grid-cols-4 gap-4 mb-4 relative z-10">
        {STATS.map((stat, i) => {
          const BadgeIcon = stat.badge.icon
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ y: -2 }}
              transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-6 py-6 cursor-default"
            >
              <div className="px-6 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500">{stat.label}</span>
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 ${stat.badge.variant}`}
                  >
                    {BadgeIcon && <BadgeIcon className="w-3 h-3" />}
                    {stat.badge.text}
                  </span>
                </div>
                <span
                  className="text-2xl font-semibold tabular-nums tracking-tight"
                  style={{ color: stat.accent }}
                >
                  {stat.value}
                </span>
              </div>
              <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
                <div className="flex items-center gap-2 font-medium text-zinc-900">
                  {stat.footerHighlight}
                </div>
                <div className="text-zinc-500 text-xs">
                  {stat.footerDescription}
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* ZONE 3: Full-width InsightCard */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.5 }}
        className="rounded-xl bg-amber-50/50 border border-amber-200/50 shadow-sm hover:shadow-md hover:border-amber-300/50 transition-all duration-200 ease-out p-6 relative z-10"
      >
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-md bg-amber-100 flex items-center justify-center shrink-0">
            <Lightbulb
              className="w-4 h-4 text-amber-600"
              strokeWidth={1.5}
            />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-zinc-950 mb-1">
              The Verifiable History Agencies Now Require
            </h4>
            <p className="text-sm text-zinc-600 leading-relaxed">
              In the post-DOGE, post-fraud environment — clean vendors are the
              scarcest commodity. Newport's 30 years of continuous Florida
              operations, real infrastructure, and clean audit history is a
              competitive moat that took decades to build and can't be
              manufactured.
            </p>
          </div>
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
          SBA.gov (Jan 28 2026) · DOJ OPA (Jun 12 2025) · USASpending FY2024 ·
          FPDS Competition Data
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
