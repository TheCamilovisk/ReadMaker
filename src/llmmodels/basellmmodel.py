import abc
from typing import Dict, List


class BaseLLMModel(abc.ABCMeta):
    def create_prompt(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        pass

    def generate_readme(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        pass
