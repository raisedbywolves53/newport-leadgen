function formatSliderValue(value, format) {
  switch (format) {
    case 'percent':
      return (value * 100).toFixed(1) + '%'
    case 'percentSigned': {
      const pct = (value * 100).toFixed(0)
      return (value >= 0 ? '+' : '') + pct + '%'
    }
    case 'multiplier':
      return value.toFixed(1) + 'x'
    case 'currency':
      return '$' + Math.round(value).toLocaleString('en-US')
    default:
      return String(value)
  }
}

export default function Slider({ label, value, onChange, min, max, step, format, className = '' }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-[11px] font-medium text-zinc-500 w-20 shrink-0 truncate">{label}</span>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="flex-1 h-1.5 bg-zinc-200 rounded-full appearance-none cursor-pointer
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:h-3.5
          [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#1B7A8A] [&::-webkit-slider-thumb]:shadow-sm
          [&::-moz-range-thumb]:w-3.5 [&::-moz-range-thumb]:h-3.5 [&::-moz-range-thumb]:rounded-full
          [&::-moz-range-thumb]:bg-[#1B7A8A] [&::-moz-range-thumb]:border-0 [&::-moz-range-thumb]:shadow-sm"
      />
      <span className="text-[11px] font-semibold text-zinc-700 w-14 text-right tabular-nums shrink-0">
        {formatSliderValue(value, format)}
      </span>
    </div>
  )
}
