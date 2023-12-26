from typing import Dict, List


def get_files_structure_text(files_list: List[str]) -> str:
    text = "Project file structure:\n"
    text += "\n".join(f"\t- {file}" for file in files_list)
    return text


def get_files_contents_text(files_contents: Dict[str, str]) -> str:
    text = "Projects files contents:\n"
    text += "\n".join(
        f"\t- File: {file}\n\t- Contents:\n```\n{contents}\n```\n"
        for file, contents in files_contents.items()
    )
    return text
