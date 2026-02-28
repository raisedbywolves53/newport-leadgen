import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { TrendingUp, Repeat, Target, DollarSign, ArrowRight } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

// Portfolio data
const data = {
  labels: ['Q1-Q2\nY1', 'Q3-Q4\nY1', 'Y2', 'Y3', 'Y4', 'Y5'],
  micro:      [6,  4,  3,  1,  0,  0],
  simplified: [1,  3,  8, 14, 18, 20],
  larger:     [0,  1,  3,  7, 14, 22],
  renewed:    [0,  2,  7, 15, 24, 36],
}

const totals = data.labels.map((_, i) =>
  data.micro[i] + data.simplified[i] + data.larger[i] + data.renewed[i]
)

const recurringValue = ['$45K', '$120K', '$480K', '$1.2M', '$2.8M', '$4.5M']

const kpis = [
  {
    icon: Target,
    label: 'Y5 Active Contracts',
    value: '78',
    change: '+670%',
    sub: 'from 7 in Year 1',
    accent: '#C9A84C',
  },
  {
    icon: DollarSign,
    label: 'Recurring Annual Value',
    value: '$4.5M',
    change: '+3,650%',
    sub: 'projected Year 5',
    accent: '#1B7A8A',
  },
  {
    icon: Repeat,
    label: 'Renewal Rate',
    value: '70%',
    change: 'steady',
    sub: 'federal incumbent avg',
    accent: '#1B7A8A',
  },
  {
    icon: TrendingUp,
    label: 'Avg Contract Size',
    value: '$58K',
    change: '+830%',
    sub: 'from $7K micro starts',
    accent: '#C9A84C',
  },
]

// The shift narrative
const SHIFT_PHASES = [
  { label: 'Entry', detail: 'Micro-purchases (<$15K)', color: '#d4d4d8' },
  { label: 'Scale', detail: 'Simplified acquisitions ($15-350K)', color: '#1B7A8A' },
  { label: 'Expand', detail: 'Larger contracts (>$100K)', color: '#239BAD' },
  { label: 'Retain', detail: '70% renewal as incumbent', color: '#C9A84C' },
]

