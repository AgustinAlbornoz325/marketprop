import os
from dotenv import load_dotenv
from app.marketmind.providers.mock_provider import MockProvider
from app.marketmind.providers.openai_provider import OpenAIProvider
from app.marketmind.providers.anthropic_provider import AnthropicProvider
from app.marketmind.providers.google_provider import GoogleProvider
load_dotenv()
class ProviderRegistry:
    def __init__(self): self.providers={"mock":MockProvider(),"openai":OpenAIProvider(),"anthropic":AnthropicProvider(),"google":GoogleProvider()}
    def demo_mode(self): return os.getenv("DEMO_MODE","true").lower()=="true"
    def available(self): return {n:p.available() for n,p in self.providers.items()}
    def status(self): return {n:{"available":p.available(),"active":(not self.demo_mode() and p.available()) or n=="mock"} for n,p in self.providers.items()}
    def get(self,name):
        if self.demo_mode(): return self.providers["mock"]
        p=self.providers.get(name)
        return p if p and p.available() else self.providers["mock"]
provider_registry=ProviderRegistry()


# Compatibility alias used by api.routes
registry = provider_registry
