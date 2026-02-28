import { useState, useMemo, useEffect, useRef, Fragment } from 'react'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { DollarSign, TrendingUp, Calendar, BarChart3 } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import SourceCitation from '../ui/SourceCitation'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import AnimatedNumber from '../ui/AnimatedNumber'
import NumberInput from '../ui/NumberInput'
import { computeProForma, computeAllScenarios, SLIDER_CONFIGS, SCENARIO_CONFIGS } from '../../data/financials'

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const KPI_DEFS = [
  { key: 'y1Revenue', label: 'Year 1 Revenue', icon: DollarSign, format: 'compact', accent: '#C9A84C' },
  { key: 'y5Revenue', label: 'Year 5 Revenue', icon: TrendingUp, format: 'compact', accent: '#1B7A8A' },
  { key: 'breakeven', label: 'Breakeven Year', icon: Calendar, format: 'year', accent: '#1B7A8A' },
  { key: 'y5NetIncome', label: '5-Year Net Income', icon: BarChart3, format: 'compact' },
]

const TABLE_ROWS = [
  { key: 'bidsSubmitted', label: 'Bids Submitted', bold: false, format: 'number' },
  { key: 'newWins', label: 'New Wins', bold: false, format: 'number' },
  { key: 'renewals', label: 'Renewals', bold: false, format: 'number' },
  { key: 'activeContracts', label: 'Active Contracts', bold: false, format: 'number' },
  { key: 'revenue', label: 'Revenue', bold: true, format: 'currency' },
  { key: 'cogs', label: 'COGS', bold: false, format: 'currency', muted: true },
  { key: 'grossProfit', label: 'Gross Profit', bold: true, format: 'currency' },
  { key: 'platformCost', label: 'Platform & Insurance', bold: false, format: 'currency' },
  { key: 'deliveryCost', label: 'Delivery Costs', bold: false, format: 'currency' },
  { key: 'adminOverhead', label: 'Admin Overhead', bold: false, format: 'currency' },
  { key: 'netIncome', label: 'Net Income', bold: true, format: 'currency', colored: true },
  { key: 'cumulativeNetIncome', label: 'Cumulative Net', bold: false, format: 'currency', colored: true },
]

function fmtCell(value, format) {
  switch (format) {
    case 'currency': {
      const abs = Math.abs(value)
      const sign = value < 0 ? '-' : ''
      if (abs >= 1_000_000) return sign + '$' + (abs / 1_000_000).toFixed(1) + 'M'
      if (abs >= 1_000) return sign + '$' + (abs / 1_000).toFixed(0) + 'K'
      return sign + '$' + abs.toLocaleString('en-US')
    }
    case 'number':
      return value.toLocaleString('en-US')
    default:
      return String(value)
  }
}

function fmtTooltipCurrency(v) {
  const abs = Math.abs(v)
  const sign = v < 0 ? '-' : ''
  if (abs >= 1_000_000) return sign + '$' + (abs / 1_000_000).toFixed(1) + 'M'
  if (abs >= 1_000) return sign + '$' + (abs / 1_000).toFixed(0) + 'K'
  return sign + '$' + abs.toLocaleString('en-US')
}

