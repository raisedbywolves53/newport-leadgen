import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { GraphicComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { TrendingUp, Shield, Lightbulb } from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { PRODUCT_TIERS } from '../../data/market'

echarts.use([PieChart, GraphicComponent, TooltipComponent, CanvasRenderer])

const confectionery = PRODUCT_TIERS.tier1[0]

export default function ConfectioneryGapSlide() {
  const chartRef = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      animation: false,
      tooltip: {
        trigger: 'item',
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: {
          color: '#fafafa',
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 12,
        },
        padding: [8, 12],
      },
      series: [
        {
          type: 'pie',
          radius: ['52%', '78%'],
          center: ['50%', '50%'],
          data: [
            {
              value: confectionery.soleSource,
              name: 'Sole Source',
              itemStyle: { color: '#C9A84C' },
            },
            {
              value: 100 - confectionery.soleSource,
              name: 'Competitive',
              itemStyle: { color: '#e5e5e5' },
            },
          ],
          label: { show: false },
          emphasis: { disabled: true },
        },
      ],
      graphic: [
        {
          type: 'text',
          left: 'center',
          top: 'center',
          style: {
            text: `${confectionery.soleSource}%`,
            fontSize: 32,
            fontWeight: 700,
            fontFamily: 'Inter, system-ui, sans-serif',
            fill: '#C9A84C',
            textAlign: 'center',
            textVerticalAlign: 'middle',
          },
        },
      ],
    })

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
  }, [])

  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      {/* ZONE 1: Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block text-xs font-medium uppercase tracking-widest text-zinc-400 mb-3"
        >
          Category Deep Dive
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          The Confectionery Gap
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          The lowest-competition category in government food — and Newport
          already has the suppliers.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — HORIZONTAL */}
      <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
        {/* $55M National Spend */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">National Spend</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-600">
                <Shield className="w-3 h-3" /> PSC 8925
              </span>
            </div>
            <span
              className="text-2xl font-semibold tabular-nums tracking-tight"
              style={{ color: '#C9A84C' }}
            >
              $55M
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              Only $412K captured in FL
            </div>
            <div className="text-zinc-500 text-xs">
              Confectionery &amp; Nuts — highest Newport fit
            </div>
          </div>
        </motion.div>

        {/* 45 National Awards */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.38 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">National Awards</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-600">
                FY2024
              </span>
            </div>
            <span
              className="text-2xl font-semibold tabular-nums tracking-tight"
              style={{ color: '#1B7A8A' }}
            >
              {confectionery.nationalAwards}
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              Contract actions nationally
            </div>
            <div className="text-zinc-500 text-xs">
              Low volume = low vendor awareness
            </div>
          </div>
        </motion.div>

        {/* 1.6 Avg Offers */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.46 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">
                Avg Offers per Award
              </span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-emerald-700">
                <TrendingUp className="w-3 h-3" /> LOW
              </span>
            </div>
            <span
              className="text-2xl font-semibold tabular-nums tracking-tight"
              style={{ color: '#1B7A8A' }}
            >
              {confectionery.avgOffers}
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              Minimal competition
            </div>
            <div className="text-zinc-500 text-xs">
              Most awards go to the only bidder
            </div>
          </div>
        </motion.div>
      </div>

      {/* ZONE 3: Chart card — FULL WIDTH donut */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col relative overflow-hidden mb-4 relative z-10"
        style={{ height: '240px' }}
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

        <div className="p-6 pb-0 pl-8">
          <h3 className="text-lg font-semibold text-zinc-950">
            Sole-Source Rate
          </h3>
          <p className="text-sm text-zinc-500 mt-1">
            PSC 8925 — Confectionery &amp; Nuts
          </p>
        </div>

        <div className="p-6 pt-4 pl-8 flex-1 min-h-0">
          <div ref={chartRef} className="w-full h-full" />
        </div>

        <div className="px-6 py-3 pl-8 border-t border-zinc-100 flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: '#C9A84C' }}
            />
            <span className="text-xs text-zinc-500">
              Sole Source ({confectionery.soleSource}%)
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: '#e5e5e5' }}
            />
            <span className="text-xs text-zinc-500">
              Competitive ({100 - confectionery.soleSource}%)
            </span>
          </div>
        </div>
      </motion.div>

      {/* ZONE 4: InsightCard */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.4 }}
        className="rounded-xl bg-amber-50/50 border border-amber-200/50 shadow-sm p-6 relative z-10"
      >
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-md bg-amber-100 flex items-center justify-center shrink-0">
            <Lightbulb
              className="w-4 h-4 text-amber-600"
              strokeWidth={1.5}
            />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-zinc-950 mb-1">
              Built-In Cost Advantage
            </h4>
            <p className="text-sm text-zinc-600 leading-relaxed">
              Newport's Segment E supplier pricing gives a built-in cost
              advantage. 93% of NAICS 424490 contracts at DoD are sole-source.
              Gov markup range: {confectionery.govMarkup}.
            </p>
          </div>
        </div>
      </motion.div>

      {/* ZONE 5: Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="text-[10px] text-zinc-300"
        >
          {confectionery.source}
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
