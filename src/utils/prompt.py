from typing import Any, Dict, List

from langchain.chains.base import Chain


def get_files_structure_text(files_list: List[str]) -> str:
    text = "Project file structure:\n"
    text += "\n".join(f"\t\t- {file}" for file in files_list)
    return text


def get_files_summaries_text(files_summaries: Dict[str, str]) -> str:
    text = "Projects files contents summaries:\n"
    text += "\n".join(
        f"\t\t- File: {file}\n\t\t- Contents: {summary}"
        for file, summary in files_summaries.items()
    )
    return text


def execute_prompt(chain: Chain, **kwrags: Any):
    return chain.invoke(kwrags)
