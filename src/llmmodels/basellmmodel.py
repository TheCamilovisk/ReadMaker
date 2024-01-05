from typing import Protocol


class BaseLLMModel(Protocol):
    def generate_readme(self) -> str:
        pass
