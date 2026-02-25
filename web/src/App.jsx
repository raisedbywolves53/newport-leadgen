import { useState, useCallback } from 'react'
import { useSlideNavigation } from './hooks/useSlideNavigation'
import { SLIDES } from './data/slides'
import PasswordGate from './components/layout/PasswordGate'
import SlideContainer from './components/layout/SlideContainer'
import Navigation from './components/layout/Navigation'
import SectionDivider from './components/ui/SectionDivider'

// Slide components
import TitleSlide from './components/slides/TitleSlide'
import ExecutiveSummarySlide from './components/slides/ExecutiveSummarySlide'
import WhyNewportSlide from './components/slides/WhyNewportSlide'
import FloridaTamSlide from './components/slides/FloridaTamSlide'
import ProductMatrixSlide from './components/slides/ProductMatrixSlide'
import ConfectioneryGapSlide from './components/slides/ConfectioneryGapSlide'
import TargetAgenciesSlide from './components/slides/TargetAgenciesSlide'
import CompetitionSlide from './components/slides/CompetitionSlide'
import B2bFastTrackSlide from './components/slides/B2bFastTrackSlide'
import HowItWorksSlide from './components/slides/HowItWorksSlide'
import ContractExamplesSlide from './components/slides/ContractExamplesSlide'
import PortfolioEvolutionSlide from './components/slides/PortfolioEvolutionSlide'
import BdStrategySlide from './components/slides/BdStrategySlide'
import RiskComplianceSlide from './components/slides/RiskComplianceSlide'
import RecommendationSlide from './components/slides/RecommendationSlide'
import KeyQuestionsSlide from './components/slides/KeyQuestionsSlide'
import BlueprintSlide from './components/slides/BlueprintSlide'
import PlaceholderSlide from './components/slides/PlaceholderSlide'

const SLIDE_COMPONENTS = {
  'title': TitleSlide,
  'executive-summary': ExecutiveSummarySlide,
  'why-newport': WhyNewportSlide,
  'florida-tam': FloridaTamSlide,
  'product-matrix': ProductMatrixSlide,
  'confectionery-gap': ConfectioneryGapSlide,
  'target-agencies': TargetAgenciesSlide,
  'competition': CompetitionSlide,
  'b2b-fast-track': B2bFastTrackSlide,
  'how-it-works': HowItWorksSlide,
  'contract-examples': ContractExamplesSlide,
  'portfolio-evolution': PortfolioEvolutionSlide,
  'bd-strategy': BdStrategySlide,
  'risk-compliance': RiskComplianceSlide,
  'recommendation': RecommendationSlide,
  'key-questions': KeyQuestionsSlide,
  'blueprint': BlueprintSlide,
}

const DIVIDER_CONFIG = {
  'divider-strategy': {
    subtitle: 'How we source, evaluate, and win government contracts',
  },
  'divider-economics': {
    subtitle: 'Five-year financial model with interactive projections',
  },
  'divider-execution': {
    subtitle: 'Risk management, compliance, and next steps',
  },
}

// Light background applied to all slides except title
function SlideBackground({ slideId, children }) {
  if (slideId === 'title') {
    return <>{children}</>
  }
  return (
    <div className="w-full h-full" style={{ backgroundColor: '#e6e6ec' }}>
      {children}
    </div>
  )
}

function renderSlide(slide, index) {
  // Section dividers
  if (slide.isDivider) {
    const config = DIVIDER_CONFIG[slide.id] || {}
    return (
      <SectionDivider
        title={slide.label}
        subtitle={config.subtitle}
        backgroundImage={config.backgroundImage}
      />
    )
  }

  // Built slide components
  const Component = SLIDE_COMPONENTS[slide.id]
  if (Component) {
    return <Component />
  }

  // Placeholder for slides not yet built
  return <PlaceholderSlide title={slide.label} slideNumber={index + 1} />
}

export default function App() {
  const [authenticated, setAuthenticated] = useState(false)
  const { currentSlide, direction, goTo, next, prev, total } = useSlideNavigation()

  const handleClick = useCallback((e) => {
    // Don't advance if clicking on interactive elements
    if (e.target.closest('button') || e.target.closest('a') || e.target.closest('input')) return

    // Click on left third goes back, right two-thirds goes forward
    const rect = e.currentTarget.getBoundingClientRect()
    const clickX = e.clientX - rect.left
    if (clickX < rect.width / 3) {
      prev()
    } else {
      next()
    }
  }, [next, prev])

  if (!authenticated) {
    return <PasswordGate onAuthenticated={() => setAuthenticated(true)} />
  }

  const slide = SLIDES[currentSlide]

  return (
    <div className="w-full h-screen bg-navy-950 overflow-hidden cursor-default select-none">
      <SlideContainer
        slideKey={slide.id}
        direction={direction}
        onClick={handleClick}
      >
        <SlideBackground slideId={slide.id}>
          {renderSlide(slide, currentSlide)}
        </SlideBackground>
      </SlideContainer>

      <Navigation currentSlide={currentSlide} goTo={goTo} />
    </div>
  )
}
