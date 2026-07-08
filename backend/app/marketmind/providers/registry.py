from app.marketmind.providers.mock_provider import MockProvider
from app.marketmind.providers.openai_provider import OpenAIProvider
from app.marketmind.providers.anthropic_provider import AnthropicProvider
from app.marketmind.providers.google_provider import GoogleProvider

class ProviderRegistry:
    def __init__(self):
        self.providers = {
            "mock": MockProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleProvider(),
        }

    def available(self):
        return {name: provider.available() for name, provider in self.providers.items()}

    def get(self, name: str):
        provider = self.providers.get(name)
        if provider and provider.available():
            return provider
        return self.providers["mock"]

provider_registry = ProviderRegistry()
