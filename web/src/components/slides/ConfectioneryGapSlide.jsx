import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { motion } from 'motion/react'
import { Candy } from 'lucide-react'
import SourceCitation from '../ui/SourceCitation'
import { GoldLine, BackgroundRing } from '../ui/DecorativeElements'
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
        backgroundColor: '#0F1A2E',
        borderColor: '#2E4068',
        borderRadius: 8,
        textStyle: { color: '#F5F6FA', fontSize: 12, fontFamily: 'Inter' },
      },
      series: [{
        type: 'pie',
        radius: ['55%', '80%'],
        center: ['50%', '50%'],
        startAngle: 90,
        label: { show: false },
        data: [
          { value: 58, name: 'Sole-Source', itemStyle: { color: '#E8913A' } },
          { value: 42, name: 'Competitive', itemStyle: { color: '#e2e8f0' } },
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
    <div className="w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 max-w-7xl mx-auto relative overflow-hidden">
      <BackgroundRing size={450} className="-top-32 -right-32" opacity={0.025} color="#E8913A" />

      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.05 }}
        className="font-body text-xs font-semibold uppercase tracking-widest text-amber-500 mb-2"
      >
        Segment E Advantage
      </motion.span>
      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="font-body text-3xl md:text-4xl font-bold tracking-tight text-navy-950 mb-2"
      >
        The Confectionery Gap
      </motion.h2>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="font-body text-base text-navy-800/60 mb-1"
      >
        PSC 8925 — Newport's candy expertise meets the most underserved category in government food procurement.
      </motion.p>
      <GoldLine width={60} className="mb-6" delay={0.25} />

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
              <span className="text-navy-800/70 text-sm leading-relaxed">{point}</span>
            </motion.div>
          ))}
        </motion.div>

        {/* Right — Chart (visual anchor) + stat callouts */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="flex flex-col items-center"
        >
          <div ref={chartRef} className="w-64 h-64" />
          <div className="text-center -mt-2 mb-4">
            <span className="font-body text-3xl font-bold" style={{ color: '#E8913A' }}>{soleSource}%</span>
            <span className="text-navy-800/60 text-sm ml-2">sole-source</span>
          </div>

          <div className="grid grid-cols-2 gap-3 w-full">
            <div className="rounded-xl border border-teal-500/20 bg-teal-500/8 p-3 text-center">
              <span className="text-teal-400 font-body text-2xl font-bold block">{awards}</span>
              <span className="text-navy-800/60 text-xs">National Awards</span>
              <span className="text-navy-800/50 text-[10px] block">Lowest of all food PSCs</span>
            </div>
            <div className="rounded-xl border border-amber-500/20 bg-amber-500/8 p-3 text-center">
              <div className="w-8 h-8 rounded-lg bg-amber-500/15 flex items-center justify-center mx-auto mb-1">
                <Candy className="w-4 h-4 text-amber-400" strokeWidth={1.5} />
              </div>
              <span className="text-amber-400 font-semibold text-sm block">Segment E</span>
              <span className="text-navy-800/60 text-xs">Newport core competency</span>
            </div>
          </div>
        </motion.div>
      </div>

      <SourceCitation>
        FPDS FY2024, PSC 8925 (Confectionery & Nuts) | USASpending FL awards
      </SourceCitation>
    </div>
  )
}
