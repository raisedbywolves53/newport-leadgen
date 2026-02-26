import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
import { useCountUp } from '../../hooks/useCountUp'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const data = {
  labels: ['Q1-Q2\nY1', 'Q3-Q4\nY1', 'Y2', 'Y3', 'Y4', 'Y5'],
  micro:      [6,  4,  3,  1,  0,  0],
  simplified: [1,  3,  8, 14, 18, 20],
  larger:     [0,  1,  3,  7, 14, 22],
  renewed:    [0,  2,  7, 15, 24, 36],
}

export default function PortfolioEvolutionSlide() {
  const chartRef = useRef(null)
  const y5Total = useCountUp(78, 1200, 500)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#0F1A2E',
        borderColor: '#2E4068',
        borderRadius: 8,
        textStyle: { color: '#F5F6FA', fontSize: 12, fontFamily: 'Inter' },
      },
      legend: {
        bottom: 0,
        textStyle: { color: '#64748B', fontSize: 11, fontFamily: 'Inter' },
        itemWidth: 12,
        itemHeight: 12,
        itemGap: 20,
      },
      grid: { left: 50, right: 20, top: 10, bottom: 50 },
      xAxis: {
        type: 'category',
        data: data.labels,
        axisLabel: { color: '#94A3B8', fontFamily: 'Inter', fontSize: 11 },
        axisLine: { lineStyle: { color: '#cbd5e1' } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        name: 'Active Contracts',
        nameTextStyle: { color: '#94A3B8', fontSize: 10, fontFamily: 'Inter' },
        axisLabel: { color: '#94A3B8', fontFamily: 'Inter', fontSize: 11 },
        splitLine: { lineStyle: { color: '#0F1A2E', opacity: 0.06 } },
        axisLine: { show: false },
      },
      series: [
        {
          name: 'Micro (<$15K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.micro,
          itemStyle: { color: '#3A5080' },
          animationDuration: 800,
          animationDelay: (i) => i * 100,
        },
        {
          name: 'Simplified ($15-350K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.simplified,
          itemStyle: { color: '#1B7A8A' },
          animationDuration: 800,
          animationDelay: (i) => i * 100 + 200,
        },
        {
          name: 'Larger (>$100K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.larger,
          itemStyle: { color: '#239BAD' },
          animationDuration: 800,
          animationDelay: (i) => i * 100 + 400,
        },
        {
          name: 'Renewed (70%)',
          type: 'bar',
          stack: 'portfolio',
          data: data.renewed,
          itemStyle: { color: '#E8913A', borderRadius: [3, 3, 0, 0] },
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
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 max-w-7xl mx-auto relative overflow-hidden">
      <BackgroundRing size={500} className="-top-40 -right-40" opacity={0.02} />

      {/* Hero stat + heading */}
      <div className="flex items-end gap-6 mb-2 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="shrink-0"
        >
          <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide block mb-1">
            Year 5 Active
          </span>
          <span className="font-body text-6xl md:text-7xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
            {y5Total}
          </span>
          <span className="font-body text-sm font-medium text-navy-800/35 uppercase tracking-wide ml-1">
            Contracts
          </span>
        </motion.div>

        <div className="pb-2">
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.15 }}
            className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-1"
          >
            Portfolio Evolution
          </motion.h2>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.25 }}
            className="font-body text-base text-navy-800/60"
          >
            Micro-purchases are the price of admission — not the destination.
          </motion.p>
        </div>
      </div>

      <GoldLine width={60} className="mb-4" delay={0.3} />

      {/* Chart — the visual anchor */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.35, duration: 0.5 }}
        className="flex-1 min-h-0 relative z-10"
      >
        <div ref={chartRef} className="w-full h-full min-h-[300px]" />
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="text-xs text-navy-800/50 text-center mt-1 relative z-10"
      >
        Year 1 is not exclusively micro-purchases. We bid on larger winnable deals from Day 1.
      </motion.p>

      <SourceCitation>
        Win rates: FPDS competition analysis FY2024 | Renewal: ~70% federal recompete incumbent rate (Fed-Spend) | Portfolio mix: modeled estimates
      </SourceCitation>
    </div>
  )
}
