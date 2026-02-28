/**
 * Slide registry — 20-slide spine (revised Feb 27, 2026).
 * 17 content slides + 1 economics divider + 2 financial slides.
 */
export const SLIDES = [
  // Act 1: The Anchor
  { id: 'title', label: 'Title', section: null },
  { id: 'executive-summary', label: 'The Opportunity at a Glance', section: null },

  // Act 2: The Market (Florida Only)
  { id: 'why-newport', label: 'Why Newport Wins', section: 'opportunity' },
  { id: 'florida-tam', label: 'Florida TAM by Channel', section: 'opportunity' },
  { id: 'product-matrix', label: 'Product Opportunity', section: 'opportunity' },
  { id: 'confectionery-gap', label: 'The Confectionery Gap', section: 'opportunity' },
  { id: 'target-agencies', label: 'Target Agencies', section: 'opportunity' },
  { id: 'competition', label: 'Competition Landscape', section: 'opportunity' },
  { id: 'b2b-fast-track', label: 'B2B Fast Track', section: 'opportunity' },

  // Act 3: The Strategy
  { id: 'how-it-works', label: 'How It Works', section: 'strategy' },
  { id: 'contract-examples', label: 'Real Contracts', section: 'strategy' },
  { id: 'portfolio-evolution', label: 'Portfolio Evolution', section: 'strategy' },
  { id: 'bd-strategy', label: 'Relationship Strategy', section: 'strategy' },

  // Act 4: Making It Real
  { id: 'risk-compliance', label: 'Risk & Compliance', section: 'execution' },
  { id: 'recommendation', label: 'Our Recommendation', section: 'execution' },
  { id: 'key-questions', label: 'Key Questions', section: 'execution' },
  // Act 5: Economics
  { id: 'divider-economics', label: 'Economics', section: null, isDivider: true },
  { id: 'financial-dashboard', label: 'Financial Dashboard', section: 'economics' },
  { id: 'pro-forma', label: '5-Year Pro Forma', section: 'economics' },

  { id: 'blueprint', label: 'The Blueprint', section: null },
]

export const TOTAL_SLIDES = SLIDES.length
