import unittest
from unittest.mock import patch

from langchain.llms.fake import FakeListLLM

from src.llmmodels.defaultllmmodel import DefaultLLMModel
from src.utils.prompt import get_files_summaries_text, get_files_structure_text


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

    @patch("src.llmmodels.defaultllmmodel.OpenAI")
    def test_get_prompt(self, mock_openAi):
        expected_prompt = """Generate a README.md for a repository with the following features:

Project file structure:
\t- TestRepo/file1.py
\t- TestRepo/file2.py

Projects files contents summaries:
\t- File: TestRepo/file1.py
\t- Contents:
```
File 1 contents
```

\t- File: TestRepo/file2.py
\t- Contents:
```
File 2 contents
```

The README.md should provide a clear and concise overview of the repository."""

        mock_openAi.result_value = FakeListLLM(responses=["foo", "bar"])

        file_structure_text = get_files_structure_text(self.sample_file_structure)
        files_contents_text = get_files_summaries_text(self.sample_files_contents)

        llm_model = DefaultLLMModel()
        prompt_text = llm_model._get_readme_prompt().format(
            file_structure=file_structure_text, files_contents=files_contents_text
        )
        self.assertEqual(prompt_text, expected_prompt)

    @patch("src.llmmodels.defaultllmmodel.OpenAI")
    def test_generate_readme(self, mock_openAi):
        mock_openAi.return_value = FakeListLLM(responses=["bar"])

        llm_model = DefaultLLMModel()
        reponse = llm_model.generate_readme(
            self.sample_file_structure, self.sample_files_contents
        )
        self.assertEqual(type(reponse), str)


if __name__ == "__main__":
    unittest.main()
