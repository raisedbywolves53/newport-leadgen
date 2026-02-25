import { SLIDES } from '../../data/slides'

const sectionColors = {
  opportunity: 'bg-teal-500',
  strategy: 'bg-amber-500',
  economics: 'bg-teal-400',
  execution: 'bg-amber-400',
}

export default function Navigation({ currentSlide, goTo }) {
  return (
    <nav className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-navy-900/80 backdrop-blur-md border border-navy-700/50">
      {SLIDES.map((slide, i) => {
        const isActive = i === currentSlide
        const colorClass = slide.section ? sectionColors[slide.section] : 'bg-slate-400'

        return (
          <button
            key={slide.id}
            onClick={() => goTo(i)}
            className={`
              relative rounded-full transition-all duration-300 cursor-pointer
              ${slide.isDivider ? 'mx-1' : ''}
              ${isActive
                ? `w-8 h-2.5 ${colorClass}`
                : `w-2 h-2 bg-slate-500/50 hover:bg-slate-400/70`
              }
            `}
            aria-label={`Go to slide: ${slide.label}`}
            title={slide.label}
          />
        )
      })}

      <span className="ml-3 text-xs font-body text-slate-400 tabular-nums">
        {currentSlide + 1}/{SLIDES.length}
      </span>
    </nav>
  )
}
