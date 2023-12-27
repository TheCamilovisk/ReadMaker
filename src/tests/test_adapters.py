import unittest
from unittest.mock import patch

from src.repositoryadapters.defaultadapter import DefaultRepositoryAdapter


class TestDefaultAdapter(unittest.TestCase):
    @patch("src.repositoryadapters.defaultadapter.get_repo")
    def test_repo_name(self, mock_get_repo):
        mock_get_repo.return_value = "mocked repo"

        adapter = DefaultRepositoryAdapter(
            "https://git-provider/owner/TestRepo", "/home/workspace"
        )
        self.assertEquals(adapter.repo_name, "TestRepo")

    def test_error_cloning(self):
        with self.assertRaises(RuntimeError):
            DefaultRepositoryAdapter(
                "https://git-provider/owner/TestRepo", "/home/workspace"
            )

    @patch("os.path.exists")
    def test_error_repo_from_dir(self, mock_exists):
        mock_exists.return_value = True

        with self.assertRaises(RuntimeError):
            DefaultRepositoryAdapter(
                "https://git-provider/owner/TestRepo", "/home/workspace"
            )

    @patch("src.repositoryadapters.defaultadapter.get_repo")
    @patch("src.repositoryadapters.defaultadapter.get_files_list")
    @patch("src.utils.repository.get_repo_ignored")
    def test_repo_list(self, mock_get_repo_ignored, mock_get_files_list, mock_get_repo):
        expected_result1 = [
            "/home/workspace/TestRepo/file1.py",
            "/home/workspace/TestRepo/file2.py",
        ]
        expected_result2 = [
            "TestRepo/file1.py",
            "TestRepo/file2.py",
        ]

        mock_get_repo.return_value = "mocked repo"
        mock_get_files_list.return_value = expected_result1
        mock_get_repo_ignored.return_value = []

        adapter = DefaultRepositoryAdapter(
            "https://git-provider/owner/TestRepo", "/home/workspace"
        )

        self.assertListEqual(adapter.repo_list(absolute=True), expected_result1)
        self.assertListEqual(adapter.repo_list(absolute=False), expected_result2)

    @patch("src.repositoryadapters.defaultadapter.get_repo")
    @patch("src.repositoryadapters.defaultadapter.get_files_list")
    @patch("src.repositoryadapters.defaultadapter.get_file_contents")
    @patch("src.utils.repository.get_repo_ignored")
    def test_repo_files_contents(
        self,
        mock_get_repo_ignored,
        mock_get_file_contents,
        mock_get_files_list,
        mock_get_repo,
    ):
        files_contents = {
            "/home/workspace/TestRepo/file1.py": "File 1 contents",
            "/home/workspace/TestRepo/file2.py": "File 2 contents",
        }
        expected_results = {
            k.replace("/home/workspace/", ""): v for k, v in files_contents.items()
        }

        def get_file_contents_side_effect(file):
            return files_contents[file]

        mock_get_repo.return_value = "mocked repo"
        mock_get_files_list.return_value = [
            "/home/workspace/TestRepo/file1.py",
            "/home/workspace/TestRepo/file2.py",
        ]
        mock_get_file_contents.side_effect = get_file_contents_side_effect
        mock_get_repo_ignored.return_value = []

        adapter = DefaultRepositoryAdapter(
            "https://git-provider/owner/TestRepo", "/home/workspace"
        )

        self.assertDictEqual(adapter.repo_files_contents(), expected_results)


if __name__ == "__main__":
    unittest.main()
