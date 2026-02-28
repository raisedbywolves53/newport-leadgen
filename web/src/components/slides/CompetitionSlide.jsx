import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { TrendingUp, Target, Users } from 'lucide-react'
import { GoldLine, CompassStar } from '../ui/DecorativeElements'
import { COMPETITORS } from '../../data/market'

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])

function fmtM(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

const sorted = [...COMPETITORS].sort((a, b) => b.amount - a.amount)
const reversed = [...sorted].reverse()

function tierBadge(tier) {
  if (tier === 'top')
    return 'bg-amber-50 text-amber-700 border border-amber-200/50'
  if (tier === 'mid')
    return 'bg-teal-50 text-teal-700 border border-teal-200/50'
  return 'bg-zinc-100 text-zinc-600'
}

function tierLabel(tier) {
  if (tier === 'top') return 'National'
  if (tier === 'mid') return 'Regional'
  return 'Entry Tier'
}

export default function CompetitionSlide() {
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
        textStyle: {
          color: '#fafafa',
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 12,
        },
        padding: [8, 12],
        formatter: (params) => {
          const p = params[0]
          const d = reversed[p.dataIndex]
          return `<b>${d.company}</b><br/>FL Gov Awards: <b>${fmtM(d.amount)}</b><br/><span style="color:#a1a1aa">${d.notes}</span>`
        },
      },
      grid: { left: 16, right: 70, top: 8, bottom: 8, containLabel: true },
      xAxis: {
        type: 'value',
        show: false,
        splitLine: { show: false },
      },
      yAxis: {
        type: 'category',
        data: reversed.map((d) => d.company),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: {
          fontSize: 11,
          fontFamily: 'Inter, system-ui, sans-serif',
          color: '#3f3f46',
          width: 160,
          overflow: 'truncate',
        },
      },
      series: [
        {
          type: 'bar',
          data: reversed.map((d) => ({
            value: d.amount,
            itemStyle: {
              color: sorted.indexOf(d) < 3 ? '#C9A84C' : '#1B7A8A',
              borderRadius: [0, 4, 4, 0],
            },
          })),
          barWidth: 20,
          label: {
            show: true,
            position: 'right',
            fontSize: 11,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 600,
            color: '#71717a',
            formatter: (params) => fmtM(params.value),
          },
          emphasis: { itemStyle: { opacity: 1 } },
        },
      ],
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
          Market Position
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.1 }}
          className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2"
        >
          Eight Firms Own Florida
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.35, delay: 0.2 }}
          className="text-sm text-zinc-600 max-w-2xl"
        >
          The top is locked — but Newport enters with more infrastructure than
          anyone in the $1–5M tier.
        </motion.p>
        <GoldLine width={48} className="mt-3" delay={0.25} />
      </div>

      {/* ZONE 2: Stat card row — HORIZONTAL */}
      <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
        {/* $26.1M Top Competitor */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Top Competitor</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-600">
                #1 FL
              </span>
            </div>
            <span
              className="text-2xl font-semibold tabular-nums tracking-tight"
              style={{ color: '#C9A84C' }}
            >
              {fmtM(COMPETITORS[0].amount)}
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              {COMPETITORS[0].company}
            </div>
            <div className="text-zinc-500 text-xs">
              {COMPETITORS[0].notes}
            </div>
          </div>
        </motion.div>

        {/* $1-5M Entry Tier */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.38 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Entry Tier</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-emerald-700">
                <Target className="w-3 h-3" /> ENTRY
              </span>
            </div>
            <span
              className="text-2xl font-semibold tabular-nums tracking-tight"
              style={{ color: '#1B7A8A' }}
            >
              $1–5M
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              Newport's competitive range{' '}
              <TrendingUp className="w-4 h-4" />
            </div>
            <div className="text-zinc-500 text-xs">
              30-year track record, cold chain, Plantation FL
            </div>
          </div>
        </motion.div>

        {/* 8 Competitors */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.46 }}
          className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
        >
          <div className="px-6 flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-500">Active Firms</span>
              <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-600">
                <Users className="w-3 h-3" /> FL FOOD
              </span>
            </div>
            <span className="text-2xl font-semibold tabular-nums tracking-tight text-zinc-950">
              8
            </span>
          </div>
          <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
            <div className="flex items-center gap-2 font-medium text-zinc-900">
              Firms with FL gov food awards
            </div>
            <div className="text-zinc-500 text-xs">
              2 national, 2 regional, 4 entry tier
            </div>
          </div>
        </motion.div>
      </div>

      {/* ZONE 3: Chart card — FULL WIDTH horizontal bar */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col relative overflow-hidden mb-4 relative z-10"
        style={{ height: '260px' }}
      >
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

        <div className="p-6 pb-0 pl-8">
          <h3 className="text-lg font-semibold text-zinc-950">
            FL Food Distributors by Revenue
          </h3>
          <p className="text-sm text-zinc-500 mt-1">Top 8 competitors</p>
        </div>

        <div className="p-6 pt-4 pl-8 flex-1 min-h-0">
          <div ref={chartRef} className="w-full h-full" />
        </div>

        <div className="px-6 py-3 pl-8 border-t border-zinc-100 flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: '#C9A84C' }}
            />
            <span className="text-xs text-zinc-500">Top 3</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{ backgroundColor: '#1B7A8A' }}
            />
            <span className="text-xs text-zinc-500">Entry tier</span>
          </div>
          <span className="text-xs text-zinc-400 ml-auto">
            Newport enters at $1–5M range
          </span>
        </div>
      </motion.div>

      {/* ZONE 4: TableCard — full width */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.4 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm relative z-10"
      >
        <div className="p-6 pb-0">
          <h3 className="text-lg font-semibold text-zinc-950">
            Competitor Breakdown
          </h3>
        </div>

        <div className="p-6 pt-4">
          {/* Header row */}
          <div className="grid grid-cols-[2fr_1fr_1fr_1fr] border-b border-zinc-200 pb-3 mb-1">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
              Company
            </span>
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider text-right">
              FL Gov Revenue
            </span>
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider text-center">
              Segment
            </span>
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider text-right">
              Notes
            </span>
          </div>

          {/* Data rows */}
          {COMPETITORS.map((c, i) => (
            <div
              key={c.rank}
              className={`grid grid-cols-[2fr_1fr_1fr_1fr] py-3 ${i % 2 === 0 ? 'bg-zinc-50/50' : ''}`}
            >
              <span className="text-sm text-zinc-900">{c.company}</span>
              <span className="text-sm text-zinc-600 text-right font-medium">
                {fmtM(c.amount)}
              </span>
              <span className="text-center">
                <span
                  className={`inline-block rounded-md px-2 py-0.5 text-xs font-medium ${tierBadge(c.tier)}`}
                >
                  {tierLabel(c.tier)}
                </span>
              </span>
              <span className="text-sm text-zinc-500 text-right">
                {c.notes}
              </span>
            </div>
          ))}

          {/* Newport callout row */}
          <div className="grid grid-cols-[2fr_1fr_1fr_1fr] py-3 bg-teal-50/50 rounded-lg mt-1">
            <span className="text-sm text-zinc-900 font-semibold">
              Newport Wholesalers
            </span>
            <span
              className="text-sm text-right font-bold"
              style={{ color: '#C9A84C' }}
            >
              $1–5M
            </span>
            <span className="text-center">
              <span className="inline-block bg-amber-50 text-amber-700 border border-amber-200/50 rounded-md px-2 py-0.5 text-xs font-medium">
                Entry
              </span>
            </span>
            <span className="text-sm text-zinc-500 text-right">
              30yr track record · Plantation, FL
            </span>
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
          USASpending API, FY2024 FL food contracts under $350K
        </motion.p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
