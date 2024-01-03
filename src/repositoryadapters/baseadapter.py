from typing import Any, Dict, List, Protocol, Tuple


class BaseRepositoryAdapter(Protocol):
    def repo_list(self) -> List[str]:
        pass

    def repo_files_contents(self) -> Dict[str, str]:
        pass

    def repo_structure(
        self, directories_only: bool = True, use_gitignore: bool = True, **kwargs: Any
    ) -> str:
        pass

    def license(self) -> Tuple[str, str]:
        pass
