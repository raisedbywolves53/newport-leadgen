import { useState, useMemo, useEffect, useRef, Fragment } from 'react'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { DollarSign, TrendingUp, Calendar, BarChart3 } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import AnimatedNumber from '../ui/AnimatedNumber'
import Slider from '../ui/Slider'
import { computeProForma, computeAllScenarios, SLIDER_CONFIGS, SCENARIO_CONFIGS, TOGGLE_CONFIGS } from '../../data/financials'

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const KPI_DEFS = [
  { key: 'y1Revenue', label: 'Year 1 Revenue', icon: DollarSign, format: 'compact', accent: '#C9A84C' },
  { key: 'y5Revenue', label: 'Year 5 Revenue', icon: TrendingUp, format: 'compact', accent: '#1B7A8A' },
  { key: 'breakeven', label: 'Breakeven', icon: Calendar, format: 'year', accent: '#1B7A8A' },
  { key: 'y5NetIncome', label: '5-Year Net', icon: BarChart3, format: 'compact' },
]

const TABLE_ROWS = [
  { key: 'activeContracts', label: 'Active Contracts', bold: false, format: 'number' },
  { key: 'revenue', label: 'Revenue', bold: true, format: 'currency' },
  { key: 'grossProfit', label: 'Gross Profit', bold: false, format: 'currency' },
  { key: 'platformCost', label: 'Platform & Ins.', bold: false, format: 'currency', muted: true },
  { key: 'bdMarketingCost', label: 'BD / Marketing', bold: false, format: 'currency', muted: true },
  { key: 'deliveryCost', label: 'Delivery', bold: false, format: 'currency', muted: true },
  { key: 'adminOverhead', label: 'Admin / Owner', bold: false, format: 'currency', muted: true },
  { key: 'netIncome', label: 'Net Income', bold: true, format: 'currency', colored: true, topBorder: true },
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

function fiveYearTotal(years, key) {
  return years.reduce((sum, y) => sum + y[key], 0)
}

export default function FinancialOutlookSlide() {
  const [route, setRoute] = useState('free')
  const [scenario, setScenario] = useState('moderate')
  const [overrides, setOverrides] = useState(() => {
    const o = {}
    SLIDER_CONFIGS.forEach(s => { o[s.key] = s.default })
    TOGGLE_CONFIGS.forEach(t => { o[t.key] = t.default })
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
        areaStyle: { opacity: isActive ? 0.35 : 0.12, color: sc.color },
        z: isActive ? 10 : 1,
        emphasis: { disabled: true },
      }
    })

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      animation: false,
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'line', lineStyle: { color: '#d4d4d8', type: 'dashed' } },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif' },
        padding: [10, 14],
        formatter: (params) => {
          const yearIdx = params[0].dataIndex
          const routeLabel = route === 'paid' ? 'Paid Route' : 'Free Route'
          let html = `<div style="font-weight:600;margin-bottom:6px;font-size:13px">Year ${yearIdx + 1} \u2014 ${routeLabel}</div>`

          scenarioKeys.forEach((key) => {
            const sc = SCENARIO_CONFIGS[key]
            const yearData = allModels[key].years[yearIdx]
            const isActive = key === scenario
            const arrow = isActive ? '\u25b8 ' : '  '
            const weight = isActive ? '700' : '400'
            const op = isActive ? '1' : '0.6'
            html += `<div style="display:flex;justify-content:space-between;gap:20px;margin:3px 0;opacity:${op}">
              <span style="font-weight:${weight}"><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${sc.color};margin-right:6px"></span>${arrow}${sc.label}</span>
              <span style="font-weight:${weight}">${fmtTooltipCurrency(yearData.revenue)}</span>
            </div>`
          })

          const activeYear = allModels[scenario].years[yearIdx]
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:6px;font-size:11px;color:#a1a1aa">`
          html += `Bids: ${activeYear.bidsSubmitted} | Wins: ${activeYear.newWins} | Renewals: ${activeYear.renewals}`
          html += `<div style="margin-top:3px">Net Income: <span style="color:${activeYear.netIncome >= 0 ? '#10b981' : '#ef4444'};font-weight:600">${fmtTooltipCurrency(activeYear.netIncome)}</span></div>`
          activeYear.tierBreakdown.filter(t => t.revenue > 0).forEach(t => {
            html += `<div style="margin-top:2px">${t.tier}: ${t.count} \u00d7 ${fmtTooltipCurrency(t.avgValue)} = ${fmtTooltipCurrency(t.revenue)}</div>`
          })
          html += `</div>`
          return html
        },
      },
      grid: { left: 52, right: 16, top: 12, bottom: 28 },
      xAxis: {
        type: 'category',
        data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
        boundaryGap: false,
        axisLine: { lineStyle: { color: '#e5e5e5' } },
        axisTick: { show: false },
        axisLabel: { color: '#71717a', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 11 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
        axisLabel: {
          color: '#a1a1aa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 11,
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
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.02} />

      {/* Header + Controls */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5"
        >
          Financial Projections
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Financial Outlook
        </motion.h2>
        <GoldLine width={60} className="mt-1" delay={0.25} />

        {/* Route + Scenario Toggles */}
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

      {/* Main 2-column layout: Input Sidebar + Dashboard */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.5 }}
        className="flex gap-4 flex-1 min-h-0 relative z-10"
      >
        {/* LEFT: Input Sidebar (mortgage calculator panel) */}
        <div className="w-[220px] shrink-0 rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col gap-4 overflow-auto">
          <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider">
            Your Assumptions
          </div>

          {/* Sliders */}
          <div className="flex flex-col gap-3">
            {SLIDER_CONFIGS.map((cfg) => (
              <Slider
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

          {/* Divider + Newport-specific toggles */}
          <div className="border-t border-zinc-100 pt-3">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-3">
              Newport-Specific
            </div>
            {TOGGLE_CONFIGS.map((toggle) => (
              <div key={toggle.key} className="flex items-center justify-between mb-2.5">
                <div className="flex flex-col">
                  <span className="text-xs font-medium text-zinc-600">{toggle.label}</span>
                  <span className="text-[10px] text-zinc-400 leading-tight">{toggle.description}</span>
                </div>
                <button
                  onClick={() => updateOverride(toggle.key, !overrides[toggle.key])}
                  className={`shrink-0 ml-2 w-9 h-5 rounded-full transition-colors relative cursor-pointer ${
                    overrides[toggle.key] ? 'bg-[#1B7A8A]' : 'bg-zinc-200'
                  }`}
                >
                  <div
                    className={`absolute top-0.5 w-4 h-4 rounded-full bg-white shadow-sm transition-transform ${
                      overrides[toggle.key] ? 'translate-x-4' : 'translate-x-0.5'
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT: Dashboard Main Panel */}
        <div className="flex-1 flex flex-col gap-4 min-w-0">
          {/* KPI Cards */}
          <div className="grid grid-cols-4 gap-4">
            {KPI_DEFS.map((kpi) => {
              const Icon = kpi.icon
              const val = kpiValues[kpi.key]
              let accent = kpi.accent
              let borderClass = 'border-zinc-200'
              if (kpi.key === 'y5NetIncome') {
                accent = val >= 0 ? '#10b981' : '#ef4444'
                borderClass = val >= 0 ? 'border-emerald-300' : 'border-red-300'
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
                    <Icon className="w-4 h-4 opacity-20" style={{ color: accent }} strokeWidth={1.5} />
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
                      format={kpi.format}
                      className="font-body text-2xl font-semibold tracking-tight leading-none block"
                      style={{ color: accent }}
                    />
                  )}
                </div>
              )
            })}
          </div>

          {/* Chart (top) + Table (bottom) — vertical stack */}
          <div className="flex flex-col gap-3 flex-1 min-h-0">
            {/* Chart Card — takes available space but shares with table */}
            <div className="flex-[3] rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col min-h-0">
              <div className="flex items-center justify-between mb-2">
                <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider">
                  Revenue — All Scenarios
                </span>
                <div className="flex items-center gap-3">
                  {Object.entries(SCENARIO_CONFIGS).map(([key, sc]) => (
                    <div key={key} className={`flex items-center gap-1.5 transition-opacity ${key === scenario ? 'opacity-100' : 'opacity-40'}`}>
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: sc.color }} />
                      <span className="text-xs text-zinc-500">{sc.label}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div ref={chartRef} className="w-full flex-1 min-h-0" />
            </div>

            {/* P&L Table — full width */}
            <div className="flex-[2] rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col justify-center">
              <div
                className="grid"
                style={{ gridTemplateColumns: '130px repeat(5, 1fr) 1fr' }}
              >
                {/* Header row */}
                <div className="text-xs font-medium text-zinc-500 uppercase tracking-wider pb-2 border-b border-zinc-200">
                  Pro Forma P&L
                </div>
                {model.years.map((y) => (
                  <div key={y.year} className="text-xs font-medium text-zinc-400 uppercase tracking-wider pb-2 border-b border-zinc-200 text-right pr-2">
                    Y{y.year}
                  </div>
                ))}
                <div className="text-xs font-medium text-[#1B7A8A] uppercase tracking-wider pb-2 border-b border-zinc-200 text-right font-semibold">
                  5-Year
                </div>

                {/* Data rows */}
                {TABLE_ROWS.map((row, ri) => {
                  const stripe = ri % 2 === 0 ? 'bg-zinc-50' : ''
                  const borderTop = row.topBorder ? 'border-t border-zinc-300' : ''
                  return (
                    <Fragment key={row.key}>
                      <div
                        className={`py-1.5 text-sm pr-2 ${
                          row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-500'
                        } ${stripe} ${borderTop}`}
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
                            className={`py-1.5 text-sm text-right pr-2 tabular-nums ${colorClass} ${stripe} ${borderTop}`}
                          >
                            {fmtCell(val, row.format)}
                          </div>
                        )
                      })}
                      {/* 5-Year Total column */}
                      <div
                        className={`py-1.5 text-sm text-right tabular-nums font-semibold ${
                          row.colored
                            ? fiveYearTotal(model.years, row.key) >= 0
                              ? 'text-emerald-600'
                              : 'text-red-500'
                            : row.bold ? 'text-zinc-900' : row.muted ? 'text-zinc-400' : 'text-zinc-700'
                        } ${stripe} ${borderTop}`}
                      >
                        {fmtCell(fiveYearTotal(model.years, row.key), row.format)}
                      </div>
                    </Fragment>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.4 }}
        className="text-[10px] text-zinc-400 font-body mt-2 relative z-10"
      >
        Sources: FPDS FY2024 win rates | USASpending FL contract values | 70% incumbent renewal rate | All inputs adjustable
      </motion.p>
    </div>
  )
}
