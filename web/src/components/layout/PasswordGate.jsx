import { useState } from 'react'
import { motion } from 'motion/react'
import { Lock, ArrowRight } from 'lucide-react'

const GATE_PASSWORD = import.meta.env.VITE_SITE_PASSWORD || 'newport2026'

export default function PasswordGate({ onAuthenticated }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)
  const [shaking, setShaking] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (password === GATE_PASSWORD) {
      onAuthenticated()
    } else {
      setError(true)
      setShaking(true)
      setTimeout(() => setShaking(false), 500)
      setTimeout(() => setError(false), 3000)
    }
  }

  return (
    <div className="fixed inset-0 bg-navy-950 flex items-center justify-center">
      {/* Subtle gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-navy-900/50 via-transparent to-teal-500/5" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="relative z-10 w-full max-w-md px-8"
      >
        {/* Branding */}
        <div className="text-center mb-10">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-navy-800 border border-navy-700 mb-6"
          >
            <Lock className="w-7 h-7 text-teal-500" />
          </motion.div>
          <h1 className="font-body text-3xl font-bold tracking-tight text-white mb-2">
            Confidential Presentation
          </h1>
          <p className="text-slate-400 text-sm">
            Prepared by Still Mind Creative LLC
          </p>
        </div>

        {/* Password form */}
        <motion.form
          onSubmit={handleSubmit}
          animate={shaking ? { x: [0, -10, 10, -10, 10, 0] } : {}}
          transition={{ duration: 0.4 }}
        >
          <div className="relative">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter access code"
              autoFocus
              className={`
                w-full px-5 py-4 rounded-xl bg-navy-900 border text-offwhite
                placeholder:text-slate-500 text-base font-body
                focus:outline-none focus:ring-2 focus:ring-teal-500/50 focus:border-teal-500
                transition-colors duration-200
                ${error ? 'border-red-500/70' : 'border-navy-700'}
              `}
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 rounded-lg bg-teal-500 hover:bg-teal-400 text-navy-950 transition-colors cursor-pointer"
            >
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>

          {error && (
            <motion.p
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-3 text-sm text-red-400 text-center"
            >
              Invalid access code. Please try again.
            </motion.p>
          )}
        </motion.form>

        {/* Footer */}
        <p className="mt-12 text-center text-xs text-slate-500">
          Newport Wholesalers &mdash; Government Contracting Opportunity
        </p>
      </motion.div>
    </div>
  )
}
