import { AnimatePresence, motion } from 'motion/react'

const variants = {
  enter: (direction) => ({
    x: direction > 0 ? '8%' : '-8%',
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
  },
  exit: (direction) => ({
    x: direction > 0 ? '-8%' : '8%',
    opacity: 0,
  }),
}

export default function SlideContainer({ slideKey, direction, children, onClick }) {
  return (
    <div
      className="relative w-full h-full overflow-hidden"
      onClick={onClick}
    >
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={slideKey}
          custom={direction}
          variants={variants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{ duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }}
          className="absolute inset-0 flex items-center justify-center"
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </div>
  )
}
