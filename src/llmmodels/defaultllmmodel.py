from typing import Dict, List

from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import BasePromptTemplate, PromptTemplate

from src.utils.prompt import (
    execute_prompt,
    get_files_structure_text,
    get_files_summaries_text,
)

from .basellmmodel import BaseLLMModel


class DefaultLLMModel(BaseLLMModel):
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        self.file_summary_prompt = self._get_file_summary_prompt()
        self.file_summary_chain = LLMChain(
            llm=self.llm, prompt=self.file_summary_prompt
        )
        self.readme_prompt = self._get_readme_prompt()
        self.readme_chain = LLMChain(llm=self.llm, prompt=self.readme_prompt)

    def _get_file_summary_prompt(self) -> BasePromptTemplate:
        template = """Write a concise summary, with 3 lines at most, of the following file contents:
        
        {file_content}
        
        SUMMARY:"""
        prompt = PromptTemplate.from_template(template)
        return prompt

    def _get_readme_prompt(self) -> BasePromptTemplate:
        template = """Generate a README.md for a repository with the following features:
        
        
        {file_structure}
        
        
        {files_contents}
        
        
        The README.md should provide a clear and concise overview of the repository.
        README.md TEXT:
        """

        prompt_template = PromptTemplate(
            input_variables=["file_structure", "files_contents"],
            template=template,
        )
        return prompt_template

    def _get_files_summaries(self, files_contents: Dict[str, str]) -> Dict[str, str]:
        files_summaries = {}
        for file, contents in files_contents.items():
            print(f"Summarizing file: {file}")
            summary = self.file_summary_chain.run(contents)
            files_summaries[file] = summary
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
