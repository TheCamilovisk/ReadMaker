import os
from typing import Dict, List, Optional

from git import Repo

from .baseadapter import BaseRepositoryAdapter


class DefaultRepositoryAdapter(BaseRepositoryAdapter):
    _TEXT_EXTENSIONS = [
        ".txt",
        ".md",
        ".py",
        ".ipynb",
        ".html",
        ".css",
        ".js",
        ".json",
        ".xml",
        ".yaml",
    ]

    def __init__(self, repo_url: str, base_dir: str) -> None:
        super().__init__()
        self._repo_url = repo_url
        self._base_dir = base_dir
        repo_name = os.path.split(repo_url)[-1]
        self._local_repo_path = os.path.join(base_dir, repo_name)
        self._repo = self._clone_repo(self._repo_url, self._local_repo_path)

    @classmethod
    def _clone_repo(cls, repo_url: str, local_repo_path: str) -> Repo:
        if os.path.exists(local_repo_path):
            print(f"Repository {local_repo_path} already cloned")
            return Repo(local_repo_path)
        print(f"Cloning repository {repo_url} to {local_repo_path}")
        return Repo.clone_from(repo_url, local_repo_path)

    @classmethod
    def _get_file_contents(cls, file_path: str) -> str:
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                return file.read()
        else:
            return None

    def _get_abs_paths(self, files_list: List[str]) -> List[str]:
        return [os.path.join(self._base_dir, f) for f in files_list]

    def repo_list(self, absolute: bool = False) -> List[str]:
        files_paths_list = []
        for root, dirs, files in os.walk(self._local_repo_path, topdown=True):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                is_hidden = file.startswith(".")
                if is_hidden:
                    continue
                pre = root if absolute else root.replace(self._base_dir, "")[1:]
                complete_file_path = os.path.join(pre, file)
                files_paths_list.append(complete_file_path)
        return files_paths_list

    def repo_files_contents(
        self, files_list: Optional[List[str]] = None, absolute: bool = True
    ) -> Dict[str, str]:
        if files_list:
            files_list = files_list if absolute else self._get_abs_paths(files_list)
        else:
            files_list = self.repo_list(absolute=True)
        contents_map = {}
        for file in files_list:
            if not any(file.endswith(e) for e in self._TEXT_EXTENSIONS):
                continue
            contents_map[file] = self._get_file_contents(file)
        return contents_map
