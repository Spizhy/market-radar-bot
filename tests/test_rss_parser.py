import pytest
from app.collectors.rss_parser import FeedCollector
from app.models.database import RadarDatabase


def test_content_hashing_and_deduplication(tmp_path):
    test_db = RadarDatabase(db_path=str(tmp_path / "test_radar.sqlite3"))
    collector = FeedCollector(database=test_db)

    # First collect should ingest items
    events1 = collector.collect_events()
    assert len(events1) >= 1

    # Second collect without force should deduplicate and return 0
    events2 = collector.collect_events(force_rescan=False)
    assert len(events2) == 0

    # Collect with force_rescan should re-read
    events3 = collector.collect_events(force_rescan=True)
    assert len(events3) >= 1
