import abc
from typing import Dict, List
from langchain.prompts import BasePromptTemplate


class BaseLLMModel(abc.ABC):
    def get_prompt(self) -> BasePromptTemplate:
        pass

    def generate_readme(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        pass
