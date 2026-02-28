import { motion } from 'motion/react'

export default function SectionDivider({ title, subtitle, backgroundImage }) {
  return (
    <div className="w-full h-full flex flex-col items-center justify-end pb-24 px-8 relative overflow-hidden">
      {/* Optional background image */}
      {backgroundImage && (
        <div className="absolute inset-0">
          <img
            src={backgroundImage}
            alt=""
            className="w-full h-full object-contain object-center"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#f4f4f5] via-[#f4f4f5]/60 to-[#f4f4f5]/30" />
        </div>
      )}

      {/* Content — sits at bottom so image breathes */}
      <div className="relative z-10 text-center">
        {/* Accent line */}
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: 60 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="h-px rounded-full mx-auto mb-6"
          style={{ backgroundColor: '#C9A84C' }}
        />

        <motion.h2
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="font-body text-4xl md:text-5xl font-bold tracking-tight text-navy-950"
        >
          {title}
        </motion.h2>

        {subtitle && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="mt-3 text-base text-navy-800/60 max-w-lg mx-auto"
          >
            {subtitle}
          </motion.p>
        )}
      </div>
    </div>
  )
}
