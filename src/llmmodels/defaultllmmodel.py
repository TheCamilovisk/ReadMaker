from typing import Dict, List

from src.utils.prompt import get_files_contents_text, get_files_structure_text
from langchain.prompts import PromptTemplate, BasePromptTemplate

from .basellmmodel import BaseLLMModel


class DefaultLLMModel(BaseLLMModel):
    def get_prompt(self) -> BasePromptTemplate:
        prompt_template = PromptTemplate.from_template(
            "Generate a README.md for a repository with the following features:\n"
            + "\n"
            + "{file_structure}"
            + "\n\n"
            + "{files_contents}"
            + "\n"
            + "The README.md should provide a clear and concise overview of the repository."
            + "\n"
            + "The output must be in markdown code only."
        )
        return prompt_template

    def generate_readme(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        return super().generate_readme(files_structure, files_contents)
