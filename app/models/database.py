import os
import sqlite3
import hashlib
from typing import List, Optional, Dict, Any
from app.config import settings
from app.models.schemas import MarketEvent, ExecutiveBriefing
from app.utils.logger import get_logger

logger = get_logger("database")


class RadarDatabase:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.DATABASE_PATH
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS event_hashes (
                    content_hash TEXT PRIMARY KEY,
                    competitor_name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    first_seen TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tracked_competitors (
                    name TEXT PRIMARY KEY,
                    feed_url TEXT,
                    created_at TEXT NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS briefings (
                    briefing_id TEXT PRIMARY KEY,
                    generated_at TEXT NOT NULL,
                    events_count INTEGER NOT NULL,
                    data_json TEXT NOT NULL
                );
            """)
            conn.commit()

    def is_hash_seen(self, content_hash: str) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM event_hashes WHERE content_hash = ?", (content_hash,))
            return cur.fetchone() is not None

    def record_hash(self, content_hash: str, competitor_name: str, title: str):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO event_hashes (content_hash, competitor_name, title, first_seen)
                VALUES (?, ?, ?, datetime('now'));
            """, (content_hash, competitor_name, title))
            conn.commit()

    def save_briefing(self, briefing: ExecutiveBriefing):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO briefings (briefing_id, generated_at, events_count, data_json)
                VALUES (?, ?, ?, ?);
            """, (
                briefing.briefing_id,
                briefing.generated_at,
                briefing.events_count,
                briefing.model_dump_json()
            ))
            conn.commit()

    def get_briefing(self, briefing_id: str) -> Optional[ExecutiveBriefing]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT data_json FROM briefings WHERE briefing_id = ?", (briefing_id,))
            row = cur.fetchone()
            if row:
                return ExecutiveBriefing.model_validate_json(row["data_json"])
            return None

    def list_briefings(self, limit: int = 10) -> List[ExecutiveBriefing]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT data_json FROM briefings ORDER BY generated_at DESC LIMIT ?", (limit,))
            return [ExecutiveBriefing.model_validate_json(r["data_json"]) for r in cur.fetchall()]


db = RadarDatabase()
