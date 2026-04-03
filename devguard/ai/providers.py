from abc import ABC, abstractmethod
from devguard.core.models import Issue

class AIProvider(ABC):
    @abstractmethod
    def explain(self, issue: Issue) -> str:
        pass

    @abstractmethod
    def suggest(self, issue: Issue) -> str:
        pass

class OllamaProvider(AIProvider):
    def __init__(self, model_name: str = "llama3"):
        import ollama
        self.client = ollama
        self.model = model_name

    def explain(self, issue: Issue) -> str:
        response = self.client.chat(model=self.model, messages=[
            {'role': 'user', 'content': f"Explain this security risk: {issue.description}"}
        ])
        return response['message']['content']

    def suggest(self, issue: Issue) -> str:
        response = self.client.chat(model=self.model, messages=[
            {'role': 'user', 'content': f"How do I fix this safely? {issue.snippet}"}
        ])
        return response['message']['content']
