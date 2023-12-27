from typing import Dict, List

from langchain.llms.openai import OpenAI
from langchain.prompts import BasePromptTemplate, PromptTemplate

from src.utils.prompt import (
    execute_prompt,
    get_files_structure_text,
    get_files_summaries_text,
)

from .basellmmodel import BaseLLMModel


class DefaultLLMModel(BaseLLMModel):
    def __init__(self):
        self.llm = OpenAI()
        self.file_summary_prompt = self._get_file_summary_prompt()
        self.file_summary_chain = self.file_summary_prompt | self.llm
        self.readme_prompt = self._get_readme_prompt()
        self.readme_chain = self.readme_prompt | self.llm

    def _get_file_summary_prompt(self) -> BasePromptTemplate:
        prompt_template = PromptTemplate(
            input_variables=["file", "file_content"],
            template="Please provide a clear, concise, and objective summary of the following content from '{file}'. The summary should be in formal language, straightforward, and avoid complex vocabulary.\n\n Content to summarize:\n{file_content}",
        )
        return prompt_template

    def _get_readme_prompt(self) -> BasePromptTemplate:
        prompt_template = PromptTemplate(
            input_variables=["file_structure", "files_contents"],
            template="Generate a README.md for a repository with the following features:\n"
            + "\n"
            + "{file_structure}"
            + "\n\n"
            + "{files_contents}"
            + "\n"
            + "The README.md should provide a clear and concise overview of the repository.",
        )
        return prompt_template

    def _get_files_summaries(self, files_contents: Dict[str, str]) -> Dict[str, str]:
        files_summaries = {}
        for file, contents in files_contents.items():
            print(f"Summarizing file: {file}")
            files_summaries[file] = execute_prompt(
                self.file_summary_chain, file=file, file_content=contents
            )
        return files_summaries

    def generate_readme(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        file_structure_text = get_files_structure_text(files_structure)

        files_summaries = self._get_files_summaries(files_contents)
        files_summaries_text = get_files_summaries_text(files_summaries)

        response = execute_prompt(
            self.readme_chain,
            file_structure=file_structure_text,
            files_contents=files_summaries_text,
        )
        return response
