from typing import Protocol, List, Dict


class BaseRepositoryAdapter(Protocol):
    def repo_list(self) -> List[str]:
        pass

    def repo_files_contents(self) -> Dict[str, str]:
        pass
