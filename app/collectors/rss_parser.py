import hashlib
import uuid
from typing import List, Optional, Dict
from app.models.schemas import MarketEvent
from app.collectors.mock_feeds import MOCK_COMPETITOR_FEED_ITEMS
from app.models.database import db
from app.utils.logger import get_logger

logger = get_logger("rss_parser")


class FeedCollector:
    def __init__(self, database=None):
        self.db = database or db

    def compute_hash(self, competitor: str, title: str, content: str) -> str:
        raw = f"{competitor.strip().lower()}|{title.strip().lower()}|{content.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def collect_events(
        self,
        competitor_filter: Optional[List[str]] = None,
        force_rescan: bool = False
    ) -> List[MarketEvent]:
        events: List[MarketEvent] = []

        for item in MOCK_COMPETITOR_FEED_ITEMS:
            comp_name = item["competitor_name"]
            if competitor_filter and comp_name.lower() not in [c.lower() for c in competitor_filter]:
                continue

            content_hash = self.compute_hash(comp_name, item["title"], item["content"])

            if not force_rescan and self.db.is_hash_seen(content_hash):
                logger.info("Skipping already processed event: %s - %s", comp_name, item["title"])
                continue

            ev = MarketEvent(
                event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
                competitor_name=comp_name,
                title=item["title"],
                source_url=item["source_url"],
                raw_content=item["content"],
                category=item["category"],
                published_date=item["published_date"],
                content_hash=content_hash
            )
            events.append(ev)

            # Record hash in database
            self.db.record_hash(content_hash, comp_name, ev.title)

        logger.info("FeedCollector gathered %d net-new market events.", len(events))
        return events
