from __future__ import annotations

import os

from src import config
from src.utils.files import get_file_contents, get_files_list


class DefaultLLModelConfig:
    def load_prompts_from_folder(self, folder_path: str) -> None:
        files_list = get_files_list(folder_path)
        files_contents = {}
        for file in files_list:
            file_base_name = os.path.basename(file)
            base_name_without_ext = os.path.splitext(file_base_name)[0]
            contents = "\n".join(d.page_content for d in get_file_contents(file))
            files_contents[base_name_without_ext] = contents

        self.file_summary_prompt_template = files_contents["file_summary"]
        self.introduction_prompt_template = files_contents["introduction"]
        self.file_structure_prompt_template = files_contents["file_structure"]
        self.installation_prompt_template = files_contents["installation"]
        self.repository_overview_prompt_template = files_contents["repository_overview"]
        self.license_prompt_template = files_contents["license_text"]

    @classmethod
    def get_default_config(cls) -> DefaultLLModelConfig:
        model_config = cls()
        resources_path = os.path.join(
            config.RESOURCES_DIR, "prompts", "defaultllmmodel"
        )
        model_config.load_prompts_from_folder(resources_path)
        return model_config
