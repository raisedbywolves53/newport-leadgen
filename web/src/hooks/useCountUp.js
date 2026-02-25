import { useState, useEffect, useRef } from 'react'

export function useCountUp(target, duration = 1500, delay = 0) {
  const [value, setValue] = useState(0)
  const hasAnimated = useRef(false)

  useEffect(() => {
    if (hasAnimated.current) return
    hasAnimated.current = true

    const start = performance.now()
    const timer = setTimeout(() => {
      const animate = (now) => {
        const elapsed = now - start - delay
        if (elapsed < 0) {
          requestAnimationFrame(animate)
          return
        }
        const progress = Math.min(elapsed / duration, 1)
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3)
        setValue(Math.round(eased * target))
        if (progress < 1) requestAnimationFrame(animate)
      }
      requestAnimationFrame(animate)
    }, delay)

    return () => clearTimeout(timer)
  }, [target, duration, delay])

  return value
}
