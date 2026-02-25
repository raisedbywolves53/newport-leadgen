import { motion } from 'motion/react'

export default function SourceCitation({ children }) {
  return (
    <motion.p
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.8, duration: 0.4 }}
      className="absolute bottom-4 left-8 right-8 text-[10px] text-navy-800/40 font-body truncate"
    >
      {children}
    </motion.p>
  )
}
