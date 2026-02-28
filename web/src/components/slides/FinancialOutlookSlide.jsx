import { useState, useMemo, useEffect, useRef, Fragment } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
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
import { computeProForma, SLIDER_CONFIGS, TIER_CONFIGS } from '../../data/financials'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const KPI_DEFS = [
  { key: 'y1Revenue',    label: 'Y1 Revenue',     icon: DollarSign, format: 'compact', accent: '#C9A84C' },
  { key: 'y5Revenue',    label: 'Y5 Revenue',     icon: TrendingUp, format: 'compact', accent: '#1B7A8A' },
  { key: 'breakeven',    label: 'Breakeven Year',  icon: Calendar,   format: 'number',  accent: '#1B7A8A' },
  { key: 'y5Cumulative', label: '5-Year Total',    icon: BarChart3,  format: 'compact', accent: '#C9A84C' },
]

const TABLE_ROWS = [
  { key: 'bidsSubmitted',    label: 'Bids Submitted',   bold: false, format: 'number' },
  { key: 'newWins',          label: 'New Wins',         bold: false, format: 'number' },
  { key: 'renewals',         label: 'Renewals',         bold: false, format: 'number' },
  { key: 'activeContracts',  label: 'Active Contracts', bold: false, format: 'number' },
  { key: 'revenue',          label: 'Revenue',          bold: true,  format: 'currency' },
  { key: 'cogs',             label: 'COGS',             bold: false, format: 'currency' },
  { key: 'grossProfit',      label: 'Gross Profit',     bold: true,  format: 'currency' },
  { key: 'toolCost',         label: 'Tool Costs',       bold: false, format: 'currency' },
  { key: 'adminCost',        label: 'Admin Costs',      bold: false, format: 'currency' },
  { key: 'netIncome',        label: 'Net Income',       bold: true,  format: 'currency', colored: true },
  { key: 'cumulativeRevenue', label: 'Cumulative Rev.', bold: false, format: 'currency' },
  { key: 'roi',              label: 'ROI',              bold: false, format: 'roi' },
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
    case 'roi':
      if (value === Infinity) return '\u221e'
      if (value === 0) return '\u2014'
      return (value * 100).toFixed(0) + '%'
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
  const [scenario, setScenario] = useState('moderate')
  const [route, setRoute] = useState('free')
  const [overrides, setOverrides] = useState(() => {
    const o = {}
    SLIDER_CONFIGS.forEach(s => { o[s.key] = s.default })
    return o
  })

  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  const model = useMemo(
    () => computeProForma(scenario, route, overrides),
    [scenario, route, overrides]
  )

  const kpiValues = useMemo(() => ({
    y1Revenue: model.years[0].revenue,
    y5Revenue: model.summary.y5Revenue,
    breakeven: model.summary.breakevenYear ?? 0,
    y5Cumulative: model.summary.y5CumulativeRevenue,
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

  // Update chart data — stacked bar by tier
  useEffect(() => {
    if (!chartInstance.current) return

    const series = TIER_CONFIGS.map((tc, idx) => ({
      name: tc.label,
      type: 'bar',
      stack: 'revenue',
      data: model.years.map(y => y.tiers[idx].revenue),
      itemStyle: {
        color: tc.color,
        ...(idx === TIER_CONFIGS.length - 1 ? { borderRadius: [3, 3, 0, 0] } : {}),
      },
      barWidth: 48,
      emphasis: { focus: 'series' },
    }))

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 13, fontFamily: 'Inter' },
        padding: [10, 14],
        formatter: (params) => {
          const yearIdx = params[0].dataIndex
          const yearData = model.years[yearIdx]
          let html = `<div style="font-weight:600;margin-bottom:6px;font-size:14px">Year ${yearData.year}</div>`
          params.forEach(p => {
            const tier = yearData.tiers[p.seriesIndex]
            html += `<div style="margin:4px 0">
              <div style="display:flex;justify-content:space-between;gap:16px">
                <span>${p.marker} ${tier.label}</span>
                <span style="font-weight:600">${fmtTooltipCurrency(tier.revenue)}</span>
              </div>
              <div style="color:#a1a1aa;font-size:12px;margin-left:14px">${tier.contracts} contracts @ ${fmtTooltipCurrency(tier.avgValue)} avg</div>
            </div>`
          })
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:4px;display:flex;justify-content:space-between;gap:16px">
            <span style="color:#C9A84C;font-weight:600">Total</span>
            <span style="color:#C9A84C;font-weight:600">${fmtTooltipCurrency(yearData.revenue)}</span>
          </div>`
          return html
        },
      },
      grid: { left: 56, right: 16, top: 12, bottom: 28 },
      xAxis: {
        type: 'category',
        data: model.years.map(y => 'Y' + y.year),
        axisLine: { lineStyle: { color: '#e5e5e5' } },
        axisTick: { show: false },
        axisLabel: { color: '#71717a', fontFamily: 'Inter', fontSize: 13 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
        axisLabel: {
          color: '#a1a1aa', fontFamily: 'Inter', fontSize: 12,
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
  }, [model])

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

      {/* Controls row: toggles + number inputs */}
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
          return (
            <div
              key={kpi.key}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm px-4 py-2.5 relative overflow-hidden"
            >
              <div className="flex items-start justify-between mb-1">
                <span className="font-body text-xs font-medium text-zinc-500 uppercase tracking-wider">
                  {kpi.label}
                </span>
                <Icon className="w-4 h-4 opacity-20" style={{ color: kpi.accent }} strokeWidth={1.5} />
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

      {/* Board 1: Stacked Bar Chart — Revenue Mix by Contract Tier */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="flex-[2] min-h-0 rounded-xl bg-white border border-zinc-200 shadow-sm p-3.5 flex flex-col mb-2 relative z-10"
      >
        <div className="flex items-center justify-between mb-1.5">
          <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider">
            Revenue Mix by Contract Tier
          </span>
          <div className="flex items-center gap-3">
            {TIER_CONFIGS.map((tc) => (
              <div key={tc.key} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: tc.color }} />
                <span className="text-xs text-zinc-500">{tc.label}</span>
              </div>
            ))}
          </div>
        </div>
        <div ref={chartRef} className="w-full flex-1 min-h-0" />
      </motion.div>

      {/* Board 2: Financial Table */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.45, duration: 0.5 }}
        className="flex-[3] min-h-0 rounded-xl bg-white border border-zinc-200 shadow-sm p-3.5 overflow-auto relative z-10"
      >
        <div
          className="grid gap-y-0"
          style={{ gridTemplateColumns: '130px repeat(5, 1fr)' }}
        >
          {/* Header row */}
          <div className="text-xs font-medium text-zinc-400 uppercase tracking-wider pb-1.5 border-b border-zinc-200" />
          {model.years.map((y) => (
            <div key={y.year} className="text-xs font-medium text-zinc-400 uppercase tracking-wider pb-1.5 border-b border-zinc-200 text-right pr-3">
              Year {y.year}
            </div>
          ))}

          {/* Data rows */}
          {TABLE_ROWS.map((row, ri) => (
            <Fragment key={row.key}>
              <div
                className={`py-1 text-[13px] pr-2 truncate ${row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-600'} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
              >
                {row.label}
              </div>
              {model.years.map((y) => {
                const val = y[row.key]
                let colorClass = row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-600'
                if (row.colored) {
                  colorClass = val >= 0 ? 'font-semibold text-emerald-600' : 'font-semibold text-red-500'
                }
                return (
                  <div
                    key={row.key + '-' + y.year}
                    className={`py-1 text-[13px] text-right pr-3 tabular-nums ${colorClass} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
                  >
                    {fmtCell(val, row.format)}
                  </div>
                )
              })}
            </Fragment>
          ))}
        </div>
      </motion.div>

      <SourceCitation>
        Win rates: FPDS FY2024 competition analysis | Contract values: USASpending FL food procurement | Renewal: 70% federal incumbent rate | Margin: user-adjustable
      </SourceCitation>
    </div>
  )
}
