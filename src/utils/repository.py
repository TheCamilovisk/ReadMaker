import os
from contextlib import contextmanager
from typing import List, Optional
from uuid import uuid4

from git import GitCommandError, Repo

from .files import create_local_file


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


def search_file_in_repo_root(repo: Repo, filename: str) -> Optional[str]:
    path = repo._working_tree_dir
    file_path = os.path.join(path, filename)
    if os.path.isfile(file_path):
        return file_path
    else:
        return None


def get_repo_license_file(repo: Repo) -> Optional[str]:
    return search_file_in_repo_root(repo, "LICENSE")


def get_readme_file(repo: Repo) -> Optional[str]:
    return search_file_in_repo_root(repo, "README.md")


def get_license_type_from_file(file_path: str) -> str:
    license_type = None
    with open(file_path, "r") as f:
        license_type = f.readline().strip()
    return license_type


def create_random_branch_name(
    prefix: Optional[str] = None, suffix: Optional[str] = None
) -> str:
    rnd_str = uuid4().hex
    prefix = f"{prefix}_" if prefix else ""
    suffix = f"_{suffix}" if suffix else ""
    return prefix + rnd_str + suffix


@contextmanager
def git_local_branch(repo: Repo, new_branch: str) -> None:
    original_branch = repo.active_branch
    try:
        repo.git.checkout("HEAD", b=new_branch)
        yield
    except Exception as e:
        raise RuntimeError(f"Could not create branch: {new_branch}\nError: {e}")
    finally:
        repo.git.checkout(original_branch)


def create_local_branch_commit_push(
    repo: Repo,
    new_branch: str,
    file_path: str,
    file_content: str,
    commit_message: str,
    force: bool = True,
) -> None:
    try:
        repo_path = repo._working_tree_dir
        full_file_path = os.path.join(repo_path, file_path)
        with git_local_branch(repo, new_branch):
            create_local_file(full_file_path, file_content, force=force)
            repo.index.add([full_file_path])
            repo.index.commit(commit_message)
            origin = repo.remote(name="origin")
            origin.push(new_branch)
    except GitCommandError as e:
        raise RuntimeError(
            f"Not possible to commit file {file_path} to branch: {new_branch}\nError: {e}"
        )
