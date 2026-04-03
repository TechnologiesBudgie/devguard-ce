import os
from devguard.core.config import Config
from devguard.ai.providers import OllamaProvider

class AIEngine:
    def __init__(self, config: Config):
        self.config = config
        self.provider = None
        
        if not config.ai_enabled:
            return

        # Simple Registry/Factory Logic
        provider_type = os.getenv("DEVGUARD_AI_PROVIDER", "ollama").lower()
        
        try:
            if provider_type == "ollama":
                model = os.getenv("OLLAMA_MODEL", "llama3")
                self.provider = OllamaProvider(model)
        except Exception as e:
            print(f"AI Initialization Failed: {e}")

    @property
    def is_ready(self) -> bool:
        return self.provider is not None

    def explain_issue(self, issue) -> str:
        return self.provider.explain(issue) if self.is_ready else "AI not configured."

    def suggest_fix(self, issue) -> str:
        return self.provider.suggest(issue) if self.is_ready else "AI not configured."
