import os
from typing import Dict, List

from src.utils.files import get_file_contents, get_files_list
from src.utils.repository import get_repo, get_repo_name_from_url

from .baseadapter import BaseRepositoryAdapter


class DefaultRepositoryAdapter(BaseRepositoryAdapter):
    def __init__(self, repo_url: str, base_dir: str) -> None:
        super().__init__()
        self._repo_url = repo_url
        self._base_dir = base_dir
        self._repo_name = get_repo_name_from_url(self._repo_url)
        self._repo_path = os.path.join(base_dir, self._repo_name)
        self._repo = get_repo(self._repo_url, self._repo_path)

    def _get_repo_relative_paths(self, repo_list: List[str]) -> List[str]:
        return [p.replace(self._base_dir, "")[1:] for p in repo_list]

    def repo_list(self, absolute: bool = False) -> List[str]:
        raw_files_list = get_files_list(self._repo_path, include_hidden=False)
        files_list = (
            raw_files_list
            if absolute
            else self._get_repo_relative_paths(raw_files_list)
        )
        return files_list

    def repo_files_contents(self) -> Dict[str, str]:
        files_list = self.repo_list(absolute=True)
        contents_map = {}
        for file in files_list:
            try:
                contents = get_file_contents(file)
                contents_map[file] = contents
            except ValueError:
                continue
            except Exception as e:
                raise RuntimeError(f"Failed to get files contents.\nError:\n{e}")
        return contents_map
