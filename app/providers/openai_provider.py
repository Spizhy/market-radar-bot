import json
from typing import List, Tuple, Optional
import httpx
from app.config import settings
from app.models.schemas import MarketEvent, ThreatAnalysis
from app.providers.base import BaseIntelLLMProvider

SYSTEM_PROMPT = """You are an elite competitive intelligence analyst and executive advisor.
Analyze the provided competitor market announcements.
For each event, evaluate:
- strategic_impact_score (1 to 5)
- threat_level (LOW, MEDIUM, HIGH, CRITICAL)
- swot_implications
- tactical_recommendation
Output strict JSON with a list of threat analyses."""

class OpenAIIntelProvider(BaseIntelLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.LLM_MODEL or "gpt-4o-mini"

    def analyze_events(self, events: List[MarketEvent]) -> Tuple[List[ThreatAnalysis], str]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        events_data = [{"competitor": e.competitor_name, "title": e.title, "content": e.raw_content, "category": e.category} for e in events]
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Competitor Events to evaluate:\n{json.dumps(events_data)}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        with httpx.Client(timeout=30.0) as client:
            res = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            res.raise_for_status()
            data = res.json()
            content = json.loads(data["choices"][0]["message"]["content"])
            analyses_list = content.get("analyses", [])
            analyses = [ThreatAnalysis.model_validate(a) for a in analyses_list]

            summary_md = f"## 🚨 Executive Competitive Radar Briefing\n\nAnalyzed {len(events)} events.\n\n"
            for a in analyses:
                summary_md += f"- **{a.competitor_name}** ({a.threat_level}): {a.tactical_recommendation}\n"
            return analyses, summary_md
