import { useSyncExternalStore, useCallback } from 'react'
import { SLIDER_CONFIGS, TOGGLE_CONFIGS } from '../data/financials'

// Module-level singleton state shared across Slide 18 and Slide 19
let state = {
  route: 'free',
  scenario: 'moderate',
  overrides: (() => {
    const o = {}
    SLIDER_CONFIGS.forEach(s => { o[s.key] = s.default })
    TOGGLE_CONFIGS.forEach(t => { o[t.key] = t.default })
    return o
  })(),
}

const listeners = new Set()

function emitChange() {
  for (const l of listeners) l()
}

function subscribe(listener) {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

function getSnapshot() {
  return state
}

export default function useFinancialModel() {
  const current = useSyncExternalStore(subscribe, getSnapshot)

  const setRoute = useCallback((route) => {
    state = { ...state, route }
    emitChange()
  }, [])

  const setScenario = useCallback((scenario) => {
    state = { ...state, scenario }
    emitChange()
  }, [])

  const updateOverride = useCallback((key, value) => {
    state = { ...state, overrides: { ...state.overrides, [key]: value } }
    emitChange()
  }, [])

  return {
    route: current.route,
    scenario: current.scenario,
    overrides: current.overrides,
    setRoute,
    setScenario,
    updateOverride,
  }
}
