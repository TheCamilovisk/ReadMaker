import unittest
from unittest.mock import patch

from langchain.llms.fake import FakeListLLM

from src.llmmodels.defaultllmmodel import DefaultLLMModel
from src.tests.utils import get_resource_path, get_text_resource
from src.utils.prompt import get_files_structure_text, get_files_summaries_text
from src.configs.llmmodels.defaultllmmodel import DefaultLLMModelConfig
from src import config


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
    def test_get_prompt(self, mock_openAi):
        expected_prompt_path = get_resource_path("expected_prompt.txt")
        expected_prompt = get_text_resource(expected_prompt_path)

        mock_openAi.result_value = FakeListLLM(responses=["foo", "bar"])

        file_structure_text = get_files_structure_text(self.sample_file_structure)
        files_summaries_text = get_files_summaries_text(self.sample_files_contents)

        llm_model = DefaultLLMModel()
        prompt_text = (
            llm_model._get_introduction_prompt()
            .format(
                files_structure=file_structure_text,
                files_summaries=files_summaries_text,
            )
            .replace("Human: ", "")
        )
        print(prompt_text)
        print(expected_prompt)
        self.assertEqual(prompt_text, expected_prompt)


if __name__ == "__main__":
    unittest.main()
