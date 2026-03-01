import { useMemo, useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { DollarSign, TrendingUp, Calendar, AlertTriangle } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import NumberInput from '../ui/NumberInput'
import AnimatedNumber from '../ui/AnimatedNumber'
import useFinancialModel from '../../hooks/useFinancialModel'
import { computeProForma, computeCashFlow } from '../../data/financials'

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])

function fmtCompact(v) {
  const abs = Math.abs(v)
  const sign = v < 0 ? '-' : ''
  if (abs >= 1_000_000) return sign + '$' + (abs / 1_000_000).toFixed(1) + 'M'
  if (abs >= 1_000) return sign + '$' + (abs / 1_000).toFixed(0) + 'K'
  return sign + '$' + abs.toLocaleString('en-US')
}

const KPI_DEFS = [
  { key: 'y1Profit', label: 'Year 1 Profit', icon: DollarSign, format: 'compact' },
  { key: 'paybackYear', label: 'Breakeven Year', icon: Calendar, format: 'year' },
  { key: 'totalProfit', label: '5-Year Total Profit', icon: TrendingUp, format: 'compact' },
  { key: 'peakWC', label: 'Peak WC Required', icon: AlertTriangle, format: 'compact' },
]

export default function CashFlowSlide() {
  const { route, scenario, overrides, setRoute, setScenario, updateOverride } = useFinancialModel()
  const [workingCapital, setWorkingCapital] = [
    overrides._workingCapital ?? 75000,
    (v) => updateOverride('_workingCapital', v),
  ]

  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  const model = useMemo(
    () => computeProForma(route, scenario, overrides),
    [route, scenario, overrides]
  )

  const cashFlow = useMemo(
    () => computeCashFlow(model, workingCapital),
    [model, workingCapital]
  )

  // KPI values — answering the owner's real questions
  const peakWC = Math.max(...cashFlow.years.map(y => y.wcRequired))
  const kpiValues = useMemo(() => ({
    y1Profit: model.years[0].netIncome,
    paybackYear: model.summary.paybackYear,
    totalProfit: model.summary.totalReturn,
    peakWC,
  }), [model, peakWC])

  // WC constraint indicator
  const wcRatio = workingCapital > 0 ? peakWC / workingCapital : 999
  const wcStatus = wcRatio <= 0.6 ? 'green' : wcRatio <= 1.0 ? 'yellow' : 'red'
  const wcColors = { green: '#10b981', yellow: '#eab308', red: '#ef4444' }

  // Init chart
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

  // Update chart — annual net income bars
  useEffect(() => {
    if (!chartInstance.current) return

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(0,0,0,0.03)' } },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif' },
        padding: [10, 14],
        formatter: (params) => {
          const idx = params[0].dataIndex
          const yr = model.years[idx]
          const cfYr = cashFlow.years[idx]
          const opex = yr.deliveryCost + yr.platformCost + yr.adminOverhead + yr.bdMarketingCost
          let html = `<div style="font-weight:600;margin-bottom:6px;font-size:13px">Year ${yr.year}</div>`
          html += `<div style="display:flex;justify-content:space-between;gap:24px;margin:2px 0">
            <span>Revenue</span><span style="font-weight:600">${fmtCompact(yr.revenue)}</span></div>`
          html += `<div style="display:flex;justify-content:space-between;gap:24px;margin:2px 0">
            <span style="color:#a1a1aa">COGS</span><span style="font-weight:600;color:#a1a1aa">-${fmtCompact(yr.cogs)}</span></div>`
          html += `<div style="display:flex;justify-content:space-between;gap:24px;margin:2px 0">
            <span style="color:#a1a1aa">Operating Costs</span><span style="font-weight:600;color:#a1a1aa">-${fmtCompact(opex)}</span></div>`
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:6px;display:flex;justify-content:space-between;gap:24px">
            <span style="font-weight:600">Net Profit</span>
            <span style="font-weight:700;color:${yr.netIncome >= 0 ? '#C9A84C' : '#ef4444'}">${fmtCompact(yr.netIncome)}</span></div>`
          html += `<div style="display:flex;justify-content:space-between;gap:24px;margin:2px 0">
            <span>Cumulative</span><span style="font-weight:600;color:#1B7A8A">${fmtCompact(yr.cumulativeNetIncome)}</span></div>`
          if (cfYr.wcRequired > 0) {
            html += `<div style="margin-top:4px;font-size:11px;color:#71717a">WC Required: ${fmtCompact(cfYr.wcRequired)}</div>`
          }
          return html
        },
      },
      grid: { left: 60, right: 16, top: 24, bottom: 28 },
      xAxis: {
        type: 'category',
        data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
        axisLine: { lineStyle: { color: '#e5e5e5' } },
        axisTick: { show: false },
        axisLabel: { color: '#71717a', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12, fontWeight: 600 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#f4f4f5' } },
        axisLabel: {
          color: '#a1a1aa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 11,
          formatter: (v) => {
            if (v === 0) return '$0'
            if (Math.abs(v) >= 1_000_000) return '$' + (v / 1_000_000).toFixed(1) + 'M'
            return '$' + (v / 1_000).toFixed(0) + 'K'
          },
        },
      },
      series: [
        {
          name: 'Annual Profit',
          type: 'bar',
          data: model.years.map(y => ({
            value: y.netIncome,
            itemStyle: {
              color: y.netIncome >= 0
                ? { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [
                    { offset: 0, color: '#C9A84C' },
                    { offset: 1, color: '#d4b35c' },
                  ]}
                : '#ef4444',
              borderRadius: y.netIncome >= 0 ? [6, 6, 0, 0] : [0, 0, 6, 6],
            },
          })),
          barWidth: 56,
          label: {
            show: true,
            position: 'top',
            formatter: (params) => fmtCompact(params.value),
            color: '#3f3f46',
            fontSize: 12,
            fontWeight: 600,
            fontFamily: 'Inter, system-ui, sans-serif',
          },
          animationDuration: 600,
          animationDelay: (idx) => idx * 100,
        },
      ],
    }, true)
  }, [model, cashFlow])

  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      <BackgroundRing size={500} className="-bottom-40 -left-40" opacity={0.02} />

      {/* Header + Controls */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5"
        >
          Owner Returns
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Cash Flow & Profitability
        </motion.h2>
        <GoldLine width={60} className="mt-1" delay={0.25} />

        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.4 }}
          className="flex items-center gap-3 mt-3"
        >
          <RouteToggle active={route} onChange={setRoute} />
          <ScenarioToggle active={scenario} onChange={setScenario} />
        </motion.div>
      </div>

      {/* Main content */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.5 }}
        className="flex gap-4 flex-1 min-h-0 relative z-10"
      >
        {/* LEFT: Working Capital sidebar */}
        <div className="w-[220px] shrink-0 rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col gap-4 overflow-auto">
          <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">
            Working Capital
          </div>
          <NumberInput
            label="Available WC"
            value={workingCapital}
            onChange={setWorkingCapital}
            min={0}
            max={2000000}
            step={5000}
            format="currency"
          />

          {/* WC Constraint Indicator */}
          <div className="border-t border-zinc-100 pt-3">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-2">
              WC Constraint
            </div>
            <div className="flex flex-col gap-2">
              <div className="flex justify-between text-xs">
                <span className="text-zinc-500">Peak Required</span>
                <span className="font-semibold text-zinc-800 tabular-nums">{fmtCompact(peakWC)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-zinc-500">Available</span>
                <span className="font-semibold text-zinc-800 tabular-nums">{fmtCompact(workingCapital)}</span>
              </div>
              {/* Bar indicator */}
              <div className="h-2.5 rounded-full bg-zinc-100 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(wcRatio * 100, 100)}%`,
                    backgroundColor: wcColors[wcStatus],
                  }}
                />
              </div>
              <span className="text-[10px] font-medium" style={{ color: wcColors[wcStatus] }}>
                {wcStatus === 'green' ? 'Sufficient' : wcStatus === 'yellow' ? 'Tight — near limit' : 'Constrained — exceeds WC'}
              </span>
            </div>
          </div>

          {/* Annual profit summary */}
          <div className="border-t border-zinc-100 pt-3">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-2">
              Annual Profit
            </div>
            <div className="flex flex-col gap-1.5">
              {model.years.map(y => (
                <div key={y.year} className="flex justify-between text-xs">
                  <span className="text-zinc-500">Y{y.year}</span>
                  <span className={`font-semibold tabular-nums ${y.netIncome >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                    {fmtCompact(y.netIncome)}
                  </span>
                </div>
              ))}
              <div className="flex justify-between text-xs border-t border-zinc-100 pt-1.5 mt-0.5">
                <span className="text-zinc-500 font-semibold">Total</span>
                <span className="font-bold tabular-nums text-zinc-900">
                  {fmtCompact(model.summary.totalReturn)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT: Dashboard */}
        <div className="flex-1 flex flex-col gap-4 min-w-0">
          {/* KPI Cards */}
          <div className="grid grid-cols-4 gap-4">
            {KPI_DEFS.map((kpi) => {
              const Icon = kpi.icon
              const val = kpiValues[kpi.key]
              let accent = '#1B7A8A'
              let borderClass = 'border-zinc-200'

              if (kpi.key === 'y1Profit') {
                accent = val >= 0 ? '#1B7A8A' : '#ef4444'
                borderClass = val < 0 ? 'border-red-300' : 'border-zinc-200'
              }
              if (kpi.key === 'totalProfit') {
                accent = val >= 0 ? '#C9A84C' : '#ef4444'
                borderClass = val < 0 ? 'border-red-300' : 'border-zinc-200'
              }
              if (kpi.key === 'peakWC') {
                accent = wcColors[wcStatus]
                borderClass = wcStatus === 'red' ? 'border-red-300' : 'border-zinc-200'
              }

              return (
                <div
                  key={kpi.key}
                  className={`rounded-xl bg-white border shadow-sm p-4 relative overflow-hidden ${borderClass}`}
                >
                  <div className="flex items-start justify-between mb-1">
                    <span className="font-body text-xs font-medium text-zinc-500 uppercase tracking-wider">
                      {kpi.label}
                    </span>
                    <Icon className="w-4 h-4 opacity-50" style={{ color: accent }} strokeWidth={1.5} />
                  </div>
                  {kpi.format === 'year' ? (
                    <span
                      className="font-body text-2xl font-semibold tracking-tight leading-none block"
                      style={{ color: accent }}
                    >
                      {val ? `Year ${val}` : '\u2014'}
                    </span>
                  ) : (
                    <AnimatedNumber
                      value={val}
                      format="compact"
                      className="font-body text-2xl font-semibold tracking-tight leading-none block"
                      style={{ color: accent }}
                    />
                  )}
                </div>
              )
            })}
          </div>

          {/* Chart — Annual Owner Profit */}
          <div className="flex-1 rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col min-h-0">
            <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-2">
              Annual Owner Profit
            </span>
            <div ref={chartRef} className="w-full flex-1 min-h-0" />
          </div>
        </div>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.4 }}
        className="text-[10px] text-zinc-400 font-body mt-2 relative z-10"
      >
        Sources: FPDS FY2024 | Prompt Payment Act DSO (FAR 52.232-25) | SLED 30-45d terms | WC = net receivables (AR - AP)
      </motion.p>
    </div>
  )
}
