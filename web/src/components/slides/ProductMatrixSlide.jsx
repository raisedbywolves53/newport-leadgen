import { useEffect, useRef, useState } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { Star, Shield } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
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

const REVERSED = [...BAR_DATA].reverse() // ECharts draws bottom-up

function tierColor(tier) {
  if (tier === 1) return 'rgba(201,168,76,0.80)'     // gold 80%
  if (tier === 2) return 'rgba(27,122,138,0.70)'      // teal 70%
  return 'rgba(36,51,86,0.15)'                         // navy-800 15%
}

function tierLabel(tier) {
  if (tier === 1) return 'Tier 1 — Highest'
  if (tier === 2) return 'Tier 2 — Growth'
  return 'Avoid'
}

const confectionery = PRODUCT_TIERS.tier1[0]

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
        backgroundColor: 'rgba(36,51,86,0.95)',
        borderColor: 'transparent',
        textStyle: {
          color: '#fff',
          fontFamily: 'Inter, system-ui, sans-serif',
          fontSize: 12,
        },
        formatter: (params) => {
          const p = params[0]
          const d = REVERSED[p.dataIndex]
          if (d.tier === 3) {
            return `<b>${d.name}</b><br/><span style="color:#94A3B8">${d.advantage}</span>`
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
      grid: {
        left: 16,
        right: 90,
        top: 16,
        bottom: 16,
        containLabel: true,
      },
      xAxis: {
        type: 'value',
        show: false,
        splitLine: { show: false },
      },
      yAxis: {
        type: 'category',
        data: REVERSED.map(d => d.name),
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: {
          show: true,
          lineStyle: { color: '#E2E8F0', opacity: 0.3, type: 'dashed' },
        },
        axisLabel: {
          fontSize: 12,
          fontFamily: 'Inter, system-ui, sans-serif',
          color: (value) => {
            const item = BAR_DATA.find(d => d.name === value)
            return item && item.tier === 3 ? '#94A3B8' : '#243356'
          },
        },
      },
      series: [{
        type: 'bar',
        data: REVERSED.map(d => ({
          value: d.flSpend,
          itemStyle: {
            color: tierColor(d.tier),
            borderRadius: [0, 4, 4, 0],
          },
          label: {
            color: d.tier === 1 ? '#C9A84C' : d.tier === 2 ? '#1B7A8A' : 'transparent',
          },
        })),
        barWidth: 18,
        label: {
          show: true,
          position: 'right',
          fontSize: 11,
          fontFamily: 'Inter, system-ui, sans-serif',
          fontWeight: 700,
          formatter: (params) => {
            const d = REVERSED[params.dataIndex]
            return d.tier !== 3 ? fmtM(params.value) : ''
          },
        },
        emphasis: {
          itemStyle: { opacity: 1 },
        },
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
    <div className="w-full h-full flex flex-col justify-center px-16 pt-6 pb-8 relative overflow-hidden">
      <BackgroundRing size={450} className="-top-36 -right-36" opacity={0.03} />
      <BackgroundRing size={280} className="bottom-16 -left-24" opacity={0.025} />

      {/* Header — compact top spacing */}
      <div className="mb-3 relative z-10">
        <motion.span
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="inline-block font-body text-xs font-semibold uppercase tracking-widest text-teal-500 mb-3"
        >
          Product Categories
        </motion.span>
        <motion.h2
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="font-body text-4xl font-bold tracking-tight text-navy-950 mb-2"
        >
          Where Newport Has Pricing Power
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="font-body text-[15px] text-navy-800/60 max-w-2xl"
        >
          Not all products are equal — prioritized by FL demand, competition, and Newport's advantage.
        </motion.p>
        <GoldLine width={60} className="mt-3" delay={0.25} />
      </div>

      {/* Top zone: full-width bar chart card (~55%) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="rounded-2xl bg-white p-5 shadow-[0_2px_8px_rgba(0,0,0,0.06)] border border-black/[0.04] relative z-10 mb-4"
        style={{ height: '340px' }}
      >
        <div className="w-full h-full flex flex-col">
          <div className="flex-1 min-h-0">
            <div ref={chartRef} className="w-full h-full" />
          </div>

          {/* Compact legend below chart */}
          <div className="flex items-center gap-5 pt-2 border-t border-black/[0.06]">
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(201,168,76,0.80)' }} />
              <span className="font-body text-[12px] text-navy-800/50">Tier 1 — Highest</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(27,122,138,0.70)' }} />
              <span className="font-body text-[12px] text-navy-800/50">Tier 2 — Growth</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: 'rgba(36,51,86,0.15)' }} />
              <span className="font-body text-[12px] text-navy-800/50">Avoid</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Bottom zone: two cards side by side (~40%) */}
      <div className="grid grid-cols-2 gap-4 relative z-10">
        {/* Left: Confectionery & Nuts deep dive */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.45 }}
          className="rounded-xl bg-white/70 backdrop-blur-sm border border-black/[0.06] px-6 py-5 flex flex-col justify-center relative overflow-hidden shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        >
          {/* Gold left accent strip */}
          <div className="absolute left-0 top-2 bottom-2 w-[3px] rounded-full" style={{ backgroundColor: '#C9A84C' }} />
          <span
            className="absolute top-3 right-3 text-[11px] font-bold px-1.5 py-0.5 rounded-md"
            style={{ backgroundColor: 'rgba(201,168,76,0.1)', color: '#C9A84C' }}
          >
            HIGHEST FIT
          </span>
          <div className="flex items-start gap-3 pl-2">
            <div
              className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
              style={{ backgroundColor: '#C9A84C15' }}
            >
              <Star className="w-5 h-5" style={{ color: '#C9A84C' }} strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <h3 className="font-body text-base font-semibold text-navy-950 mb-1">
                {confectionery.name}
              </h3>
              <div className="flex items-baseline gap-2 mb-2">
                <span className="font-body text-2xl font-bold tracking-tight leading-none" style={{ color: '#C9A84C' }}>
                  {fmtM(confectionery.nationalSpend)}
                </span>
                <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide">
                  National
                </span>
              </div>
              <div className="space-y-1">
                <p className="font-body text-sm text-navy-800/70">
                  <span className="font-semibold text-navy-950">{confectionery.soleSource}%</span> sole-source — minimal competition
                </p>
                <p className="font-body text-sm text-navy-800/70">
                  Newport's Segment E supplier pricing = built-in cost advantage
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Right: LPTA Evaluation */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.55 }}
          className="rounded-2xl bg-white/80 backdrop-blur-sm px-6 py-5 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] flex flex-col justify-center"
        >
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-lg bg-navy-950/[0.08] flex items-center justify-center shrink-0">
              <Shield className="w-5 h-5 text-navy-800/50" strokeWidth={1.5} />
            </div>
            <div className="flex-1">
              <h3 className="font-body text-base font-semibold text-navy-950 mb-1.5">
                LPTA Evaluation
              </h3>
              <p className="font-body text-sm leading-relaxed text-navy-800/65 mb-2">
                Most food contracts use <span className="font-semibold text-navy-950">Lowest Price Technically Acceptable</span> — directly favors wholesale distributors.
              </p>
              <p className="font-body text-sm leading-relaxed text-navy-800/65">
                Volume purchasing = pricing power. Newport's 30-year supplier relationships are the moat.
              </p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Footer: Avoid items strikethrough + source */}
      <div className="flex items-center justify-between mt-3 relative z-10">
        <div>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="flex items-center gap-3 mb-1"
          >
            <span className="font-body text-[11px] text-navy-800/40">Deprioritized:</span>
            {PRODUCT_TIERS.avoid.map(item => (
              <span key={item.psc} className="font-body text-[11px] text-navy-800/35 line-through">
                {item.name}
              </span>
            ))}
          </motion.div>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="text-[11px] text-navy-800/40"
          >
            FPDS FY2024 by PSC code | USASpending FL awards | FAR 15.101-2 (LPTA evaluation)
          </motion.p>
        </div>
        <CompassStar size={16} opacity={0.2} delay={1.2} />
      </div>
    </div>
  )
}