export default function FinancialOutlookSlide() {
  const [route, setRoute] = useState('free')
  const [scenario, setScenario] = useState('moderate')
  const [overrides, setOverrides] = useState(() => {
    const o = {}
    SLIDER_CONFIGS.forEach(s => { o[s.key] = s.default })
    return o
  })

  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  const model = useMemo(
    () => computeProForma(route, scenario, overrides),
    [route, scenario, overrides]
  )

  const allModels = useMemo(
    () => computeAllScenarios(route, overrides),
    [route, overrides]
  )

  const kpiValues = useMemo(() => ({
    y1Revenue: model.years[0].revenue,
    y5Revenue: model.summary.y5Revenue,
    breakeven: model.summary.breakevenYear,
    y5NetIncome: model.summary.totalReturn,
  }), [model])

  const updateOverride = (key, value) => {
    setOverrides(prev => ({ ...prev, [key]: value }))
  }

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

  // Update chart — 3-scenario overlapping area
  useEffect(() => {
    if (!chartInstance.current) return

    const scenarioKeys = ['aggressive', 'moderate', 'conservative']

    const series = scenarioKeys.map((key) => {
      const sc = SCENARIO_CONFIGS[key]
      const m = allModels[key]
      const isActive = key === scenario
      return {
        name: sc.label,
        type: 'line',
        data: m.years.map(y => y.revenue),
        smooth: true,
        symbol: 'circle',
        symbolSize: isActive ? 6 : 0,
        lineStyle: { width: isActive ? 3 : 1.5, color: sc.color },
        itemStyle: { color: sc.color },
        areaStyle: { opacity: isActive ? 0.35 : 0.08, color: sc.color },
        z: isActive ? 10 : 1,
        emphasis: { disabled: true },
      }
    })

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'line', lineStyle: { color: '#d4d4d8', type: 'dashed' } },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 12, fontFamily: 'Inter' },
        padding: [10, 14],
        formatter: (params) => {
          const yearIdx = params[0].dataIndex
          const routeLabel = route === 'paid' ? 'Paid Route' : 'Free Route'
          let html = `<div style="font-weight:600;margin-bottom:6px;font-size:13px">Year ${yearIdx + 1} \u2014 ${routeLabel}</div>`

          // All 3 scenario values
          scenarioKeys.forEach((key) => {
            const sc = SCENARIO_CONFIGS[key]
            const yearData = allModels[key].years[yearIdx]
            const isActive = key === scenario
            const arrow = isActive ? '\u25b8 ' : '  '
            const weight = isActive ? '700' : '400'
            const opacity = isActive ? '1' : '0.6'
            html += `<div style="display:flex;justify-content:space-between;gap:20px;margin:3px 0;opacity:${opacity}">
              <span style="font-weight:${weight}"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${sc.color};margin-right:6px"></span>${arrow}${sc.label}</span>
              <span style="font-weight:${weight}">${fmtTooltipCurrency(yearData.revenue)}</span>
            </div>`
          })

          // Active scenario tier breakdown
          const activeYear = allModels[scenario].years[yearIdx]
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:6px;font-size:11px;color:#a1a1aa">`
          html += `Bids: ${activeYear.bidsSubmitted} &nbsp;|&nbsp; Wins: ${activeYear.newWins} &nbsp;|&nbsp; Renewals: ${activeYear.renewals}`
          activeYear.tierBreakdown.filter(t => t.revenue > 0).forEach(t => {
            html += `<div style="margin-top:2px">${t.tier}: ${t.count} \u00d7 ${fmtTooltipCurrency(t.avgValue)} = ${fmtTooltipCurrency(t.revenue)}</div>`
          })
          html += `</div>`
          return html
        },
      },
      grid: { left: 52, right: 12, top: 8, bottom: 24 },
      xAxis: {
        type: 'category',
        data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
        boundaryGap: false,
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
          color: '#a1a1aa', fontFamily: 'Inter', fontSize: 11,
          formatter: (v) => {
            if (v === 0) return '0'
            return Math.abs(v) >= 1_000_000
              ? '$' + (v / 1_000_000).toFixed(1) + 'M'
              : '$' + (v / 1_000).toFixed(0) + 'K'
          },
        },
      },
      series,
    }, true)
  }, [allModels, scenario, route])

  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-2 pb-14 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-1 relative z-10">
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
        <GoldLine width={60} className="mt-0.5" delay={0.25} />
      </div>

      {/* Controls: toggles + inputs */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="flex items-center gap-3 mb-2 relative z-10 flex-wrap"
      >
        <div className="flex items-center gap-2 shrink-0">
          <RouteToggle active={route} onChange={setRoute} />
          <ScenarioToggle active={scenario} onChange={setScenario} />
        </div>
        <div className="h-5 w-px bg-zinc-200 shrink-0" />
        <div className="flex items-center gap-3 flex-wrap">
          {SLIDER_CONFIGS.map((cfg) => (
            <NumberInput
              key={cfg.key}
              label={cfg.label}
              value={overrides[cfg.key]}
              onChange={(v) => updateOverride(cfg.key, v)}
              min={cfg.min}
              max={cfg.max}
              step={cfg.step}
              format={cfg.format}
            />
          ))}
        </div>
      </motion.div>

      {/* KPI Tiles */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.4 }}
        className="grid grid-cols-4 gap-3 mb-2 relative z-10"
      >
        {KPI_DEFS.map((kpi) => {
          const Icon = kpi.icon
          const val = kpiValues[kpi.key]
          // Dynamic accent for net income card
          let accent = kpi.accent
          let borderClass = 'border-zinc-200'
          if (kpi.key === 'y5NetIncome') {
            accent = val >= 0 ? '#10b981' : '#ef4444'
            borderClass = val >= 0 ? 'border-emerald-300' : 'border-red-300'
          }

          return (
            <div
              key={kpi.key}
              className={`rounded-xl bg-white border shadow-sm px-4 py-2.5 relative overflow-hidden ${borderClass}`}
            >
              <div className="flex items-start justify-between mb-1">
                <span className="font-body text-[10px] font-medium text-zinc-500 uppercase tracking-wider">
                  {kpi.label}
                </span>
                <Icon className="w-4 h-4 opacity-20" style={{ color: accent }} strokeWidth={1.5} />
              </div>
              {kpi.format === 'year' ? (
                <span
                  className="font-body text-2xl font-bold tracking-tight leading-none block"
                  style={{ color: accent }}
                >
                  {val ? `Year ${val}` : '\u2014'}
                </span>
              ) : (
                <AnimatedNumber
                  value={val}
                  format={kpi.format}
                  className="font-body text-2xl font-bold tracking-tight leading-none block"
                  style={{ color: accent }}
                />
              )}
            </div>
          )
        })}
      </motion.div>

      {/* Main content: Table + Chart side by side */}
      <div className="flex gap-3 flex-1 min-h-0 relative z-10">
        {/* Table (55%) */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="w-[55%] rounded-xl bg-white border border-zinc-200 shadow-sm p-3 overflow-auto"
        >
          <div
            className="grid gap-y-0"
            style={{ gridTemplateColumns: '120px repeat(5, 1fr)' }}
          >
            {/* Header */}
            <div className="text-[10px] font-medium text-zinc-400 uppercase tracking-wider pb-1 border-b border-zinc-200" />
            {model.years.map((y) => (
              <div key={y.year} className="text-[10px] font-medium text-zinc-400 uppercase tracking-wider pb-1 border-b border-zinc-200 text-right pr-2">
                Year {y.year}
              </div>
            ))}

            {/* Rows */}
            {TABLE_ROWS.map((row, ri) => (
              <Fragment key={row.key}>
                <div
                  className={`py-0.5 text-[11px] pr-1 truncate ${row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-500'} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
                >
                  {row.label}
                </div>
                {model.years.map((y) => {
                  const val = y[row.key]
                  let colorClass = row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-600'
                  if (row.muted) colorClass = 'text-zinc-400'
                  if (row.colored) {
                    colorClass = val >= 0 ? 'font-semibold text-emerald-600' : 'font-semibold text-red-500'
                  }
                  return (
                    <div
                      key={`${row.key}-${y.year}`}
                      className={`py-0.5 text-[11px] text-right pr-2 tabular-nums ${colorClass} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
                    >
                      {fmtCell(val, row.format)}
                    </div>
                  )
                })}
              </Fragment>
            ))}
          </div>
        </motion.div>

        {/* Chart (45%) */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.45, duration: 0.5 }}
          className="w-[45%] rounded-xl bg-white border border-zinc-200 shadow-sm p-3 flex flex-col"
        >
          <div className="flex items-center justify-between mb-1">
            <span className="font-body text-[10px] font-semibold text-zinc-500 uppercase tracking-wider">
              Revenue — All Scenarios
            </span>
            <div className="flex items-center gap-2">
              {Object.entries(SCENARIO_CONFIGS).map(([key, sc]) => (
                <div key={key} className={`flex items-center gap-1 transition-opacity ${key === scenario ? 'opacity-100' : 'opacity-40'}`}>
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: sc.color }} />
                  <span className="text-[10px] text-zinc-500">{sc.label}</span>
                </div>
              ))}
            </div>
          </div>
          <div ref={chartRef} className="w-full flex-1 min-h-0" />
        </motion.div>
      </div>

      <SourceCitation>
        Win rates: FPDS FY2024 | Contract values: USASpending FL | Renewal: 70% incumbent rate | All financial inputs adjustable
      </SourceCitation>
    </div>
  )
}
