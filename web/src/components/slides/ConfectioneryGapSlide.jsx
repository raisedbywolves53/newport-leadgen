import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { Candy } from 'lucide-react'
import SlideLayout, { SlideTitle, SlideSubtitle } from '../ui/SlideLayout'
import SourceCitation from '../ui/SourceCitation'
import { useCountUp } from '../../hooks/useCountUp'

echarts.use([PieChart, TooltipComponent, LegendComponent, CanvasRenderer])

export default function ConfectioneryGapSlide() {
  const chartRef = useRef(null)
  const soleSource = useCountUp(58, 1200, 400)
  const awards = useCountUp(45, 1000, 600)

  useEffect(() => {
    if (!chartRef.current) return
    const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })

    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: {
        backgroundColor: '#ffffff',
        borderColor: '#e2e8f0',
        textStyle: { color: '#0F1A2E', fontSize: 12, fontFamily: 'Inter' },
      },
      series: [{
        type: 'pie',
        radius: ['55%', '80%'],
        center: ['50%', '50%'],
        startAngle: 90,
        label: { show: false },
        data: [
          {
            value: 58, name: 'Sole-Source',
            itemStyle: { color: '#E8913A' },
          },
          {
            value: 42, name: 'Competitive',
            itemStyle: { color: '#e2e8f0' },
          },
        ],
        animationDuration: 1200,
        animationEasing: 'cubicOut',
      }],
    })

    const handleResize = () => chart.resize()
    window.addEventListener('resize', handleResize)
    return () => { window.removeEventListener('resize', handleResize); chart.dispose() }
  }, [])

  return (
    <SlideLayout>
      <SlideTitle>Newport's Edge: The Confectionery Gap</SlideTitle>
      <SlideSubtitle>
        PSC 8925 — Newport's Segment E candy expertise meets the most underserved category in government food procurement.
      </SlideSubtitle>

      <div className="grid grid-cols-2 gap-8 flex-1 mt-2">
        {/* Left — The story */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="flex flex-col gap-3"
        >
          {[
            '$55M national spending, $412K in FL alone',
            'Only 45 awards nationally — tiny, fragmented market',
            '58% sole-source — incumbents rarely challenged',
            "Newport's Segment E candy expertise = direct competitive advantage",
            'Existing supplier relationships and wholesale pricing',
            'Few competitors even know this category exists in gov procurement',
          ].map((point, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + i * 0.08, duration: 0.3 }}
              className="flex items-start gap-3"
            >
              <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
              <span className="text-navy-800 text-sm leading-relaxed">{point}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* Right — Chart + stat callouts */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="flex flex-col items-center"
        >
          <div ref={chartRef} className="w-56 h-56" />
          <div className="text-center -mt-2 mb-4">
            <span className="text-amber-400 font-body text-2xl font-bold">{soleSource}%</span>
            <span className="text-navy-800/60 text-sm ml-2">sole-source</span>
          </div>

          <div className="grid grid-cols-2 gap-3 w-full">
            <div className="rounded-lg border border-teal-500/20 bg-teal-500/8 p-3 text-center">
              <span className="text-teal-400 font-body text-2xl font-bold block">{awards}</span>
              <span className="text-navy-800/60 text-xs">National Awards</span>
              <span className="text-navy-800/50 text-[10px] block">Lowest of all food PSCs</span>
            </div>
            <div className="rounded-lg border border-amber-500/20 bg-amber-500/8 p-3 text-center">
              <Candy className="w-5 h-5 text-amber-400 mx-auto mb-1" />
              <span className="text-amber-400 font-semibold text-sm block">Segment E</span>
              <span className="text-navy-800/60 text-xs">Newport core competency</span>
            </div>
          </div>
        </motion.div>
      </div>

      <SourceCitation>
        FPDS FY2024, PSC 8925 (Confectionery & Nuts) | USASpending FL awards
      </SourceCitation>
    </SlideLayout>
  )
}
