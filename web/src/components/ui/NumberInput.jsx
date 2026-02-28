import { useState, useEffect, useRef } from 'react'

function toDisplay(value, format) {
  switch (format) {
    case 'percent':
      return (value * 100).toFixed(1)
    case 'multiplier':
      return value.toFixed(1)
    case 'percentSigned':
      return (value >= 0 ? '+' : '') + (value * 100).toFixed(0)
    case 'currency':
      return Math.round(value).toLocaleString('en-US')
    default:
      return String(value)
  }
}

function suffix(format) {
  switch (format) {
    case 'percent':
    case 'percentSigned':
      return '%'
    case 'multiplier':
      return 'x'
    case 'currency':
      return ''
    default:
      return ''
  }
}

function prefix(format) {
  return format === 'currency' ? '$' : ''
}

function parseInput(raw, format) {
  const cleaned = raw.replace(/[$,%x+\s]/g, '')
  const num = parseFloat(cleaned)
  if (isNaN(num)) return null
  // percent and percentSigned are displayed as whole numbers but stored as decimals
  if (format === 'percent' || format === 'percentSigned') return num / 100
  return num
}

export default function NumberInput({ label, value, onChange, min, max, step, format, className = '' }) {
  const [localValue, setLocalValue] = useState(() => toDisplay(value, format))
  const [focused, setFocused] = useState(false)
  const inputRef = useRef(null)

  // Sync external value changes when not focused
  useEffect(() => {
    if (!focused) {
      setLocalValue(toDisplay(value, format))
    }
  }, [value, format, focused])

  const commit = () => {
    const parsed = parseInput(localValue, format)
    if (parsed === null) {
      // Reset to current value
      setLocalValue(toDisplay(value, format))
      return
    }
    const clamped = Math.min(max, Math.max(min, parsed))
    // Snap to step
    const snapped = Math.round(clamped / step) * step
    onChange(snapped)
    setLocalValue(toDisplay(snapped, format))
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      commit()
      inputRef.current?.blur()
    }
    if (e.key === 'Escape') {
      setLocalValue(toDisplay(value, format))
      inputRef.current?.blur()
    }
  }

  const pfx = prefix(format)
  const sfx = suffix(format)

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-[13px] font-medium text-zinc-500 w-[84px] shrink-0 truncate">
        {label}
      </span>
      <div className="flex items-center rounded-md border border-zinc-200 bg-zinc-50 focus-within:border-[#1B7A8A] focus-within:ring-1 focus-within:ring-[#1B7A8A]/30 transition-colors">
        {pfx && (
          <span className="text-[13px] text-zinc-400 pl-2 select-none">{pfx}</span>
        )}
        <input
          ref={inputRef}
          type="text"
          inputMode="decimal"
          value={localValue}
          onChange={(e) => setLocalValue(e.target.value)}
          onFocus={(e) => {
            setFocused(true)
            e.target.select()
          }}
          onBlur={() => {
            setFocused(false)
            commit()
          }}
          onKeyDown={handleKeyDown}
          className="w-[64px] px-1.5 py-1 text-[13px] font-semibold text-zinc-700 tabular-nums bg-transparent outline-none text-right
            [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
        />
        {sfx && (
          <span className="text-[13px] text-zinc-400 pr-2 select-none">{sfx}</span>
        )}
      </div>
    </div>
  )
}
