import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { Star, Shield, TrendingUp } from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { PRODUCT_TIERS } from '../../data/market'

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])

function fmtM(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

// All bars sorted descending by FL spend — tier determines color
const BAR_DATA = [
  ...PRODUCT_TIERS.tier1.map(p => ({ ...p, tier: 1 })),
  ...PRODUCT_TIERS.tier2.map(p => ({ ...p, tier: 2 })),
  ...PRODUCT_TIERS.avoid.map(p => ({
    psc: p.psc,
    name: p.name,
    flSpend: p.name === 'Meat, Poultry, Fish' ? 800000 : p.name === 'MREs/Composites' ? 500000 : 300000,
    soleSource: 0,
    advantage: p.reason,
    govMarkup: 'N/A',
    tier: 3,
  })),
].sort((a, b) => b.flSpend - a.flSpend)

const REVERSED = [...BAR_DATA].reverse()

function tierColor(tier) {
  if (tier === 1) return 'rgba(201,168,76,0.80)'
  if (tier === 2) return 'rgba(27,122,138,0.70)'
  return 'rgba(161,161,170,0.25)'
}

const confectionery = PRODUCT_TIERS.tier1[0]

const STAT_CARDS = [
  {
    label: 'Confectionery & Nuts',
    value: fmtM(confectionery.nationalSpend),
    accent: '#C9A84C',
    badge: { icon: Star, text: 'Highest Fit', variant: 'text-amber-700' },
    footerHighlight: 'National spend, PSC 8925',
    footerDescription: "Newport's #1 product match",
  },
  {
    label: 'PSC 8925 Sole-Source',
    value: `${confectionery.soleSource}%`,
    accent: '#C9A84C',
    badge: { icon: TrendingUp, text: 'No competition', variant: 'text-emerald-700' },
    footerHighlight: 'Most awards are sole-source',
    footerDescription: 'Lowest competition of all categories',
  },
  {
    label: 'Evaluation Method',
    value: 'LPTA',
    accent: '#1B7A8A',
    badge: { icon: Shield, text: 'Price wins', variant: 'text-zinc-600' },
    footerHighlight: 'Lowest Price Technically Acceptable',
    footerDescription: "Newport's wholesale pricing advantage",
  },
]

export default function ProductMatrixSlide() {
  const chartRef = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      animation: false,
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 },
        padding: [8, 12],
        borderRadius: 8,
        extraCssText: 'box-shadow: 0 8px 24px rgba(0,0,0,0.25);',
        formatter: (params) => {
          const p = params[0]
          const d = REVERSED[p.dataIndex]
          if (d.tier === 3) {
            return `<b>${d.name}</b><br/><span style="color:#a1a1aa">${d.advantage}</span>`
          }
          return [
            `<b>${d.name}</b>`,
            `FL Spend: <b>${fmtM(d.flSpend)}</b>`,
            d.soleSource ? `Sole-source: <b>${d.soleSource}%</b>` : '',
            d.govMarkup ? `Markup range: <b>${d.govMarkup}</b>` : '',
            d.advantage ? `<span style="color:#C9A84C">${d.advantage}</span>` : '',
          ].filter(Boolean).join('<br/>')
        },
      },
      grid: { left: 16, right: 90, top: 16, bottom: 16, containLabel: true },
      xAxis: { type: 'value', show: false, splitLine: { show: false } },
      yAxis: {
        type: 'category',
        data: REVERSED.map(d => d.name),
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: true, lineStyle: { color: '#e5e5e5', opacity: 0.3, type: 'dashed' } },
        axisLabel: {
          fontSize: 12,
          fontFamily: 'Inter, system-ui, sans-serif',
          color: (value) => {
            const item = BAR_DATA.find(d => d.name === value)
            return item && item.tier === 3 ? '#a1a1aa' : '#18181b'
          },
        },
      },
      series: [{
        type: 'bar',
        data: REVERSED.map(d => ({
          value: d.flSpend,
          itemStyle: { color: tierColor(d.tier), borderRadius: [0, 4, 4, 0] },
          label: { color: d.tier === 1 ? '#C9A84C' : d.tier === 2 ? '#1B7A8A' : 'transparent' },
        })),
        barWidth: 18,
        label: {
          show: true, position: 'right', fontSize: 11,
          fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 600,
          formatter: (params) => {
            const d = REVERSED[params.dataIndex]
            return d.tier !== 3 ? fmtM(params.value) : ''
          },
        },
        emphasis: { itemStyle: { opacity: 1 } },
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
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      {/* ZONE 1: Header */}
      <div className="mb-4 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block text-xs font-medium uppercase tracking-widest text-zinc-400 mb-3"
        >
          Product Categories
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          Where Newport Has Pricing Power
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          Prioritized by FL demand, competition density, and Newport's wholesale
          advantage.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — ABOVE chart */}
      <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
        {STAT_CARDS.map((stat, i) => {
          const BadgeIcon = stat.badge.icon
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ y: -2 }}
              transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-6 py-6 cursor-default"
            >
              <div className="px-6 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-zinc-500">{stat.label}</span>
                  <span
                    className={`inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 ${stat.badge.variant}`}
                  >
                    {BadgeIcon && <BadgeIcon className="w-3 h-3" />}
                    {stat.badge.text}
                  </span>
                </div>
                <span
                  className="text-2xl font-semibold tabular-nums tracking-tight"
                  style={{ color: stat.accent }}
                >
                  {stat.value}
                </span>
              </div>
              <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
                <div className="flex items-center gap-2 font-medium text-zinc-900">
                  {stat.footerHighlight}
                </div>
                <div className="text-zinc-500 text-xs">
                  {stat.footerDescription}
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* ZONE 3: ChartCard — FULL WIDTH, BELOW stats */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out relative overflow-hidden z-10"
        style={{ height: '300px' }}
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

        <div className="w-full h-full flex flex-col">
          {/* CardHeader */}
          <div className="p-6 pb-0 pl-8">
            <h3 className="text-lg font-semibold text-zinc-950">
              FL Spend by Product Category
            </h3>
            <p className="text-sm text-zinc-500 mt-1">
              Gold = Tier 1, Teal = Tier 2, Gray = Avoid
            </p>
          </div>

          {/* CardContent: chart */}
          <div className="p-6 pt-4 pl-8 flex-1 min-h-0">
            <div ref={chartRef} className="w-full h-full" />
          </div>

          {/* CardFooter: legend */}
          <div className="px-6 py-3 pl-8 border-t border-zinc-100 flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(201,168,76,0.80)' }} />
              <span className="text-xs text-zinc-500">Tier 1 — Highest</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(27,122,138,0.70)' }} />
              <span className="text-xs text-zinc-500">Tier 2 — Growth</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(161,161,170,0.25)' }} />
              <span className="text-xs text-zinc-500">Avoid</span>
            </div>
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
          FPDS FY2024 by PSC code | USASpending FL awards | FAR 15.101-2 (LPTA evaluation)
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