export default function PortfolioEvolutionSlide() {
  const chartRef = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderRadius: 8,
        textStyle: { color: '#fafafa', fontSize: 12, fontFamily: 'Inter' },
        formatter: (params) => {
          const period = params[0].axisValue.replace('\n', ' ')
          let html = `<div style="font-weight:600;margin-bottom:6px">${period}</div>`
          let total = 0
          params.forEach(p => {
            total += p.value
            html += `<div style="display:flex;justify-content:space-between;gap:16px;margin:2px 0">
              <span>${p.marker} ${p.seriesName}</span>
              <span style="font-weight:600">${p.value}</span>
            </div>`
          })
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:4px;display:flex;justify-content:space-between;gap:16px">
            <span style="font-weight:600">Total</span>
            <span style="font-weight:700;color:#C9A84C">${total}</span>
          </div>`
          const idx = data.labels.indexOf(params[0].axisValue)
          if (idx >= 0) {
            html += `<div style="display:flex;justify-content:space-between;gap:16px;margin-top:2px">
              <span>Est. Annual Value</span>
              <span style="font-weight:600;color:#1B7A8A">${recurringValue[idx]}</span>
            </div>`
          }
          return html
        },
      },
      legend: {
        bottom: 0,
        textStyle: { color: '#71717a', fontSize: 12, fontFamily: 'Inter' },
        itemWidth: 12,
        itemHeight: 12,
        itemGap: 24,
      },
      grid: { left: 48, right: 16, top: 12, bottom: 44 },
      xAxis: {
        type: 'category',
        data: data.labels,
        axisLabel: { color: '#71717a', fontFamily: 'Inter', fontSize: 12 },
        axisLine: { lineStyle: { color: '#e4e4e7' } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#a1a1aa', fontFamily: 'Inter', fontSize: 12 },
        splitLine: { lineStyle: { color: '#f4f4f5' } },
        axisLine: { show: false },
      },
      series: [
        {
          name: 'Micro (<$15K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.micro,
          itemStyle: { color: '#d4d4d8' },
          barWidth: 64,
          animationDuration: 800,
          animationDelay: (i) => i * 100,
        },
        {
          name: 'Simplified ($15-350K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.simplified,
          itemStyle: { color: '#1B7A8A' },
          barWidth: 64,
          animationDuration: 800,
          animationDelay: (i) => i * 100 + 200,
        },
        {
          name: 'Larger (>$100K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.larger,
          itemStyle: { color: '#239BAD' },
          barWidth: 64,
          animationDuration: 800,
          animationDelay: (i) => i * 100 + 400,
        },
        {
          name: 'Renewed (70%)',
          type: 'bar',
          stack: 'portfolio',
          data: data.renewed,
          itemStyle: { color: '#C9A84C', borderRadius: [4, 4, 0, 0] },
          barWidth: 64,
          label: {
            show: true,
            position: 'top',
            formatter: (params) => totals[params.dataIndex],
            color: '#3f3f46',
            fontSize: 14,
            fontFamily: 'Inter',
            fontWeight: 700,
          },
          animationDuration: 800,
          animationDelay: (i) => i * 100 + 600,
        },
      ],
    })

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    return () => { window.removeEventListener('resize', handleResize); chart.dispose() }
  }, [])

  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-2 pb-14 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.02} />

      {/* Compact header */}
      <div className="mb-2 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5"
        >
          5-Year Growth Model
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          Portfolio Evolution
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600"
        >
          Micro-purchases are the price of admission — not the destination.
        </motion.p>
        <GoldLine width={60} className="mt-1" delay={0.25} />
      </div>

      {/* KPI Cards Row — compact */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="grid grid-cols-4 gap-2.5 mb-2 relative z-10"
      >
        {kpis.map((kpi) => {
          const Icon = kpi.icon
          return (
            <div
              key={kpi.label}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm px-4 py-3 relative overflow-hidden"
            >
              <div className="flex items-start justify-between mb-1">
                <span className="font-body text-[10px] font-medium text-zinc-500 uppercase tracking-wider">
                  {kpi.label}
                </span>
                <span
                  className="text-[10px] font-semibold px-1.5 py-0.5 rounded flex items-center gap-0.5"
                  style={{
                    backgroundColor: `${kpi.accent}12`,
                    color: kpi.accent,
                  }}
                >
                  <TrendingUp className="w-3 h-3" />
                  {kpi.change}
                </span>
              </div>
              <div className="flex items-end justify-between">
                <span
                  className="font-body text-2xl font-bold tracking-tight leading-none"
                  style={{ color: kpi.accent }}
                >
                  {kpi.value}
                </span>
                <Icon
                  className="w-5 h-5 opacity-15"
                  style={{ color: kpi.accent }}
                  strokeWidth={1.5}
                />
              </div>
              <span className="font-body text-[10px] text-zinc-500 block mt-1">
                {kpi.sub}
              </span>
            </div>
          )
        })}
      </motion.div>

      {/* Main content: Chart (left ~70%) + Shift narrative (right ~30%) */}
      <div className="flex gap-2.5 flex-1 min-h-0 relative z-10">
        {/* Chart area */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm p-3 flex-1 min-h-0 flex flex-col"
        >
          <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-1 block">
            Active Contracts by Type
          </span>
          <div ref={chartRef} className="w-full flex-1 min-h-0" />
        </motion.div>

        {/* Shift narrative panel — wider with bigger text */}
        <motion.div
          initial={{ opacity: 0, x: 12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="w-[280px] shrink-0 rounded-xl bg-white border border-zinc-200 shadow-sm p-5 flex flex-col"
        >
          <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-3 block">
            The Shift
          </span>
          <div className="flex flex-col gap-4 flex-1">
            {SHIFT_PHASES.map((phase, i) => (
              <div key={phase.label} className="flex items-start gap-3">
                {/* Colored dot + connector line */}
                <div className="flex flex-col items-center pt-1">
                  <div
                    className="w-4 h-4 rounded-full shrink-0"
                    style={{ backgroundColor: phase.color }}
                  />
                  {i < SHIFT_PHASES.length - 1 && (
                    <div
                      className="w-px flex-1 mt-1"
                      style={{ backgroundColor: '#e4e4e7' }}
                    />
                  )}
                </div>
                <div className="pb-1">
                  <span className="font-body text-base font-bold text-zinc-900 block leading-tight">
                    {phase.label}
                  </span>
                  <span className="font-body text-sm text-zinc-600 leading-snug block mt-0.5">
                    {phase.detail}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Bottom summary */}
          <div className="border-t border-zinc-100 pt-3 mt-auto">
            <div className="flex items-center gap-2 mb-1.5">
              <span className="font-body text-sm text-zinc-500">Y1 avg</span>
              <span className="font-body text-lg font-bold text-zinc-500">$7K</span>
              <ArrowRight className="w-4 h-4 text-zinc-300" />
              <span className="font-body text-sm text-zinc-500">Y5 avg</span>
              <span className="font-body text-lg font-bold" style={{ color: '#C9A84C' }}>$58K</span>
            </div>
            <span className="font-body text-xs text-zinc-500 leading-snug">
              Each micro-purchase builds the past performance record needed to win larger contracts.
            </span>
          </div>
        </motion.div>
      </div>

      <SourceCitation>
        Win rates: FPDS competition analysis FY2024 | Renewal: ~70% federal recompete incumbent rate (Fed-Spend) | Portfolio mix: modeled estimates
      </SourceCitation>
    </div>
  )
}
