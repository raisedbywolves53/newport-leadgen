import { useMemo, useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, MarkLineComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { DollarSign, TrendingUp, Calendar, AlertTriangle } from 'lucide-react'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import RouteToggle from '../ui/RouteToggle'
import ScenarioToggle from '../ui/ScenarioToggle'
import Slider from '../ui/Slider'
import AnimatedNumber from '../ui/AnimatedNumber'
import useFinancialModel from '../../hooks/useFinancialModel'
import { computeProForma, computeCashFlow } from '../../data/financials'

echarts.use([LineChart, GridComponent, TooltipComponent, MarkLineComponent, CanvasRenderer])

function fmtCompact(v) {
  const abs = Math.abs(v)
  const sign = v < 0 ? '-' : ''
  if (abs >= 1_000_000) return sign + '$' + (abs / 1_000_000).toFixed(1) + 'M'
  if (abs >= 1_000) return sign + '$' + (abs / 1_000).toFixed(0) + 'K'
  return sign + '$' + abs.toLocaleString('en-US')
}

const KPI_DEFS = [
  { key: 'peakDeficit', label: 'Peak Cash Deficit', icon: AlertTriangle, format: 'compact' },
  { key: 'paybackYear', label: 'Payback Period', icon: Calendar, format: 'year' },
  { key: 'fiveYearFCF', label: '5-Year Cumul. FCF', icon: DollarSign, format: 'compact' },
  { key: 'fiveYearROI', label: '5-Year ROI', icon: TrendingUp, format: 'pct' },
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

  const kpiValues = useMemo(() => ({
    peakDeficit: cashFlow.peakDeficit,
    paybackYear: model.summary.paybackYear,
    fiveYearFCF: model.summary.totalReturn,
    fiveYearROI: model.summary.fiveYearROI,
  }), [cashFlow, model])

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

  // Update chart — dual-line cumulative owner economics
  useEffect(() => {
    if (!chartInstance.current) return

    const investmentData = model.summary.cumulativeInvestment
    const incomeData = model.summary.cumulativeNetIncome

    // Find crossover year index (where cumulative income exceeds cumulative investment)
    let crossoverIdx = -1
    for (let i = 0; i < 5; i++) {
      if (incomeData[i] >= 0) {
        crossoverIdx = i
        break
      }
    }

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
          const yr = params[0].dataIndex + 1
          let html = `<div style="font-weight:600;margin-bottom:6px;font-size:13px">Year ${yr}</div>`
          params.forEach(p => {
            html += `<div style="display:flex;justify-content:space-between;gap:20px;margin:2px 0">
              <span><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${p.color};margin-right:6px"></span>${p.seriesName}</span>
              <span style="font-weight:600">${fmtCompact(p.value)}</span>
            </div>`
          })
          const cf = cashFlow.years[params[0].dataIndex]
          html += `<div style="border-top:1px solid #3f3f46;margin-top:6px;padding-top:6px;font-size:11px;color:#a1a1aa">`
          html += `Net Cash Flow: <span style="color:${cf.netCashFlow >= 0 ? '#10b981' : '#ef4444'};font-weight:600">${fmtCompact(cf.netCashFlow)}</span>`
          html += `<div style="margin-top:2px">Blended DSO: ${cf.blendedDSO}d | COGS Float: ${fmtCompact(cf.cogsFloat)}</div>`
          html += `</div>`
          return html
        },
      },
      grid: { left: 56, right: 16, top: 16, bottom: 28 },
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
      series: [
        {
          name: 'Cumul. Investment',
          type: 'line',
          data: investmentData,
          smooth: true,
          symbol: 'circle',
          symbolSize: 4,
          lineStyle: { width: 2, color: '#71717a', type: 'dashed' },
          itemStyle: { color: '#71717a' },
          z: 1,
        },
        {
          name: 'Cumul. Net Income',
          type: 'line',
          data: incomeData,
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: { width: 3, color: '#1B7A8A' },
          itemStyle: { color: '#1B7A8A' },
          areaStyle: {
            color: {
              type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(201,168,76,0.25)' },
                { offset: 1, color: 'rgba(201,168,76,0.02)' },
              ],
            },
          },
          markLine: crossoverIdx >= 0 ? {
            silent: true,
            symbol: 'none',
            lineStyle: { color: '#C9A84C', type: 'dashed', width: 1 },
            data: [{ xAxis: crossoverIdx }],
            label: {
              formatter: 'Payback',
              position: 'insideStartTop',
              color: '#C9A84C',
              fontSize: 10,
              fontFamily: 'Inter, system-ui, sans-serif',
            },
          } : undefined,
          z: 10,
        },
      ],
    }, true)
  }, [model, cashFlow])

  // Working capital constraint indicator
  const wcRequired = Math.max(...cashFlow.years.map(y => Math.abs(y.cogsFloat)))
  const wcRatio = workingCapital > 0 ? wcRequired / workingCapital : 999
  const wcStatus = wcRatio <= 0.6 ? 'green' : wcRatio <= 1.0 ? 'yellow' : 'red'
  const wcColors = { green: '#10b981', yellow: '#eab308', red: '#ef4444' }

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
          Cash Flow Analysis
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-2xl font-semibold tracking-tight text-zinc-950"
        >
          Cash Flow & Owner Returns
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
          <Slider
            label="Available WC"
            value={workingCapital}
            onChange={setWorkingCapital}
            min={0}
            max={500000}
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
                <span className="text-zinc-500">Required</span>
                <span className="font-semibold text-zinc-800 tabular-nums">{fmtCompact(wcRequired)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-zinc-500">Available</span>
                <span className="font-semibold text-zinc-800 tabular-nums">{fmtCompact(workingCapital)}</span>
              </div>
              {/* Bar indicator */}
              <div className="h-2 rounded-full bg-zinc-100 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${Math.min(wcRatio * 100, 100)}%`,
                    backgroundColor: wcColors[wcStatus],
                  }}
                />
              </div>
              <span className="text-[10px] font-medium" style={{ color: wcColors[wcStatus] }}>
                {wcStatus === 'green' ? 'Sufficient' : wcStatus === 'yellow' ? 'Tight' : 'Constrained'}
              </span>
            </div>
          </div>

          {/* Cash flow year summary */}
          <div className="border-t border-zinc-100 pt-3">
            <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-2">
              Annual Cash Flow
            </div>
            <div className="flex flex-col gap-1.5">
              {cashFlow.years.map(y => (
                <div key={y.year} className="flex justify-between text-xs">
                  <span className="text-zinc-500">Y{y.year}</span>
                  <span className={`font-semibold tabular-nums ${y.netCashFlow >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                    {fmtCompact(y.netCashFlow)}
                  </span>
                </div>
              ))}
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

              if (kpi.key === 'peakDeficit') {
                accent = val < 0 ? '#ef4444' : '#10b981'
                borderClass = val < 0 ? 'border-red-300' : 'border-emerald-300'
              }
              if (kpi.key === 'fiveYearFCF') {
                accent = val >= 0 ? '#C9A84C' : '#ef4444'
                borderClass = val >= 0 ? 'border-zinc-200' : 'border-red-300'
              }
              if (kpi.key === 'fiveYearROI') {
                accent = val >= 0 ? '#C9A84C' : '#ef4444'
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
                  ) : kpi.format === 'pct' ? (
                    <span
                      className="font-body text-2xl font-semibold tracking-tight leading-none block tabular-nums"
                      style={{ color: accent }}
                    >
                      {(val * 100).toFixed(0)}%
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

          {/* Chart — Cumulative Owner Economics */}
          <div className="flex-1 rounded-xl bg-white border border-zinc-200 shadow-sm p-4 flex flex-col min-h-0">
            <div className="flex items-center justify-between mb-2">
              <span className="font-body text-xs font-semibold text-zinc-500 uppercase tracking-wider">
                Cumulative Owner Economics
              </span>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1.5">
                  <div className="w-4 h-0.5 border-t-2 border-dashed border-zinc-400" />
                  <span className="text-xs text-zinc-500">Investment</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="w-4 h-0.5 bg-[#1B7A8A] rounded" />
                  <span className="text-xs text-zinc-500">Net Income</span>
                </div>
              </div>
            </div>
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
        Sources: FPDS FY2024 | Prompt Payment Act DSO (FAR 52.232-25) | SLED 30-45d terms | Working capital based on COGS float
      </motion.p>
    </div>
  )
}
