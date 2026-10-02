from typing import List, Dict

MOCK_COMPETITOR_FEED_ITEMS: List[Dict[str, str]] = [
    {
        "competitor_name": "AcmeCloud",
        "title": "AcmeCloud Announces 35% Price Cut Across Enterprise GPU & Serverless Tiers",
        "source_url": "https://acmecloud.example.com/blog/2026-price-reduction",
        "category": "PRICING",
        "published_date": "2026-10-01",
        "content": (
            "AcmeCloud today announced aggressive price reductions of up to 35% on all enterprise serverless compute "
            "and dedicated AI inferencing instances. The company stated this is made possible by new custom ASIC hardware "
            "and aims to capture market share from mid-market cloud providers. Price drops take effect immediately on all monthly invoices."
        )
    },
    {
        "competitor_name": "DataFlow Systems",
        "title": "DataFlow Launches Autonomous Multi-Agent Process Engine with Zero-Code Canvas",
        "source_url": "https://dataflow.example.com/press/autonomous-agent-launch",
        "category": "FEATURE_LAUNCH",
        "published_date": "2026-10-02",
        "content": (
            "DataFlow Systems unveiled its next-generation Multi-Agent Canvas today, allowing non-technical enterprise users "
            "to chain LLM agents directly with ERP and CRM systems. The product features native Slack integration, automatic "
            "error remediation, and SOC2-compliant human-in-the-loop approval gates."
        )
    },
    {
        "competitor_name": "Nova Dynamics",
        "title": "Nova Dynamics Raises $45M Series B Led by Apex Ventures to Expand EU Presence",
        "source_url": "https://techpress.example.com/nova-dynamics-series-b-45m",
        "category": "FUNDING",
        "published_date": "2026-09-30",
        "content": (
            "Automation startup Nova Dynamics announced a $45 million Series B financing round led by Apex Ventures. "
            "The capital will be used to double their engineering headcount in London and Berlin, specifically targeting "
            "enterprise compliance and GDPR-compliant local AI automation solutions."
        )
    }
]
