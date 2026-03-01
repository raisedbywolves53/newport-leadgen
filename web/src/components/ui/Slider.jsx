function formatSliderValue(value, format) {
  switch (format) {
    case 'percent':
      return (value * 100).toFixed(1) + '%'
    case 'currency': {
      const abs = Math.abs(value)
      if (abs >= 1000) return '$' + (abs / 1000).toFixed(0) + 'K'
      return '$' + abs.toLocaleString('en-US')
    }
    default:
      return String(value)
  }
}

export default function Slider({ label, value, onChange, min, max, step, format, className = '' }) {
  const pct = ((value - min) / (max - min)) * 100

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-zinc-500">{label}</span>
        <span className="text-xs font-semibold text-zinc-800 tabular-nums">
          {formatSliderValue(value, format)}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-1.5 rounded-full appearance-none cursor-pointer
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3.5 [&::-webkit-slider-thumb]:h-3.5
          [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#1B7A8A]
          [&::-webkit-slider-thumb]:border-2 [&::-webkit-slider-thumb]:border-white
          [&::-webkit-slider-thumb]:shadow-sm [&::-webkit-slider-thumb]:cursor-pointer
          [&::-moz-range-thumb]:w-3.5 [&::-moz-range-thumb]:h-3.5 [&::-moz-range-thumb]:rounded-full
          [&::-moz-range-thumb]:bg-[#1B7A8A] [&::-moz-range-thumb]:border-2 [&::-moz-range-thumb]:border-white
          [&::-moz-range-thumb]:shadow-sm [&::-moz-range-thumb]:cursor-pointer"
        style={{
          background: `linear-gradient(to right, #1B7A8A ${pct}%, #e4e4e7 ${pct}%)`,
        }}
      />
    </div>
  )
}
