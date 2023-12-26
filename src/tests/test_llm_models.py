import unittest

from src.llmmodels.defaultllmmodel import DefaultLLMModel
from src.utils.prompt import get_files_contents_text, get_files_structure_text


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

    def test_get_prompt(self):
        expected_prompt = """Generate a README.md for a repository with the following features:

Project file structure:
\t- TestRepo/file1.py
\t- TestRepo/file2.py

Projects files contents:
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

The README.md should provide a clear and concise overview of the repository.
The output must be in markdown code only."""

        file_structure_text = get_files_structure_text(self.sample_file_structure)
        files_contents_text = get_files_contents_text(self.sample_files_contents)

        llm_model = DefaultLLMModel()
        prompt_text = llm_model.get_prompt().format(
            file_structure=file_structure_text, files_contents=files_contents_text
        )
        self.assertEqual(prompt_text, expected_prompt)


if __name__ == "__main__":
    unittest.main()
