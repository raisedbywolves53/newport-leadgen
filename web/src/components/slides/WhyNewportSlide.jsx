import { motion } from 'motion/react'

const stats = [
  {
    value: '30',
    label: 'Years',
    description: 'Uninterrupted wholesale distribution in Florida. Real warehouse, real fleet, real W-2 workforce.',
    color: '#C9A84C',
  },
  {
    value: '1,091',
    label: 'Firms Suspended',
    description: 'SBA cleared 25% of the 8(a) program in Jan 2026. Agencies need vendors with verifiable histories.',
    color: '#C9A84C',
  },
  {
    value: '83%',
    label: 'Micro-Purchase',
    description: 'Of FL food contracts fall below $15K — no competitive bidding, no past performance required to win.',
    color: '#1B7A8A',
  },
  {
    value: '$5M',
    label: 'Entry Tier',
    description: 'FL competitors #5-10 do $1-5M with less infrastructure. Newport enters with trucks, cold chain, and routes.',
    color: '#1B7A8A',
  },
]

export default function WhyNewportSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-16">
      <motion.h2
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl font-bold tracking-tight text-white mb-3"
      >
        Why Newport Wins
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-sm text-slate-400 mb-8"
      >
        A competitive moat built over three decades — exactly what agencies need right now.
      </motion.p>

      <div className="flex gap-6">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: 0.3 + i * 0.1 }}
            className="flex-1 h-64 rounded-3xl bg-gradient-to-br from-[#0c1220] via-[#131d30] to-[#0c1220] border border-white/5 p-6 flex flex-col justify-end"
          >
            <span
              className="font-body text-5xl font-bold tracking-tight leading-none mb-2 drop-shadow-lg"
              style={{ color: stat.color }}
            >
              {stat.value}
            </span>
            <span className="font-body text-sm font-semibold text-white uppercase tracking-wide mb-2">
              {stat.label}
            </span>
            <span className="text-white/50 text-xs leading-relaxed">
              {stat.description}
            </span>
          </motion.div>
        ))}
      </div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.0 }}
        className="text-[10px] text-slate-600 mt-6"
      >
        SBA.gov (Jan 28, 2026) — 1,091 firms suspended | DOJ OPA (Jun 12, 2025) — $550M scheme | USASpending FY2024
      </motion.p>
    </div>
  )
}
