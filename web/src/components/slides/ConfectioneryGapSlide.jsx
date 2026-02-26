import { motion } from 'motion/react'
import { Star, DollarSign, Package, Scale } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'

const statCards = [
  {
    icon: DollarSign,
    stat: '$55M',
    unit: 'National',
    headline: 'Massive, Underserved Market',
    detail: 'Only $412K currently captured in Florida — 99% of national spend is untouched by regional distributors.',
    accent: '#1B7A8A',
  },
  {
    icon: Package,
    stat: 'Segment E',
    unit: 'Core Line',
    headline: 'Existing Supplier Pricing',
    detail: "Newport already wholesales confectionery at scale. Same products, same logistics — different buyer.",
    accent: '#C9A84C',
  },
  {
    icon: Scale,
    stat: 'LPTA',
    unit: 'Method',
    headline: 'Lowest Price Wins',
    detail: 'Government uses Lowest Price Technically Acceptable — directly rewards wholesale volume pricing.',
    accent: '#1B7A8A',
  },
]

export default function ConfectioneryGapSlide() {
  return (
    <div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
      {/* Background decorative rings — matching slide 3 */}
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.03} />
      <BackgroundRing size={300} className="bottom-20 -right-20" opacity={0.025} />

      {/* Header */}
      <div className="mb-6 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-navy-800/40 mb-3"
        >
          Beachhead Category
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          Your First Win: Confectionery
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-navy-800/60 max-w-2xl"
        >
          The lowest-competition category in government food — and you already have the suppliers.
        </motion.p>
        <GoldLine width={60} className="mt-4" delay={0.25} />
      </div>

      {/* Bento grid: hero left (2 rows) + 3 cards stacked right */}
      <div className="grid grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr] gap-5 relative z-10" style={{ height: '460px' }}>

        {/* Hero card — "The Opportunity" */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="row-span-2 rounded-2xl bg-white p-10 shadow-[0_2px_8px_rgba(0,0,0,0.06)] border border-black/[0.04] flex flex-col justify-center relative overflow-hidden"
        >
          {/* Gold accent strip */}
          <div className="absolute left-0 top-8 bottom-8 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />

          <div className="pl-4">
            {/* Icon pill */}
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
              style={{ backgroundColor: '#C9A84C15' }}
            >
              <Star className="w-6 h-6" style={{ color: '#C9A84C' }} strokeWidth={1.8} />
            </div>

            {/* Hero stat */}
            <div className="flex items-baseline gap-3 mb-2">
              <span className="font-body text-7xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
                58%
              </span>
              <span className="font-body text-lg font-medium text-navy-800/35 uppercase tracking-wide">
                Sole Source
              </span>
            </div>

            {/* Headline */}
            <h3 className="font-body text-xl font-semibold text-navy-950 mt-4 mb-3">
              Virtually No Competition
            </h3>

            {/* Detail */}
            <p className="font-body text-[15px] leading-relaxed text-navy-800/70">
              PSC 8925 has the lowest vendor competition of any food category. Average 1.6 offers per award — most contracts go to the only bidder. Newport's Segment E pricing wins on day one.
            </p>

            {/* Footer */}
            <div className="flex items-center gap-2 mt-5 pt-5 border-t border-black/[0.06]">
              <span className="font-body text-xs font-medium text-navy-800/45">PSC 8925</span>
              <span className="text-navy-800/25">·</span>
              <span className="font-body text-xs font-medium text-navy-800/45">Confectionery & Nuts</span>
            </div>
          </div>
        </motion.div>

        {/* 3 StatCards — right column, stacked */}
        {statCards.map((card, i) => {
          const Icon = card.icon
          return (
            <motion.div
              key={card.headline}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.4 + i * 0.1 }}
              className="rounded-2xl bg-white/70 backdrop-blur-sm p-6 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] flex flex-col justify-center"
            >
              <div className="flex items-start gap-4">
                <div
                  className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                  style={{ backgroundColor: `${card.accent}15` }}
                >
                  <Icon className="w-5 h-5" style={{ color: card.accent }} strokeWidth={1.5} />
                </div>
                <div className="flex-1">
                  <div className="flex items-baseline gap-2 mb-1">
                    <span
                      className="font-body text-3xl font-bold tracking-tight leading-none"
                      style={{ color: card.accent }}
                    >
                      {card.stat}
                    </span>
                    <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide">
                      {card.unit}
                    </span>
                  </div>
                  <h3 className="font-body text-base font-semibold text-navy-950 mb-1.5">
                    {card.headline}
                  </h3>
                  <p className="font-body text-sm leading-relaxed text-navy-800/65">
                    {card.detail}
                  </p>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Source + compass star */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="text-[10px] text-navy-800/35"
        >
          FPDS FY2024, PSC 8925 | USASpending FL awards | FAR 15.101-2 (LPTA)
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
