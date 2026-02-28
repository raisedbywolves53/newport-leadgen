import { useEffect, useRef } from 'react'
import { animate } from 'motion'

function formatValue(value, format) {
  switch (format) {
    case 'currency':
      return '$' + Math.round(value).toLocaleString('en-US')
    case 'compact': {
      const abs = Math.abs(value)
      if (abs >= 1_000_000) return (value < 0 ? '-' : '') + '$' + (abs / 1_000_000).toFixed(1) + 'M'
      if (abs >= 1_000) return (value < 0 ? '-' : '') + '$' + Math.round(abs / 1_000) + 'K'
      return '$' + Math.round(value).toLocaleString('en-US')
    }
    case 'percent':
      return Math.round(value) + '%'
    case 'number':
      return Math.round(value).toLocaleString('en-US')
    default:
      return String(Math.round(value))
  }
}

export default function AnimatedNumber({ value, format = 'number', duration = 0.6, className = '', style }) {
  const ref = useRef(null)
  const prevValue = useRef(0)

  useEffect(() => {
    if (!ref.current) return
    const from = prevValue.current
    const to = value

    const controls = animate(from, to, {
      duration,
      ease: [0.25, 0.1, 0.25, 1],
      onUpdate(v) {
        if (ref.current) {
          ref.current.textContent = formatValue(v, format)
        }
      },
    })

    prevValue.current = to
    return () => controls.stop()
  }, [value, format, duration])

  return (
    <span ref={ref} className={className} style={style}>
      {formatValue(value, format)}
    </span>
  )
}
