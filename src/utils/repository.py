import os

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
