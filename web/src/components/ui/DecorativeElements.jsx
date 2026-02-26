import { motion } from 'motion/react'

/**
 * Animated gold accent line — editorial separator.
 * Use between subtitle and content to add polish.
 */
export function GoldLine({ width = 60, className = '', delay = 0.15 }) {
  return (
    <motion.div
      initial={{ width: 0 }}
      animate={{ width }}
      transition={{ duration: 0.8, delay }}
      className={`h-px ${className}`}
      style={{ backgroundColor: '#C9A84C' }}
    />
  )
}

/**
 * Decorative 4-pointed compass star — subtle brand mark.
 * Used as a finishing touch on editorial slides.
 */
export function CompassStar({ size = 20, color = '#C9A84C', opacity = 0.25, className = '', delay = 1.2 }) {
  return (
    <motion.svg
      initial={{ opacity: 0, rotate: -30 }}
      animate={{ opacity, rotate: 0 }}
      transition={{ duration: 0.8, delay }}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      className={className}
    >
      <path
        d="M12 0L13.2 9.6L12 8.4L10.8 9.6L12 0Z"
        fill={color}
      />
      <path
        d="M24 12L14.4 13.2L15.6 12L14.4 10.8L24 12Z"
        fill={color}
      />
      <path
        d="M12 24L10.8 14.4L12 15.6L13.2 14.4L12 24Z"
        fill={color}
      />
      <path
        d="M0 12L9.6 10.8L8.4 12L9.6 13.2L0 12Z"
        fill={color}
      />
      <circle cx="12" cy="12" r="1.2" fill={color} />
    </motion.svg>
  )
}

/**
 * Oversized hero stat — the visual anchor for data slides.
 * Pulls the key number out of cards and makes it the centerpiece.
 */
export function HeroStat({ value, unit, detail, delay = 0.25, accentColor = '#C9A84C', className = '' }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className={`flex items-baseline gap-3 ${className}`}
    >
      <span
        className="font-body text-6xl md:text-7xl font-bold tracking-tighter leading-none"
        style={{ color: accentColor }}
      >
        {value}
      </span>
      <div className="flex flex-col">
        <span className="font-body text-sm font-semibold text-navy-950">
          {unit}
        </span>
        {detail && (
          <span className="font-body text-xs text-navy-800/50 mt-0.5">
            {detail}
          </span>
        )}
      </div>
    </motion.div>
  )
}

/**
 * Subtle background ring — geometric decorative element.
 * Adds depth to otherwise flat warm-gray backgrounds.
 */
export function BackgroundRing({ size = 400, color = '#C9A84C', opacity = 0.04, className = '' }) {
  return (
    <div
      className={`absolute pointer-events-none ${className}`}
      style={{
        width: size,
        height: size,
        border: `1px solid ${color}`,
        borderRadius: '50%',
        opacity,
      }}
    />
  )
}
