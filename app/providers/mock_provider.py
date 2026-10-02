from typing import List, Tuple
from app.models.schemas import MarketEvent, ThreatAnalysis
from app.providers.base import BaseIntelLLMProvider


class MockIntelLLMProvider(BaseIntelLLMProvider):
    def analyze_events(self, events: List[MarketEvent]) -> Tuple[List[ThreatAnalysis], str]:
        analyses: List[ThreatAnalysis] = []

        for ev in events:
            cat = ev.category
            comp = ev.competitor_name

            if cat == "PRICING":
                analyses.append(ThreatAnalysis(
                    competitor_name=comp,
                    event_title=ev.title,
                    strategic_impact_score=4,
                    threat_level="HIGH",
                    swot_implications="Strengthens competitor's mid-market cost advantage. Weakens our entry-level pricing pitch.",
                    tactical_recommendation="Review our compute tier margins; launch value-add bundling (e.g. free premium analytics) rather than entering a destructive race to the bottom."
                ))
            elif cat == "FEATURE_LAUNCH":
                analyses.append(ThreatAnalysis(
                    competitor_name=comp,
                    event_title=ev.title,
                    strategic_impact_score=4,
                    threat_level="HIGH",
                    swot_implications="Competitor encroaching on no-code workflow orchestration, lowering technical friction for business teams.",
                    tactical_recommendation="Fast-track developer documentation and highlight our native enterprise compliance guardrails in sales collateral."
                ))
            elif cat == "FUNDING":
                analyses.append(ThreatAnalysis(
                    competitor_name=comp,
                    event_title=ev.title,
                    strategic_impact_score=3,
                    threat_level="MEDIUM",
                    swot_implications="Provides competitor with a 24-month runway to recruit enterprise account executives across Europe.",
                    tactical_recommendation="Secure key EMEA distribution channels and lock in 2-year renewal agreements with high-value European customers."
                ))
            else:
                analyses.append(ThreatAnalysis(
                    competitor_name=comp,
                    event_title=ev.title,
                    strategic_impact_score=2,
                    threat_level="LOW",
                    swot_implications="Standard operational activity with negligible competitive threat.",
                    tactical_recommendation="Continue periodic passive monitoring."
                ))

        # Markdown executive summary
        high_threats = [a for a in analyses if a.strategic_impact_score >= 4]
        summary_md = (
            f"## 🚨 Executive Competitive Radar Briefing\n\n"
            f"**Total Events Analyzed**: {len(events)} | **High-Impact Strategic Threats**: {len(high_threats)}\n\n"
            f"### Key Tactical Takeaways:\n"
        )
        for a in analyses:
            summary_md += (
                f"- **{a.competitor_name}** [{a.threat_level} - Score: {a.strategic_impact_score}/5]: "
                f"{a.event_title}\n"
                f"  - *Impact*: {a.swot_implications}\n"
                f"  - *Action*: {a.tactical_recommendation}\n\n"
            )

        return analyses, summary_md
