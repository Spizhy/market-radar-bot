import pytest
from app.services.synthesizer import IntelligenceSynthesizer


def test_run_intelligence_cycle():
    synth = IntelligenceSynthesizer(provider_name="mock")
    briefing = synth.run_intelligence_cycle(force_rescan=True)

    assert briefing.briefing_id.startswith("BRF-")
    assert briefing.events_count >= 1
    assert len(briefing.analyses) >= 1
    assert any(a.competitor_name == "AcmeCloud" for a in briefing.analyses)
    assert any(a.threat_level == "HIGH" for a in briefing.analyses)
    assert "Executive Competitive Radar Briefing" in briefing.executive_summary_markdown
    assert briefing.dispatched_status == "DELIVERED"
