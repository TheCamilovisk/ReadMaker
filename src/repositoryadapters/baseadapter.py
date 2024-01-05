from typing import Any, Dict, List, Optional, Protocol, Tuple


class BaseRepositoryAdapter(Protocol):
    repo_url: str

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

    def readme(self) -> Optional[str]:
        pass
