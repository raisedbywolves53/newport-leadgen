import { motion } from 'motion/react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine } from '../ui/DecorativeElements'
import { CONTRACT_EXAMPLES, CONTRACT_EXAMPLES_SOURCE } from '../../data/strategy'

const typeColors = {
  'Micro-purchase': { bg: '#f0fdfa', text: '#0d9488' },
  'Micro / Simplified': { bg: '#f0fdfa', text: '#0d9488' },
  'Simplified / SLED': { bg: '#fffbeb', text: '#d97706' },
  'B2B sub-supply': { bg: '#fffbeb', text: '#d97706' },
  'Disaster micro-purchase': { bg: '#f4f4f5', text: '#52525b' },
  'B2B (private)': { bg: '#fffbeb', text: '#d97706' },
}

const fitColors = {
  HIGHEST: '#C9A84C',
  HIGH: '#1B7A8A',
  MODERATE: '#71717a',
}

export default function ContractExamplesSlide() {
  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-5 pb-14">
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-1"
      >
        Market Evidence
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-1"
      >
        Real Contract Opportunities
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-sm text-zinc-600 mb-1"
      >
        Representative examples of what hits Florida procurement channels — these are the kinds of deals Newport would bid on.
      </motion.p>
      <GoldLine width={60} className="mb-4" delay={0.25} />

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="rounded-xl border border-zinc-200 shadow-sm overflow-hidden bg-white flex-1 min-h-0 flex flex-col"
      >
        {/* Table using real <table> for proper alignment */}
        <table style={{ width: '100%', borderCollapse: 'collapse', tableLayout: 'fixed' }}>
          <colgroup>
            <col style={{ width: '18%' }} />
            <col style={{ width: '30%' }} />
            <col style={{ width: '13%' }} />
            <col style={{ width: '14%' }} />
            <col style={{ width: '17%' }} />
            <col style={{ width: '8%' }} />
          </colgroup>
          <thead>
            <tr style={{ backgroundColor: '#f4f4f5', borderBottom: '2px solid #e4e4e7' }}>
              {['Agency', 'Description', 'Est. Value', 'Type', 'Competition', 'Fit'].map(h => (
                <th
                  key={h}
                  style={{
                    padding: '14px 16px',
                    textAlign: 'left',
                    fontSize: '12px',
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    color: '#52525b',
                    fontFamily: 'Inter, sans-serif',
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {CONTRACT_EXAMPLES.map((c, i) => {
              const tc = typeColors[c.type] || { bg: '#f4f4f5', text: '#52525b' }
              return (
                <motion.tr
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.35 + i * 0.05, duration: 0.25 }}
                  style={{
                    backgroundColor: i % 2 === 0 ? '#ffffff' : '#fafafa',
                    borderBottom: '1px solid #f4f4f5',
                  }}
                >
                  <td style={{ padding: '14px 16px', fontSize: '14px', fontWeight: 600, color: '#18181b', fontFamily: 'Inter, sans-serif', lineHeight: 1.3 }}>
                    {c.agency}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', color: '#52525b', fontFamily: 'Inter, sans-serif', lineHeight: 1.4 }}>
                    {c.description}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', fontWeight: 600, color: '#1B7A8A', fontFamily: 'JetBrains Mono, monospace' }}>
                    {c.estValue}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span
                      style={{
                        display: 'inline-block',
                        fontSize: '11px',
                        fontWeight: 600,
                        padding: '3px 8px',
                        borderRadius: '6px',
                        backgroundColor: tc.bg,
                        color: tc.text,
                        fontFamily: 'Inter, sans-serif',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {c.type}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', color: '#52525b', fontFamily: 'Inter, sans-serif', lineHeight: 1.3 }}>
                    {c.competition}
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '13px', fontWeight: 700, color: fitColors[c.fit] || '#71717a', fontFamily: 'Inter, sans-serif' }}>
                    {c.fit}
                  </td>
                </motion.tr>
              )
            })}
          </tbody>
        </table>
      </motion.div>

      <SourceCitation>{CONTRACT_EXAMPLES_SOURCE}</SourceCitation>
    </div>
  )
}
