import os
from typing import Dict, List, Optional, Tuple

from src.utils.files import (
    get_file_contents,
    get_files_list,
    get_folder_structure_str,
    get_relative_path,
)
from src.utils.repository import (
    get_license_type_from_file,
    get_readme_file,
    get_repo,
    get_repo_license_file,
    get_repo_name_from_url,
    get_repo_non_ignored,
)

from .baseadapter import BaseRepositoryAdapter


class DefaultRepositoryAdapter(BaseRepositoryAdapter):
    def __init__(self, repo_url: str, base_dir: str) -> None:
        super().__init__()
        self.repo_url = repo_url
        self.base_dir = base_dir
        self.repo_name = get_repo_name_from_url(self.repo_url)
        self.repo_path = os.path.join(base_dir, self.repo_name)
        self.repo = get_repo(self.repo_url, self.repo_path)

    def _get_repo_relative_paths(self, repo_list: List[str]) -> List[str]:
        return [get_relative_path(p, self.base_dir) for p in repo_list]

    def repo_list(self, absolute: bool = False) -> List[str]:
        raw_files_list = get_files_list(self.repo_path, include_hidden=False)
        raw_files_list[:] = get_repo_non_ignored(self.repo, raw_files_list)
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
                contents_map[get_relative_path(file, self.base_dir)] = contents
            except ValueError:
                continue
            except Exception as e:
                raise RuntimeError(f"Failed to get files contents.\nError:\n{e}")
        return contents_map

    def repo_structure(
        self,
        directories_only: bool = True,
        use_gitignore: bool = True,
        exclude_patterns: Optional[List[str]] = ["__pycache__"],
    ) -> str:
        file_structure_lines = get_folder_structure_str(
            self.repo_path,
            directories_only=directories_only,
            use_gitignore=use_gitignore,
            exclude_patterns=exclude_patterns,
        ).split("\n")
        processed_tree_output = (
            self.repo_name + "\n" + "\n".join(file_structure_lines[1:])
        )
        return processed_tree_output

    def license(self) -> Tuple[str, str]:
        license_path = get_repo_license_file(self.repo)
        license_type = get_license_type_from_file(license_path)
        license_link = license_path.replace(
            self.repo_path, f"{self.repo_url}/blob/main"
        )
        return license_type, license_link

    def readme(self) -> Optional[str]:
        return get_readme_file(self.repo)
