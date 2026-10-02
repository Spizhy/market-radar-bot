import json
from typing import List, Tuple, Optional
import httpx
from app.config import settings
from app.models.schemas import MarketEvent, ThreatAnalysis
from app.providers.base import BaseIntelLLMProvider


class GeminiIntelProvider(BaseIntelLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = model or "gemini-1.5-flash"

    def analyze_events(self, events: List[MarketEvent]) -> Tuple[List[ThreatAnalysis], str]:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        events_data = [{"competitor": e.competitor_name, "title": e.title, "content": e.raw_content} for e in events]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        prompt = (
            f"Analyze these competitor events and return JSON with key 'analyses' containing a list matching ThreatAnalysis schema:\n"
            f"{json.dumps(events_data)}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        with httpx.Client(timeout=30.0) as client:
            res = client.post(url, json=payload)
            res.raise_for_status()
            data = res.json()
            content = json.loads(data["candidates"][0]["content"]["parts"][0]["text"])
            analyses_list = content.get("analyses", [])
            analyses = [ThreatAnalysis.model_validate(a) for a in analyses_list]
            summary_md = f"## 🚨 Executive Radar Briefing\n\nAnalyzed {len(events)} events."
            return analyses, summary_md
