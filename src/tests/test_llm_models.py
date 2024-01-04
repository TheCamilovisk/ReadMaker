import unittest
from unittest.mock import patch

from langchain.llms.fake import FakeListLLM

from src.llmmodels.defaultllmmodel import DefaultLLMModel
from src.tests.utils import get_resource_path, get_text_resource
from src.utils.prompt import get_files_structure_text, get_files_summaries_text
from src.repositoryadapters.defaultadapter import DefaultRepositoryAdapter


class TestDefaultLLMModel(unittest.TestCase):
    def setUp(self):
        self.sample_file_structure = [
            "TestRepo/file1.py",
            "TestRepo/file2.py",
        ]

        self.sample_files_contents = {
            "TestRepo/file1.py": "File 1 contents",
            "TestRepo/file2.py": "File 2 contents",
        }

    @patch("src.llmmodels.defaultllmmodel.ChatOpenAI")
    @patch("src.repositoryadapters.defaultadapter.get_repo")
    @patch("src.repositoryadapters.defaultadapter.get_files_list")
    @patch("src.utils.repository.get_repo_ignored")
    def test_get_prompt(
        self, mock_get_repo_ignored, mock_get_files_list, mock_get_repo, mock_openAi
    ):
        expected_prompt_path = get_resource_path("expected_prompt.txt")
        expected_prompt = get_text_resource(expected_prompt_path)

        mock_openAi.result_value = FakeListLLM(responses=["foo", "bar"])

        mock_get_repo.return_value = "mocked repo"
        mock_get_files_list.return_value = self.sample_file_structure
        mock_get_repo_ignored.return_value = []

        file_structure_text = get_files_structure_text(self.sample_file_structure)
        files_summaries_text = get_files_summaries_text(self.sample_files_contents)

        adapter = DefaultRepositoryAdapter(
            "https://git-provider/owner/TestRepo", "/home/workspace"
        )

        llm_model = DefaultLLMModel(adapter)
        prompt_text = (
            llm_model._get_introduction_prompt()
            .format(
                files_structure=file_structure_text,
                files_summaries=files_summaries_text,
            )
            .replace("Human: ", "")
        )
        self.assertEqual(prompt_text, expected_prompt)


if __name__ == "__main__":
    unittest.main()
