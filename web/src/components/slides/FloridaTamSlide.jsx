import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { FL_TAM_CHANNELS } from '../../data/market'

echarts.use([BarChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

function fmtDollars(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`
  return `$${n}`
}

export default function FloridaTamSlide() {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })
    chartInstance.current = chart

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: '#1A2744',
        borderColor: '#2E4068',
        textStyle: { color: '#F5F6FA', fontSize: 12, fontFamily: 'Inter' },
        formatter: (params) => {
          const d = params[0]
          const ch = FL_TAM_CHANNELS[d.dataIndex]
          return `<strong>${ch.channel}</strong><br/>${ch.amountLabel || fmtDollars(ch.amount)}<br/><span style="color:#94A3B8;font-size:11px">${ch.description}</span>`
        },
      },
      grid: { left: 200, right: 60, top: 10, bottom: 30 },
      xAxis: {
        type: 'value',
        axisLabel: {
          formatter: (v) => fmtDollars(v),
          color: '#64748B',
          fontFamily: 'Inter',
          fontSize: 11,
        },
        splitLine: { lineStyle: { color: '#243356', type: 'dashed' } },
        axisLine: { show: false },
      },
      yAxis: {
        type: 'category',
        data: FL_TAM_CHANNELS.map(c => c.channel).reverse(),
        axisLabel: {
          color: '#CBD5E1',
          fontFamily: 'Inter',
          fontSize: 12,
          width: 180,
          overflow: 'truncate',
        },
        axisLine: { show: false },
        axisTick: { show: false },
      },
      series: [{
        type: 'bar',
        data: FL_TAM_CHANNELS.map(c => c.amount).reverse(),
        barWidth: 28,
        itemStyle: {
          borderRadius: [0, 4, 4, 0],
          color: (params) => {
            const colors = ['#3A5080', '#E8913A', '#239BAD', '#1B7A8A', '#1B7A8A']
            return colors.reverse()[params.dataIndex]
          },
        },
        label: {
          show: true,
          position: 'right',
          formatter: (p) => {
            const ch = FL_TAM_CHANNELS[FL_TAM_CHANNELS.length - 1 - p.dataIndex]
            return ch.amountLabel || fmtDollars(ch.amount)
          },
          color: '#F5F6FA',
          fontFamily: 'Inter',
          fontSize: 12,
          fontWeight: 600,
        },
        animationDuration: 1200,
        animationEasing: 'cubicOut',
        animationDelay: (idx) => idx * 150,
      }],
    }

    chart.setOption(option)

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      chart.dispose()
    }
  }, [])

  return (
    <SlideLayout>
      <SlideTitle>Florida TAM by Procurement Channel</SlideTitle>
      <SlideSubtitle>
        $87M in federal food contracts alone — state, education, and local are additive.
      </SlideSubtitle>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
        className="flex-1 min-h-0"
      >
        <div ref={chartRef} className="w-full h-full min-h-[320px]" />
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
        className="text-xs text-slate-500 mt-2 text-center"
      >
        Geographic expansion beyond FL depends on Newport's delivery capabilities — a key question for ownership.
      </motion.p>

      <SourceCitation>
        Federal: USASpending API FY2024 (Feb 2026) | State: FL MFMP | Education: FL DOE 2024-25, USDA NSLP FY2024 | Local: County procurement data
      </SourceCitation>
    </SlideLayout>
  )
}
