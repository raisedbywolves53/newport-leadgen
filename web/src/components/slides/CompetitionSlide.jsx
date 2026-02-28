import { motion } from 'motion/react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { COMPETITORS } from '../../data/market'

const topTier = COMPETITORS.filter(c => c.tier === 'top')
const midTier = COMPETITORS.filter(c => c.tier === 'mid')
const targetTier = COMPETITORS.filter(c => c.tier === 'target')

function fmtM(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

const allDataRows = []
let rowIdx = 0

function pushTier(label, dotColor, rows) {
  allDataRows.push({ type: 'tier', label, dotColor })
  rows.forEach(c => {
    allDataRows.push({ type: 'row', c, idx: rowIdx++ })
    // Insert Newport after Rainmaker (rank 5)
    if (c.rank === 5) {
      allDataRows.push({ type: 'newport' })
    }
  })
}
pushTier('National Leaders', '#C9A84C', topTier)
pushTier('Regional Mid-Market', '#1B7A8A', midTier)
pushTier("Newport's Competitive Tier", '#C9A84C', targetTier)

export default function CompetitionSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-20 pb-12 relative overflow-hidden">
      <BackgroundRing size={400} className="-top-32 -right-32" opacity={0.03} />

      {/* Header */}
      <div className="mb-5 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-3"
        >
          Competitive Analysis
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-1"
        >
          The Competitive Field
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[13px] text-zinc-600 max-w-2xl"
        >
          The top is locked — but Newport enters with more infrastructure than anyone in the $1-5M tier.
        </motion.p>
        <GoldLine width={60} className="mt-2" delay={0.25} />
      </div>

      {/* Table Card */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm overflow-hidden relative z-10"
      >
        <table className="w-full" style={{ borderCollapse: 'collapse' }}>
          <colgroup>
            <col style={{ width: '60px' }} />
            <col style={{ width: '40%' }} />
            <col style={{ width: '110px' }} />
            <col />
          </colgroup>

          {/* Header */}
          <thead>
            <tr style={{ backgroundColor: '#f4f4f5' }}>
              <th className="px-5 py-3 text-left font-body text-[11px] font-semibold text-zinc-600 uppercase tracking-wider border-b-2 border-zinc-200">
                #
              </th>
              <th className="px-4 py-3 text-left font-body text-[11px] font-semibold text-zinc-600 uppercase tracking-wider border-b-2 border-zinc-200">
                Company
              </th>
              <th className="px-4 py-3 text-right font-body text-[11px] font-semibold text-zinc-600 uppercase tracking-wider border-b-2 border-zinc-200">
                FL Awards
              </th>
              <th className="px-5 py-3 text-left font-body text-[11px] font-semibold text-zinc-600 uppercase tracking-wider border-b-2 border-zinc-200">
                Notes
              </th>
            </tr>
          </thead>

          <tbody>
            {allDataRows.map((row, i) => {
              const delay = 0.3 + i * 0.04

              // Tier section header
              if (row.type === 'tier') {
                return (
                  <motion.tr
                    key={`tier-${row.label}`}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay, duration: 0.3 }}
                  >
                    <td
                      colSpan={4}
                      className="px-5 pt-4 pb-1.5 border-b border-zinc-100"
                      style={{ backgroundColor: '#fafafa' }}
                    >
                      <span className="font-body text-[11px] font-bold uppercase tracking-[0.12em] text-zinc-700 flex items-center gap-2">
                        <span
                          className="w-2 h-2 rounded-full inline-block"
                          style={{ backgroundColor: row.dotColor }}
                        />
                        {row.label}
                      </span>
                    </td>
                  </motion.tr>
                )
              }

              // Newport callout row
              if (row.type === 'newport') {
                return (
                  <motion.tr
                    key="newport"
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay, duration: 0.3 }}
                    className="transition-colors duration-150"
                    style={{
                      backgroundColor: 'rgba(27,122,138,0.06)',
                      borderLeft: '3px solid #1B7A8A',
                    }}
                  >
                    <td className="px-5 py-3 border-b border-zinc-200">
                      <span
                        className="inline-flex items-center justify-center text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded"
                        style={{
                          backgroundColor: 'rgba(27,122,138,0.12)',
                          color: '#1B7A8A',
                        }}
                      >
                        You
                      </span>
                    </td>
                    <td className="px-4 py-3 border-b border-zinc-200">
                      <span className="font-body text-sm font-bold" style={{ color: '#1B7A8A' }}>
                        Newport Wholesalers
                      </span>
                    </td>
                    <td
                      className="px-4 py-3 text-right border-b border-zinc-200 font-body text-sm font-bold tabular-nums"
                      style={{ color: '#C9A84C' }}
                    >
                      $1-5M
                    </td>
                    <td className="px-5 py-3 border-b border-zinc-200 font-body text-xs text-zinc-700">
                      35-year track record · Cold chain · Plantation, FL
                    </td>
                  </motion.tr>
                )
              }

              // Regular competitor row
              const c = row.c
              const isEven = row.idx % 2 === 0
              const isTopTier = c.tier === 'top'

              return (
                <motion.tr
                  key={`row-${c.rank}`}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay, duration: 0.3 }}
                  className="hover:bg-zinc-100/60 transition-colors duration-150"
                  style={{
                    backgroundColor: isEven ? '#ffffff' : '#fafafa',
                  }}
                >
                  <td className="px-5 py-3 border-b border-zinc-100 font-body text-sm text-zinc-600 tabular-nums">
                    {c.rank}
                  </td>
                  <td className={`px-4 py-3 border-b border-zinc-100 font-body text-sm ${isTopTier ? 'font-semibold text-zinc-900' : 'font-semibold text-zinc-800'}`}>
                    {c.company}
                  </td>
                  <td
                    className="px-4 py-3 border-b border-zinc-100 text-right font-body text-sm font-semibold tabular-nums"
                    style={{ color: c.rank === 1 ? '#C9A84C' : '#27272a' }}
                  >
                    {fmtM(c.amount)}
                  </td>
                  <td className="px-5 py-3 border-b border-zinc-100 font-body text-xs text-zinc-700">
                    {c.notes}
                  </td>
                </motion.tr>
              )
            })}
          </tbody>
        </table>
      </motion.div>

      {/* Source */}
      <div className="flex items-center justify-between mt-3 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="font-body text-[11px] text-zinc-400"
        >
          USASpending API, FY2024 FL food contracts under $350K
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.4} />
      </div>
    </div>
  )
}
