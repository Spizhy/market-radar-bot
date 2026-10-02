import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["service"] == "market-radar-bot"


def test_trigger_scan_endpoint():
    res = client.post("/api/v1/scan", json={"force_rescan": True})
    assert res.status_code == 200
    briefing = res.json()
    assert briefing["briefing_id"].startswith("BRF-")
    assert briefing["events_count"] >= 1
    assert len(briefing["analyses"]) >= 1


def test_list_and_get_briefings():
    # Trigger a scan first
    client.post("/api/v1/scan", json={"force_rescan": True})

    # List briefings
    res = client.get("/api/v1/briefings")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1

    # Get single briefing
    first_id = items[0]["briefing_id"]
    get_res = client.get(f"/api/v1/briefings/{first_id}")
    assert get_res.status_code == 200
    assert get_res.json()["briefing_id"] == first_id


def test_telegram_webhook():
    payload = {
        "update_id": 10001,
        "message": {
            "message_id": 1,
            "chat": {"id": 12345},
            "text": "/briefing"
        }
    }
    res = client.post("/webhook/telegram", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "Dispatched briefing" in data["payload_preview"]
