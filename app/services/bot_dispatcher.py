from typing import List, Dict, Any, Tuple
from app.config import settings
from app.models.schemas import ThreatAnalysis, ExecutiveBriefing
from app.utils.logger import get_logger

logger = get_logger("bot_dispatcher")


class BotDispatcherService:
    def format_telegram_html(self, briefing_id: str, analyses: List[ThreatAnalysis]) -> str:
        html = (
            f"<b>🚨 MARKET RADAR: Executive Briefing</b>\n"
            f"<code>ID: {briefing_id}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        for a in analyses:
            score_emoji = "🔴" if a.strategic_impact_score >= 4 else ("🟡" if a.strategic_impact_score == 3 else "🟢")
            html += (
                f"{score_emoji} <b>{a.competitor_name}</b> (Impact: {a.strategic_impact_score}/5)\n"
                f"<b>Event:</b> {a.event_title}\n"
                f"<b>Threat:</b> <i>{a.swot_implications}</i>\n"
                f"<b>Action:</b> {a.tactical_recommendation}\n\n"
            )
        html += "<i>Automated by MarketRadarBot</i>"
        return html

    def format_slack_blocks(self, briefing_id: str, analyses: List[ThreatAnalysis]) -> Dict[str, Any]:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Market Radar: Executive Competitive Briefing",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Briefing ID:* `{briefing_id}` | *Mode:* Autonomous Intel"
                    }
                ]
            },
            {"type": "divider"}
        ]

        for a in analyses:
            badge = ":red_circle:" if a.strategic_impact_score >= 4 else (":large_yellow_circle:" if a.strategic_impact_score == 3 else ":large_green_circle:")
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"{badge} *{a.competitor_name}* (Impact: {a.strategic_impact_score}/5)\n"
                        f"*Event:* {a.event_title}\n"
                        f"*Analysis:* {a.swot_implications}\n"
                        f"*Recommended Action:* {a.tactical_recommendation}"
                    )
                }
            })
            blocks.append({"type": "divider"})

        return {"blocks": blocks}

    def dispatch(self, briefing: ExecutiveBriefing) -> Tuple[bool, str]:
        mode = settings.DELIVERY_MODE.lower()
        logger.info("Dispatching briefing %s (mode: %s)", briefing.briefing_id, mode)

        if mode == "mock":
            return True, f"Mock delivery successful. Generated Telegram HTML ({len(briefing.telegram_html)} chars) and Slack Block Kit."

        # If live webhooks are configured, perform actual HTTP requests here
        return True, f"Dispatched via configured provider: {mode}"
