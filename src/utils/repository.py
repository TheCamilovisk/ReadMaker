import os
from glob import glob
from typing import List, Optional

from git import Repo


def _get_repo_from_dir(repo_path: str) -> Repo:
    try:
        return Repo(repo_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to create repository from path: {repo_path}\nError:\n{e}"
        )


def _clone_repo(repo_url: str, repo_path: str) -> Repo:
    try:
        return Repo.clone_from(repo_url, repo_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to clone repository {repo_url} to {repo_path}\nError:\n{e}"
        )


def get_repo(repo_url: str, repo_path: str) -> Repo:
    if os.path.exists(repo_path):
        repo = _get_repo_from_dir(repo_path)
        print(f"Repository {repo_url} already exists in {repo_path}.")
        return repo
    repo = _clone_repo(repo_url, repo_path)
    print(f"Repository {repo_url} cloned to {repo_path}.")
    return repo


def get_repo_name_from_url(repo_url: str) -> str:
    return os.path.basename(repo_url)


def get_repo_ignored(repo: Repo, files_list: List[str]) -> List[str]:
    return repo.ignored(*files_list)


def get_repo_non_ignored(repo: Repo, files_list: List[str]) -> List[str]:
    ignored = get_repo_ignored(repo, files_list)
    return [p for p in files_list if p not in ignored]


def get_repo_license_file(repo: Repo) -> Optional[str]:
    path = repo.working_tree_dir
    pattern = os.path.join(path, "*LICENSE")
    glob_output = glob(pattern)
    if glob_output:
        return glob_output[0]
    else:
        return None


def get_license_type_from_file(file_path: str) -> str:
    license_type = None
    with open(file_path, "r") as f:
        license_type = f.readline().strip()
    return license_type
