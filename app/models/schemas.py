from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

EventCategory = Literal[
    "PRICING",
    "FEATURE_LAUNCH",
    "LEADERSHIP",
    "FUNDING",
    "PARTNERSHIP"
]

ThreatLevel = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


class MarketEvent(BaseModel):
    event_id: str
    competitor_name: str
    title: str
    source_url: str
    raw_content: str
    category: EventCategory
    published_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    content_hash: str


class ThreatAnalysis(BaseModel):
    competitor_name: str
    event_title: str
    strategic_impact_score: int = Field(..., ge=1, le=5, description="1 is negligible, 5 is critical threat")
    threat_level: ThreatLevel
    swot_implications: str
    tactical_recommendation: str


class ExecutiveBriefing(BaseModel):
    briefing_id: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    period: str = "Last 24 Hours"
    events_count: int
    analyses: List[ThreatAnalysis]
    executive_summary_markdown: str
    telegram_html: str
    slack_blocks: Dict[str, Any]
    dispatched_status: str = "PENDING"


class ScanRequest(BaseModel):
    competitors: Optional[List[str]] = Field(default=None, description="Optional filter of competitor names to scan")
    force_rescan: bool = Field(default=False, description="Whether to ignore hash deduplication")


class WebhookResponse(BaseModel):
    status: str
    delivered_to: str
    payload_preview: Optional[str] = None
