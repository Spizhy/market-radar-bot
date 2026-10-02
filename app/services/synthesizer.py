import uuid
from typing import Optional, List
from app.models.schemas import ExecutiveBriefing, MarketEvent, ThreatAnalysis
from app.collectors.rss_parser import FeedCollector
from app.providers import get_intel_provider
from app.services.bot_dispatcher import BotDispatcherService
from app.models.database import db
from app.utils.logger import get_logger

logger = get_logger("synthesizer")


class IntelligenceSynthesizer:
    def __init__(self, provider_name: Optional[str] = None):
        self.collector = FeedCollector()
        self.provider = get_intel_provider(provider_name)
        self.dispatcher = BotDispatcherService()

    def run_intelligence_cycle(
        self,
        competitor_filter: Optional[List[str]] = None,
        force_rescan: bool = False
    ) -> ExecutiveBriefing:
        briefing_id = f"BRF-{uuid.uuid4().hex[:8].upper()}"
        logger.info("Starting intelligence cycle: %s", briefing_id)

        # 1. Collect events
        events: List[MarketEvent] = self.collector.collect_events(
            competitor_filter=competitor_filter,
            force_rescan=force_rescan
        )

        if not events:
            # If no net-new events, force re-collecting sample items for continuous demonstration
            events = self.collector.collect_events(competitor_filter=competitor_filter, force_rescan=True)

        # 2. AI Threat & Strategy Analysis
        analyses, summary_md = self.provider.analyze_events(events)

        # 3. Format Multi-Platform Bot Payloads
        tg_html = self.dispatcher.format_telegram_html(briefing_id, analyses)
        slack_blocks = self.dispatcher.format_slack_blocks(briefing_id, analyses)

        # 4. Construct Briefing
        briefing = ExecutiveBriefing(
            briefing_id=briefing_id,
            events_count=len(events),
            analyses=analyses,
            executive_summary_markdown=summary_md,
            telegram_html=tg_html,
            slack_blocks=slack_blocks,
            dispatched_status="PENDING"
        )

        # 5. Dispatch
        success, dispatch_notes = self.dispatcher.dispatch(briefing)
        briefing.dispatched_status = "DELIVERED" if success else "FAILED"

        # 6. Save in SQLite
        db.save_briefing(briefing)
        logger.info("Intelligence cycle %s completed with status: %s", briefing_id, briefing.dispatched_status)
        return briefing
