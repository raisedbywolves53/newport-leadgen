import { useState, useMemo, useEffect, useRef, Fragment } from 'react'
import * as echarts from 'echarts/core'
import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import SourceCitation from '../ui/SourceCitation'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import Slider from '../ui/Slider'
import { computeProForma, SLIDER_CONFIGS, SCENARIO_PARAMS } from '../../data/financials'

echarts.use([BarChart, LineChart, GridComponent, TooltipComponent, CanvasRenderer])

const TABLE_ROWS = [
  { key: 'bidsSubmitted',    label: 'Bids Submitted',    bold: false, format: 'number' },
  { key: 'newWins',          label: 'New Wins',          bold: false, format: 'number' },
  { key: 'renewals',         label: 'Renewals',          bold: false, format: 'number' },
  { key: 'activeContracts',  label: 'Active Contracts',  bold: false, format: 'number' },
  { key: 'revenue',          label: 'Revenue',           bold: true,  format: 'currency' },
  { key: 'cogs',             label: 'COGS',              bold: false, format: 'currency' },
  { key: 'grossProfit',      label: 'Gross Profit',      bold: true,  format: 'currency' },
  { key: 'toolCost',         label: 'Tool Costs',        bold: false, format: 'currency' },
  { key: 'adminCost',        label: 'Admin Costs',       bold: false, format: 'currency' },
  { key: 'netIncome',        label: 'Net Income',        bold: true,  format: 'currency', colored: true },
  { key: 'cumulativeRevenue', label: 'Cumulative Rev.',  bold: false, format: 'currency' },
  { key: 'roi',              label: 'ROI',               bold: false, format: 'roi' },
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

export default function ProFormaSlide() {
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

  // Update chart
  useEffect(() => {
    if (!chartInstance.current) return
    const color = SCENARIO_PARAMS[scenario].color

    chartInstance.current.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#18181b',
        borderColor: '#27272a',
        borderWidth: 1,
        textStyle: { color: '#fafafa', fontSize: 11, fontFamily: 'Inter' },
        padding: [6, 10],
        formatter: (params) => {
          let html = `<div style="font-weight:600;margin-bottom:4px">Year ${params[0].axisValue}</div>`
          params.forEach(p => {
            html += `<div style="display:flex;justify-content:space-between;gap:12px;margin:1px 0">
              <span>${p.marker} ${p.seriesName}</span>
              <span style="font-weight:600">$${(Math.abs(p.value) / 1000).toFixed(0)}K</span>
            </div>`
          })
          return html
        },
      },
      grid: { left: 44, right: 8, top: 8, bottom: 24 },
      xAxis: {
        type: 'category',
        data: model.years.map(y => y.year),
        axisLine: { lineStyle: { color: '#e5e5e5' } },
        axisTick: { show: false },
        axisLabel: { color: '#71717a', fontFamily: 'Inter', fontSize: 11 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
        axisLabel: {
          color: '#a1a1aa', fontFamily: 'Inter', fontSize: 10,
          formatter: (v) => {
            if (v === 0) return '0'
            return v >= 1_000_000 || v <= -1_000_000
              ? '$' + (v / 1_000_000).toFixed(1) + 'M'
              : '$' + (v / 1_000).toFixed(0) + 'K'
          },
        },
      },
      series: [
        {
          name: 'Revenue',
          type: 'bar',
          data: model.years.map(y => y.revenue),
          itemStyle: { color: '#1B7A8A', borderRadius: [2, 2, 0, 0] },
          barWidth: 16,
          barGap: '20%',
        },
        {
          name: 'Total Costs',
          type: 'bar',
          data: model.years.map(y => y.cogs + y.toolCost + y.adminCost),
          itemStyle: { color: '#d4d4d8', borderRadius: [2, 2, 0, 0] },
          barWidth: 16,
        },
        {
          name: 'Net Income',
          type: 'line',
          data: model.years.map(y => y.netIncome),
          smooth: true,
          symbol: 'circle',
          symbolSize: 5,
          lineStyle: { color: '#C9A84C', width: 2 },
          itemStyle: { color: '#C9A84C', borderColor: '#fff', borderWidth: 2 },
        },
      ],
    }, true)
  }, [model, scenario])

  return (
    <div className="w-full h-full flex flex-col px-10 lg:px-14 pt-2 pb-14 relative overflow-hidden">
      <BackgroundRing size={500} className="-bottom-40 -left-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-1.5 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-0.5"
        >
          Interactive Model
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950 mb-0.5"
        >
          5-Year Pro Forma
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-sm text-zinc-600"
        >
          Adjust assumptions to model your specific scenario.
        </motion.p>
        <GoldLine width={60} className="mt-1" delay={0.25} />
      </div>

      {/* Controls row */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.4 }}
        className="flex items-start gap-4 mb-2 relative z-10"
      >
        <div className="flex items-center gap-3 shrink-0">
          <RouteToggle active={route} onChange={setRoute} />
          <ScenarioToggle active={scenario} onChange={setScenario} />
        </div>
        <div className="flex-1 grid grid-cols-2 gap-x-4 gap-y-1">
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
      </motion.div>

      {/* Main content: Table + Chart */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="flex gap-2.5 flex-1 min-h-0 relative z-10"
      >
        {/* Table */}
        <div className="w-[60%] rounded-xl bg-white border border-zinc-200 shadow-sm p-3 overflow-auto">
          <div
            className="grid gap-y-0"
            style={{ gridTemplateColumns: '140px repeat(5, 1fr)' }}
          >
            {/* Header row */}
            <div className="text-[10px] font-medium text-zinc-400 uppercase tracking-wider pb-1.5 border-b border-zinc-200" />
            {model.years.map((y) => (
              <div key={y.year} className="text-[10px] font-medium text-zinc-400 uppercase tracking-wider pb-1.5 border-b border-zinc-200 text-right pr-2">
                Year {y.year}
              </div>
            ))}

            {/* Data rows */}
            {TABLE_ROWS.map((row, ri) => (
              <Fragment key={row.key}>
                <div
                  className={`py-1.5 text-[11px] pr-2 truncate ${row.bold ? 'font-semibold text-zinc-900' : 'text-zinc-600'} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
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
                      className={`py-1.5 text-[11px] text-right pr-2 tabular-nums ${colorClass} ${ri % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
                    >
                      {fmtCell(val, row.format)}
                    </div>
                  )
                })}
              </Fragment>
            ))}
          </div>
        </div>

        {/* Chart */}
        <div className="w-[40%] rounded-xl bg-white border border-zinc-200 shadow-sm p-3 flex flex-col min-h-0">
          <span className="font-body text-[10px] font-semibold text-zinc-500 uppercase tracking-wider mb-1 block">
            Revenue vs. Costs
          </span>
          <div ref={chartRef} className="w-full flex-1 min-h-0" />
          {/* Compact legend */}
          <div className="flex items-center gap-3 pt-2 mt-1 border-t border-zinc-100">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-[#1B7A8A]" />
              <span className="text-[10px] text-zinc-500">Revenue</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-zinc-300" />
              <span className="text-[10px] text-zinc-500">Costs</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-[#C9A84C]" />
              <span className="text-[10px] text-zinc-500">Net Income</span>
            </div>
          </div>
        </div>
      </motion.div>

      <SourceCitation>
        Model inputs: FPDS FY2024 competition analysis, USASpending FL food procurement | Renewal: 70% federal incumbent rate | Margin: user-adjustable
      </SourceCitation>
    </div>
  )
}
