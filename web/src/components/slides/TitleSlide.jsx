import { motion } from 'motion/react'

export default function TitleSlide() {
  return (
    <div className="w-full h-full relative overflow-hidden">
      {/* Background image — heavy overlay, barely visible */}
      <div className="absolute inset-0">
        <img
          src="/newport_background.jpg"
          alt=""
          className="w-full h-full object-cover object-bottom"
        />
        <div className="absolute inset-0 bg-navy-950/80" />
      </div>

      {/* Content — left-aligned, shifted below center so logo leads into text */}
      <div className="relative z-10 h-full flex flex-col justify-center px-16">
        {/* Main title — large, bold, dominant */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          className="font-body text-7xl md:text-9xl font-bold leading-none tracking-tight text-white"
        >
          Government
          <br />
          Contracting
        </motion.h1>

        {/* Subtitle line */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="font-body text-base font-normal tracking-[0.2em] uppercase mt-8"
          style={{ color: '#B0B4B8' }}
        >
          30 Years of Wholesale Distribution
        </motion.p>

        {/* "Opportunity" — champagne gold accent */}
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.9 }}
          className="font-body text-4xl md:text-5xl font-bold tracking-tight mt-4"
          style={{ color: '#C9A84C' }}
        >
          Opportunity
        </motion.h2>

        {/* Footer credit */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 1.2 }}
          className="font-body text-sm uppercase tracking-[0.2em] mt-8"
          style={{ color: '#9CA0A4' }}
        >
          Prepared by Still Mind Creative &nbsp;&middot;&nbsp; February 2026
        </motion.p>
      </div>
    </div>
  )
}
