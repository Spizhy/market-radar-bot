import pytest
from app.services.bot_dispatcher import BotDispatcherService
from app.models.schemas import ThreatAnalysis


def test_telegram_html_formatting():
    dispatcher = BotDispatcherService()
    analyses = [
        ThreatAnalysis(
            competitor_name="AcmeCloud",
            event_title="Slashes prices by 35%",
            strategic_impact_score=4,
            threat_level="HIGH",
            swot_implications="Mid-market risk",
            tactical_recommendation="Bundle premium features"
        )
    ]
    html = dispatcher.format_telegram_html("BRF-TEST", analyses)
    assert "<b>🚨 MARKET RADAR: Executive Briefing</b>" in html
    assert "<b>AcmeCloud</b>" in html
    assert "<i>Bundle premium features</i>" in html or "Bundle premium features" in html


def test_slack_block_kit_formatting():
    dispatcher = BotDispatcherService()
    analyses = [
        ThreatAnalysis(
            competitor_name="DataFlow Systems",
            event_title="Launches AI agent canvas",
            strategic_impact_score=4,
            threat_level="HIGH",
            swot_implications="Direct workflow competition",
            tactical_recommendation="Emphasize SOC2 compliance"
        )
    ]
    slack = dispatcher.format_slack_blocks("BRF-TEST", analyses)
    assert "blocks" in slack
    assert len(slack["blocks"]) >= 3
    assert slack["blocks"][0]["type"] == "header"
