import { motion } from 'motion/react'
import { SCENARIO_PARAMS } from '../../data/financials'

const SCENARIOS = ['conservative', 'moderate', 'aggressive']

export default function ScenarioToggle({ active, onChange, className = '' }) {
  return (
    <div className={`inline-flex rounded-lg bg-zinc-100 p-0.5 ${className}`}>
      {SCENARIOS.map((key) => {
        const s = SCENARIO_PARAMS[key]
        const isActive = active === key
        return (
          <button
            key={key}
            onClick={() => onChange(key)}
            className="relative px-3 py-1.5 rounded-md text-xs font-medium transition-colors cursor-pointer"
            style={{ color: isActive ? '#fff' : '#71717a' }}
          >
            {isActive && (
              <motion.div
                layoutId="scenario-bg"
                className="absolute inset-0 rounded-md"
                style={{ backgroundColor: s.color }}
                transition={{ type: 'spring', bounce: 0.15, duration: 0.4 }}
              />
            )}
            <span className="relative z-10">{s.label}</span>
          </button>
        )
      })}
    </div>
  )
}
