from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import (
    ExecutiveBriefing,
    ScanRequest,
    WebhookResponse
)
from app.models.database import db
from app.services.synthesizer import IntelligenceSynthesizer
from app.utils.logger import get_logger

logger = get_logger("main")

app = FastAPI(
    title="MarketRadar Bot API",
    description="Automated B2B Competitive Intelligence & Multi-Platform Executive Briefing Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

synthesizer = IntelligenceSynthesizer()


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "market-radar-bot",
        "provider": settings.LLM_PROVIDER,
        "delivery_mode": settings.DELIVERY_MODE
    }


# Intelligence Scan & Briefings Endpoints
@app.post("/api/v1/scan", response_model=ExecutiveBriefing, tags=["Intelligence"])
def trigger_scan(req: Optional[ScanRequest] = None):
    competitors = req.competitors if req else None
    force = req.force_rescan if req else False
    briefing = synthesizer.run_intelligence_cycle(
        competitor_filter=competitors,
        force_rescan=force
    )
    return briefing


@app.get("/api/v1/briefings", response_model=List[ExecutiveBriefing], tags=["Intelligence"])
def list_briefings(limit: int = Query(10, ge=1, le=50)):
    return db.list_briefings(limit=limit)


@app.get("/api/v1/briefings/{briefing_id}", response_model=ExecutiveBriefing, tags=["Intelligence"])
def get_briefing(briefing_id: str):
    brf = db.get_briefing(briefing_id)
    if not brf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Briefing '{briefing_id}' not found."
        )
    return brf


# Multi-Platform Bot Webhook Handlers
@app.post("/webhook/telegram", response_model=WebhookResponse, tags=["Webhooks"])
async def telegram_webhook(request: Request):
    """Handles incoming Telegram bot updates & slash commands (/briefing, /status, /track)."""
    payload = await request.json()
    logger.info("Received Telegram webhook update")

    message = payload.get("message", {})
    text = (message.get("text") or "").strip()
    chat_id = message.get("chat", {}).get("id", "default_chat")

    if text.startswith("/briefing"):
        briefing = synthesizer.run_intelligence_cycle(force_rescan=True)
        return WebhookResponse(
            status="success",
            delivered_to=str(chat_id),
            payload_preview=f"Dispatched briefing {briefing.briefing_id} ({briefing.events_count} events)"
        )
    elif text.startswith("/status"):
        briefings = db.list_briefings(limit=1)
        latest_id = briefings[0].briefing_id if briefings else "None"
        return WebhookResponse(
            status="active",
            delivered_to=str(chat_id),
            payload_preview=f"Radar Bot is active. Latest briefing: {latest_id}"
        )
    else:
        return WebhookResponse(
            status="acknowledged",
            delivered_to=str(chat_id),
            payload_preview="Command acknowledged. Use /briefing to trigger a strategic report."
        )


@app.post("/webhook/slack", tags=["Webhooks"])
async def slack_webhook(request: Request):
    """Handles incoming Slack slash commands (/radar-briefing)."""
    # Slack sends application/x-www-form-urlencoded or json
    try:
        form = await request.form()
        text = form.get("text", "")
    except Exception:
        text = ""

    briefing = synthesizer.run_intelligence_cycle(force_rescan=True)
    return {
        "response_type": "in_channel",
        "text": f"🚨 *Executive Market Radar Briefing: {briefing.briefing_id}*",
        "blocks": briefing.slack_blocks.get("blocks", [])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
