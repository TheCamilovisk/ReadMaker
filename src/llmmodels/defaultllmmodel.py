from typing import Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.prompts import BaseChatPromptTemplate, ChatPromptTemplate
from langchain.schema import StrOutputParser

from src.utils.preprocess import remove_markdown_tags
from src.utils.prompt import (
    execute_prompt,
    get_files_structure_text,
    get_files_summaries_text,
)

from .basellmmodel import BaseLLMModel


class DefaultLLMModel(BaseLLMModel):
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")
        self.file_summary_chain = (
            self._get_file_summary_prompt() | self.llm | StrOutputParser()
        )
        self.introduction_chain = (
            self._get_introduction_prompt() | self.llm | StrOutputParser()
        )
        self.file_structure_chain = (
            self._get_file_structure_prompt() | self.llm | StrOutputParser()
        )
        self.installation_chain = (
            self._get_installation_prompt() | self.llm | StrOutputParser()
        )
        self.repository_overview_chain = (
            self._get_repository_overview_prompt() | self.llm | StrOutputParser()
        )
        self.license_chain = self._get_license_prompt() | self.llm | StrOutputParser()

    def _get_file_summary_prompt(self) -> BaseChatPromptTemplate:
        template = """Write a concise summary, with 3 lines at most, of the following file contents:
        
        {file_contents}
        
        SUMMARY:"""
        return ChatPromptTemplate.from_template(template)

    def _get_introduction_prompt(self) -> BaseChatPromptTemplate:
        template = """We have a code repository with the following features:
        
        
        {files_structure}
        
        
        {files_summaries}
        
        
        Write an Introduction text for the repository. The Introduction must provide a clear and concise overview of the repository, must have a single paragraph of 10 lines at most and should not mention files that are not related to the main goal of the repository (e.g.: README.md, LICENSE, requirements.txt, configuration files, etc). Add the title to the text. The output must be in markdown text."""
        return ChatPromptTemplate.from_template(template)

    def _get_file_structure_prompt(self) -> BaseChatPromptTemplate:
        template = """We have a code repository with the following file structure:
    
        {files_structure}
        
        Write the text for the File Structure of the repository's README. The new file structure must be in a structured format, similar to output of the "tree" linux prompt command. The section text must consist of a title followed by the file structure. The output must be in markdown text."""
        return ChatPromptTemplate.from_template(template)

    def _get_installation_prompt(self) -> BaseChatPromptTemplate:
        template = """We have a code repository with the following file structure:

        {files_summaries}

        Write the text for the Installation section of this repository's README. The Installation section must contain (as subsections) the list of prerequisites, the list of the main used packages,  and environment setup instructions. Add the title (top level) to the text. The output must be a markdown text."""
        return ChatPromptTemplate.from_template(template)

    def _get_repository_overview_prompt(self) -> BaseChatPromptTemplate:
        template = """We have a code repository with the following files:
        
        
        {files_structure}
        
        
        {files_summaries}
        
        
        Write the section "Repository overview" for the README. The section must consist of a title (top level) followed by a brief summary and purpose of each folder and the main. The output must be a markdown text and should not mention files that are not related to the main goal of the repository (e.g.: README.md, LICENSE, requirements.txt, configuration files, etc). Add the title (top level) to the text."""
        return ChatPromptTemplate.from_template(template)

    def _get_license_prompt(self) -> BaseChatPromptTemplate:
        template = """We have a code repository with the following file structure:
        
        {files_structure}

        Write the section LICENSE of the repository. The text must consist of a title (top-level) followed by a single line, with the link to the repository's LICENSE file. The link should be relative to the root of the repository. The text of the link must be just the letters that represents the lincese type. The output must be a markdown text."""
        return ChatPromptTemplate.from_template(template)

    def _get_files_summaries(self, files_contents: Dict[str, str]) -> Dict[str, str]:
        files_summaries = {}
        for file, contents in files_contents.items():
            print(f"Summarizing file: {file}")
            summary = execute_prompt(self.file_summary_chain, file_contents=contents)
            files_summaries[file] = summary
        return files_summaries

    def generate_readme(
        self, files_structure: List[str], files_contents: Dict[str, str]
    ) -> str:
        files_structure_text = get_files_structure_text(files_structure)

        files_summaries = self._get_files_summaries(files_contents)
        files_summaries_text = get_files_summaries_text(files_summaries)

        print("Generating README.md")
        readme_text = "\n\n".join(
            remove_markdown_tags(text)
            for text in (
                execute_prompt(
                    self.introduction_chain,
                    files_structure=files_structure_text,
                    files_summaries=files_summaries_text,
                ),
                execute_prompt(
                    self.file_structure_chain, files_structure=files_structure_text
                ),
                execute_prompt(
                    self.installation_chain, files_summaries=files_summaries_text
                ),
                execute_prompt(
                    self.repository_overview_chain,
                    files_structure=files_structure_text,
                    files_summaries=files_summaries_text,
                ),
                execute_prompt(
                    self.license_chain, files_structure=files_structure_text
                ),
            )
        )
        return readme_text
