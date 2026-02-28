import { motion } from 'motion/react'

const ROUTES = [
  { key: 'free', label: 'Free Route', cost: '$0/yr', color: '#71717a' },
  { key: 'paid', label: 'Paid Route', cost: '$13K/yr', color: '#1B7A8A' },
]

export default function RouteToggle({ active, onChange, className = '' }) {
  return (
    <div className={`inline-flex rounded-lg bg-zinc-100 p-0.5 ${className}`}>
      {ROUTES.map((route) => (
        <button
          key={route.key}
          onClick={() => onChange(route.key)}
          className="relative px-3 py-1.5 rounded-md text-xs font-medium transition-colors cursor-pointer"
          style={{ color: active === route.key ? '#fff' : '#71717a' }}
        >
          {active === route.key && (
            <motion.div
              layoutId="route-bg"
              className="absolute inset-0 rounded-md"
              style={{ backgroundColor: route.color }}
              transition={{ type: 'spring', bounce: 0.15, duration: 0.4 }}
            />
          )}
          <span className="relative z-10 flex flex-col items-center gap-0.5">
            <span>{route.label}</span>
            <span className="text-[10px] opacity-75">{route.cost}</span>
          </span>
        </button>
      ))}
    </div>
  )
}
