/**
 * Slide registry — 20-slide spine (revised Feb 25, 2026).
 * Literary story only — economics/interactive model deferred to Phase 5D.
 */
export const SLIDES = [
  // Act 1: The Anchor
  { id: 'title', label: 'Title', section: null },
  { id: 'executive-summary', label: 'The Opportunity at a Glance', section: null },

  // Act 2: The Market (Florida Only)
  { id: 'divider-opportunity', label: 'The Opportunity', section: 'opportunity', isDivider: true },
  { id: 'why-newport', label: 'Why Newport Wins', section: 'opportunity' },
  { id: 'florida-tam', label: 'Florida TAM by Channel', section: 'opportunity' },
  { id: 'product-matrix', label: 'Product Opportunity', section: 'opportunity' },
  { id: 'confectionery-gap', label: 'The Confectionery Gap', section: 'opportunity' },
  { id: 'target-agencies', label: 'Target Agencies', section: 'opportunity' },
  { id: 'competition', label: 'Competition Landscape', section: 'opportunity' },
  { id: 'b2b-fast-track', label: 'B2B Fast Track', section: 'opportunity' },

  // Act 3: The Strategy
  { id: 'divider-strategy', label: 'The Strategy', section: 'strategy', isDivider: true },
  { id: 'how-it-works', label: 'How It Works', section: 'strategy' },
  { id: 'contract-examples', label: 'Real Contracts', section: 'strategy' },
  { id: 'portfolio-evolution', label: 'Portfolio Evolution', section: 'strategy' },
  { id: 'bd-strategy', label: 'Relationship Strategy', section: 'strategy' },

  // Act 4: Making It Real
  { id: 'divider-execution', label: 'Making It Real', section: 'execution', isDivider: true },
  { id: 'risk-compliance', label: 'Risk & Compliance', section: 'execution' },
  { id: 'recommendation', label: 'Our Recommendation', section: 'execution' },
  { id: 'key-questions', label: 'Key Questions', section: 'execution' },
  { id: 'blueprint', label: 'The Blueprint', section: null },
]

export const TOTAL_SLIDES = SLIDES.length
