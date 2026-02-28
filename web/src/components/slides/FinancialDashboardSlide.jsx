import { useState, useMemo, useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { DollarSign, TrendingUp, Calendar, BarChart3 } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import SourceCitation from '../ui/SourceCitation'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import AnimatedNumber from '../ui/AnimatedNumber'
import { computeProForma, SCENARIO_PARAMS } from '../../data/financials'

echarts.use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const KPI_DEFS = [
  { key: 'y1Revenue',    label: 'Y1 Revenue',        icon: DollarSign,  format: 'compact',  accent: '#C9A84C' },
  { key: 'y5Revenue',    label: 'Y5 Revenue',        icon: TrendingUp,  format: 'compact',  accent: '#1B7A8A' },
  { key: 'breakeven',    label: 'Breakeven Year',    icon: Calendar,    format: 'number',   accent: '#1B7A8A' },
  { key: 'y5Cumulative', label: '5-Year Total',      icon: BarChart3,   format: 'compact',  accent: '#C9A84C' },
]

export default function FinancialDashboardSlide() {
  const [scenario, setScenario] = useState('moderate')
  const [route, setRoute] = useState('free')
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  const model = useMemo(() => computeProForma(scenario, route), [scenario, route])

  const kpiValues = useMemo(() => ({
    y1Revenue: model.years[0].revenue,
    y5Revenue: model.summary.y5Revenue,
    breakeven: model.summary.breakevenYear ?? 0,
    y5Cumulative: model.summary.y5CumulativeRevenue,
  }), [model])

  // Init chart on mount
  useEffect(() => {
    if (!chartRef.current) return
    chartInstance.current = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    const handleResize = () => chartInstance.current?.resize()
    window.addEventListener('resize', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      chartInstance.current?.dispose()
      chartInstance.current = null
    }
  }, [])

  // Update chart data when model changes
  useEffect(() => {
    if (!chartInstance.current) return
    const color = SCENARIO_PARAMS[scenario].color

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 12, fontFamily: 'Inter' },
        padding: [8, 12],
        formatter: (params) => {
          const d = model.years[params[0].dataIndex]
          return `<div style="font-weight:600;margin-bottom:6px">Year ${d.year}</div>
            <div style="display:flex;justify-content:space-between;gap:16px;margin:2px 0">
              <span>Revenue</span><span style="font-weight:600">$${(d.revenue / 1000).toFixed(0)}K</span>
            </div>
            <div style="display:flex;justify-content:space-between;gap:16px;margin:2px 0">
              <span>Net Income</span><span style="font-weight:600;color:${d.netIncome >= 0 ? '#4ade80' : '#f87171'}">$${(d.netIncome / 1000).toFixed(0)}K</span>
            </div>
            <div style="display:flex;justify-content:space-between;gap:16px;margin:2px 0">
              <span>Active Contracts</span><span style="font-weight:600">${d.activeContracts}</span>
            </div>`
        },
      },
      grid: { left: 56, right: 20, top: 16, bottom: 32 },
      xAxis: {
        type: 'category',
        data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
        axisLine: { lineStyle: { color: '#e5e5e5' } },
        axisTick: { show: false },
        axisLabel: { color: '#71717a', fontFamily: 'Inter', fontSize: 12 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
        axisLabel: {
          color: '#71717a', fontFamily: 'Inter', fontSize: 11,
          formatter: (v) => v >= 1_000_000 ? '$' + (v / 1_000_000).toFixed(1) + 'M' : '$' + (v / 1_000) + 'K',
        },
      },
      series: [{
        type: 'line',
        data: model.years.map(y => y.revenue),
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: { color, width: 2.5 },
        itemStyle: { color, borderColor: '#fff', borderWidth: 2 },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: color + '25' }, { offset: 1, color: color + '05' }] } },
        animationDuration: 800,
      }],
    }, true)
  }, [model, scenario])

  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-2 pb-14 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-2 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5"
        >
          Financial Projections
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          Financial Outlook
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600"
        >
          Five-year revenue trajectory across three scenarios and two investment routes.
        </motion.p>
        <GoldLine width={60} className="mt-1" delay={0.25} />
      </div>

      {/* Controls */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="flex items-center justify-center gap-3 mb-2 relative z-10"
      >
        <RouteToggle active={route} onChange={setRoute} />
        <ScenarioToggle active={scenario} onChange={setScenario} />
      </motion.div>

      {/* KPI Cards */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.4 }}
        className="grid grid-cols-4 gap-2.5 mb-2 relative z-10"
      >
        {KPI_DEFS.map((kpi) => {
          const Icon = kpi.icon
          const val = kpiValues[kpi.key]
          return (
            <div
              key={kpi.key}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm px-4 py-3 relative overflow-hidden"
            >
              <div className="flex items-start justify-between mb-1">
                <span className="font-body text-[10px] font-medium text-zinc-500 uppercase tracking-wider">
                  {kpi.label}
                </span>
                <div
                  className="w-6 h-6 rounded-md flex items-center justify-center"
                  style={{ backgroundColor: kpi.accent + '12' }}
                >
                  <Icon className="w-3.5 h-3.5" style={{ color: kpi.accent }} strokeWidth={1.5} />
                </div>
              </div>
              <AnimatedNumber
                value={val}
                format={kpi.format}
                className="font-body text-2xl font-bold tracking-tight leading-none block"
                style={{ color: kpi.accent }}
              />
            </div>
          )
        })}
      </motion.div>

      {/* Chart */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm p-3 flex-1 min-h-0 flex flex-col relative z-10"
      >
        <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-1 block">
          5-Year Revenue Trajectory
        </span>
        <div ref={chartRef} className="w-full flex-1 min-h-0" />
      </motion.div>

      <SourceCitation>
        Win rates: FPDS FY2024 competition analysis | Contract values: USASpending FL food procurement | Renewal: 70% federal incumbent rate
      </SourceCitation>
    </div>
  )
}
