import { useState, useEffect } from 'react'

export function useCountUp(target, duration = 1500, delay = 0) {
  const [value, setValue] = useState(0)

  useEffect(() => {
    let rafId
    const timeoutId = setTimeout(() => {
      const start = performance.now()
      const animate = (now) => {
        const elapsed = now - start
        const progress = Math.min(elapsed / duration, 1)
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3)
        setValue(Math.round(eased * target))
        if (progress < 1) rafId = requestAnimationFrame(animate)
      }
      rafId = requestAnimationFrame(animate)
    }, delay)

    return () => {
      clearTimeout(timeoutId)
      if (rafId) cancelAnimationFrame(rafId)
    }
  }, [target, duration, delay])

  return value
}
