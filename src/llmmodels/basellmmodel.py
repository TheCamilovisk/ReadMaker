from typing import Any, Protocol


class BaseLLMModel(Protocol):
    def generate_readme(self, **kwargs: Any) -> str:
        pass
