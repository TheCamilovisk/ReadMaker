from typing import Any, Dict, List

from langchain.chains.base import Chain


def get_files_structure_text(files_list: List[str]) -> str:
    text = "Project file structure:\n"
    text += "\n".join(f"- {file}" for file in files_list)
    return text


def get_files_summaries_text(files_summaries: Dict[str, str]) -> str:
    text = "Projects files contents summaries:\n"
    text += "\n\n".join(
        f"- File: {file}\n- Contents: {summary}"
        for file, summary in files_summaries.items()
    )
    return text


def execute_prompt(chain: Chain, **kwrags: Any):
    return chain.invoke(kwrags)
