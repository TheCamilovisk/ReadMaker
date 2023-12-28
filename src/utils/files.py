import ctypes
import os
import platform
from typing import List

import magic
from langchain.document_loaders import (
    JSONLoader,
    NotebookLoader,
    PythonLoader,
    TextLoader,
)
from langchain.document_loaders.base import BaseLoader

_document_loaders = {
    "py": PythonLoader,
    "ipynb": NotebookLoader,
    "json": JSONLoader,
}


def _is_hidden_unix(path: str) -> bool:
    return os.path.basename(path).startswith(".")


def _is_hidden_windows(path: str) -> bool:
    attribute = ctypes.windll.kernel32.GetFileAttributesW(path)
    return attribute & 0x02 != 0


def is_hidden(path: str) -> bool:
    os_name = platform.system()
    if os_name == "Linux" or os_name == "Darwin":
        return _is_hidden_unix(path)
    elif os_name == "Windows":
        return _is_hidden_windows(path)
    else:
        raise RuntimeError("Unknown operating system.")


def is_text_file(path: str) -> bool:
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(path)
    return mime_type.startswith("text/") or mime_type.endswith("json")


def get_files_list(root_dir: str, include_hidden: bool = False) -> List[str]:
    if not os.path.isdir(root_dir):
        raise ValueError(f"No such folder: {root_dir}")
    files_paths_list = []
    for root, dirs, files in os.walk(root_dir, topdown=True):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not is_hidden(d)]
        for file in files:
            if not include_hidden:
                if not include_hidden and is_hidden(file):
                    continue
                file_path = os.path.join(root, file)
                files_paths_list.append(file_path)
    return files_paths_list


def get_file_contents(file_path: str) -> str:
    if not (os.path.isfile(file_path) and is_text_file(file_path)):
        raise ValueError(f"Not a valid text file: {file_path}")
    ext = os.path.splitext(file_path)[-1].replace(".", "").lower()
    LoaderClass: BaseLoader = _document_loaders.get(ext, TextLoader)
    loader = LoaderClass(file_path)
    content = loader.load()
    return content


def get_relative_path(file_path: str, root_dir: str) -> str:
    return file_path.replace(root_dir, "")[1:]
