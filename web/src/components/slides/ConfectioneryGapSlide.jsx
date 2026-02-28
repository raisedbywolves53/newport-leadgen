import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { GraphicComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { Star, Award, Users } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
import { PRODUCT_TIERS } from '../../data/market'

echarts.use([PieChart, GraphicComponent, TooltipComponent, CanvasRenderer])

const confectionery = PRODUCT_TIERS.tier1[0]

const statTiles = [
  {
    icon: Star,
    label: 'National Spend',
    stat: `$${(confectionery.nationalSpend / 1e6).toFixed(0)}M`,
    detail: `Only $${(confectionery.flSpend / 1e3).toFixed(0)}K captured in Florida`,
    accent: '#C9A84C',
  },
  {
    icon: Award,
    label: 'National Awards',
    stat: `${confectionery.nationalAwards}`,
    detail: 'PSC 8925 — Confectionery & Nuts',
    accent: '#1B7A8A',
  },
  {
    icon: Users,
    label: 'Avg Offers per Award',
    stat: `${confectionery.avgOffers}`,
    detail: 'Minimal competition',
    accent: '#1B7A8A',
  },
]

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
        borderRadius: 8,
        textStyle: { color: '#fff', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 },
      },
      graphic: [{
        type: 'group',
        left: 'center',
        top: 'center',
        children: [
          {
            type: 'text',
            style: {
              text: `${confectionery.soleSource}%`,
              textAlign: 'center',
              fill: '#C9A84C',
              fontSize: 40,
              fontWeight: 600,
              fontFamily: 'Inter, system-ui, sans-serif',
            },
            top: -8,
          },
          {
            type: 'text',
            style: {
              text: 'Sole Source',
              textAlign: 'center',
              fill: '#71717a',
              fontSize: 13,
              fontFamily: 'Inter, system-ui, sans-serif',
            },
            top: 34,
          },
        ],
      }],
      series: [{
        type: 'pie',
        radius: ['48%', '76%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: false,
        label: { show: false },
        labelLine: { show: false },
        emphasis: { scale: false },
        data: [
          { value: confectionery.soleSource, name: 'Sole Source', itemStyle: { color: '#C9A84C' } },
          { value: 100 - confectionery.soleSource, name: 'Competitive', itemStyle: { color: '#e5e5e5' } },
        ],
      }],
    })

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
  }, [])

  return (
    <div className="w-full h-full flex flex-col justify-center px-20 pb-16 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.03} />
      <BackgroundRing size={300} className="bottom-20 -right-20" opacity={0.025} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-3"
        >
          Category Deep Dive
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          The Confectionery Gap
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-zinc-600 max-w-2xl"
        >
          The lowest-competition category in government food — and you already have the suppliers.
        </motion.p>
        <GoldLine width={60} className="mt-4" delay={0.25} />
      </div>

      {/* Dashboard: Chart + Stat Tiles */}
      <div className="grid grid-cols-[3fr_2fr] gap-4 relative z-10" style={{ height: '380px' }}>

        {/* Left: Hero chart card */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.3 }}
          className="rounded-xl bg-white p-5 shadow-sm border border-zinc-200 relative overflow-hidden"
        >
          {/* Gold accent strip */}
          <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />

          <div className="flex flex-col h-full">
            <div className="flex-1 min-h-0">
              <div ref={chartRef} className="w-full h-full" />
            </div>
            {/* Compact legend */}
            <div className="flex items-center gap-5 pt-2 border-t border-zinc-100">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#C9A84C' }} />
                <span className="font-body text-[13px] text-zinc-500">Sole Source</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#e5e5e5' }} />
                <span className="font-body text-[13px] text-zinc-500">Competitive</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Right: 3 stacked stat tiles */}
        <div className="flex flex-col gap-4">
          {statTiles.map((tile, i) => {
            const Icon = tile.icon
            return (
              <motion.div
                key={tile.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.4 + i * 0.1 }}
                className="rounded-xl bg-white p-5 shadow-sm border border-zinc-200 flex-1 flex flex-col justify-center"
              >
                <div className="flex items-start gap-3">
                  <div
                    className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                    style={{ backgroundColor: `${tile.accent}15` }}
                  >
                    <Icon className="w-5 h-5" style={{ color: tile.accent }} strokeWidth={1.5} />
                  </div>
                  <div className="flex-1">
                    <span className="font-body text-xs font-semibold text-zinc-500">{tile.label}</span>
                    <span
                      className="font-body text-2xl font-semibold tracking-tight leading-none block mt-1"
                      style={{ color: tile.accent }}
                    >
                      {tile.stat}
                    </span>
                    <p className="font-body text-xs text-zinc-500 mt-1.5">
                      {tile.detail}
                    </p>
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Source + compass star */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
          className="text-[10px] text-zinc-300"
        >
          {confectionery.source}
        </motion.p>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
