from app.config import settings
from app.providers.base import BaseIntelLLMProvider
from app.providers.mock_provider import MockIntelLLMProvider
from app.providers.openai_provider import OpenAIIntelProvider
from app.providers.gemini_provider import GeminiIntelProvider


def get_intel_provider(override_name: str = None) -> BaseIntelLLMProvider:
    name = (override_name or settings.LLM_PROVIDER).lower()
    if name == "mock":
        return MockIntelLLMProvider()
    elif name == "openai":
        return OpenAIIntelProvider()
    elif name == "gemini":
        return GeminiIntelProvider()
    return MockIntelLLMProvider()
