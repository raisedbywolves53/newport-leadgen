import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

// Portfolio mix — showing the shift from micro-heavy to larger deals
// Micros are loss leaders done as fast as possible, but larger deals start Day 1
const data = {
  labels: ['Q1-Q2\nY1', 'Q3-Q4\nY1', 'Y2', 'Y3', 'Y4', 'Y5'],
  micro:      [6,  4,  3,  1,  0,  0],   // Shrinks rapidly
  simplified: [1,  3,  8, 14, 18, 20],   // Grows as past performance builds
  larger:     [0,  1,  3,  7, 14, 22],   // Emerges Y2+, dominates Y4-5
  renewed:    [0,  2,  7, 15, 24, 36],   // Compounds — the flywheel
}

export default function PortfolioEvolutionSlide() {
  const chartRef = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#ffffff',
        borderColor: '#e2e8f0',
        textStyle: { color: '#0F1A2E', fontSize: 12, fontFamily: 'Inter' },
      },
      legend: {
        bottom: 0,
        textStyle: { color: '#475569', fontSize: 11, fontFamily: 'Inter' },
        itemWidth: 12,
        itemHeight: 12,
        itemGap: 20,
      },
      grid: { left: 50, right: 20, top: 10, bottom: 50 },
      xAxis: {
        type: 'category',
        data: data.labels,
        axisLabel: { color: '#475569', fontFamily: 'Inter', fontSize: 11 },
        axisLine: { lineStyle: { color: '#cbd5e1' } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        name: 'Active Contracts',
        nameTextStyle: { color: '#475569', fontSize: 10, fontFamily: 'Inter' },
        axisLabel: { color: '#475569', fontFamily: 'Inter', fontSize: 11 },
        splitLine: { lineStyle: { color: '#e2e8f0', type: 'dashed' } },
        axisLine: { show: false },
      },
      series: [
        {
          name: 'Micro (<$15K)',
          type: 'bar',
          stack: 'portfolio',
          data: data.micro,
          itemStyle: { color: '#3A5080', borderRadius: [0, 0, 0, 0] },
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
    <SlideLayout>
      <SlideTitle>Portfolio Evolution</SlideTitle>
      <SlideSubtitle>
        Micro-purchases are the price of admission — not the destination. The portfolio shifts to larger deals as credibility compounds.
      </SlideSubtitle>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="flex-1 min-h-0"
      >
        <div ref={chartRef} className="w-full h-full min-h-[300px]" />
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="text-xs text-navy-800/50 text-center mt-1"
      >
        The question isn't whether to do micros — it's how quickly we can build enough references to shift the portfolio upward.
        Year 1 is not exclusively micro-purchases. We bid on larger winnable deals from Day 1.
      </motion.p>

      <SourceCitation>
        Win rates: FPDS competition analysis FY2024 | Renewal: ~70% federal recompete incumbent rate (Fed-Spend) | Portfolio mix: modeled estimates
      </SourceCitation>
    </SlideLayout>
  )
}
