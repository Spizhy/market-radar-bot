from abc import ABC, abstractmethod
from typing import List, Tuple
from app.models.schemas import MarketEvent, ThreatAnalysis


class BaseIntelLLMProvider(ABC):
    @abstractmethod
    def analyze_events(self, events: List[MarketEvent]) -> Tuple[List[ThreatAnalysis], str]:
        """Analyze list of market events and generate threat analyses plus an executive Markdown summary."""
        pass
