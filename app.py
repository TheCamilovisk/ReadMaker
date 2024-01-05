from typing import Any

import streamlit as st

from src.llmmodels.defaultllmmodel import BaseLLMModel, DefaultLLMModel
from src.repositoryadapters.defaultadapter import DefaultRepositoryAdapter

REQUIRED_STATE_VARS = (
    "readme_text",
    "readme_submited",
    "repo_url",
    "repo_path",
    "has_readme",
    "info",
    "repo_adapter",
    "llm_model",
)


def init_required_vars(force: bool = False) -> None:
    for var in REQUIRED_STATE_VARS:
        if force or var not in st.session_state:
            st.session_state[var] = None


def generate_readme(llm_model: BaseLLMModel) -> str:
    output = llm_model.generate_readme()

    set_var("readme_text", output)

    return output


def set_var(var_name: str, var_value: Any) -> None:
    st.session_state[var_name] = var_value


def upload_readme():
    st.session_state.repo_adapter.upload_readme(st.session_state.readme_text, force=True)
    set_var("readme_submited", True)


def main():
    st.set_page_config(page_title="ReadMaker: README Generator for Git Repositories")

    init_required_vars()

    st.title("ReadMaker: README Generator for Git Repositories")

    with st.sidebar:
        st.header("Inputs")
        repo_url = st.text_input(
            "Enter the remote Git repository URL",
            value=st.session_state.repo_url or "",
        )
        repo_path = st.text_input(
            "Enter the local system path to clone the repository",
            value=st.session_state.repo_path or "",
        )

        analyze_button = st.button("Analyze repository")
        if analyze_button and not (repo_url and repo_path):
            st.write(":red[Enter the repository URL and local path]")

        if analyze_button and repo_url and repo_path:
            set_var("repo_url", repo_url)
            set_var("repo_path", repo_path)
            repo_adapter = DefaultRepositoryAdapter(
                repo_url=repo_url, base_dir=repo_path
            )
            llm_model = DefaultLLMModel(repo_adapter)
            set_var("repo_adapter", repo_adapter)
            set_var("llm_model", llm_model)
            set_var("has_readme", bool(repo_adapter.readme()))

    if st.session_state.has_readme:
        st.subheader(":red[WARNING: The selected repository already contains a README]")

    if (
        st.session_state.repo_url
        and st.session_state.repo_path
        and not st.session_state.readme_text
    ):
        st.button(
            "Generate README",
            on_click=generate_readme,
            args=[st.session_state.llm_model],
        )

    elif st.session_state.readme_text:
        text_area_text = st.text_area(
            "Generated README", st.session_state.readme_text, height=300
        )

        col1, col2, col3 = st.columns(3)
        update_button = col1.button(
            "Update Preview",
            on_click=set_var,
            args=["readme_text", text_area_text],
            use_container_width=True,
        )

        submit_button = col2.button(
            "Submit README"
            if not (st.session_state.has_readme and st.session_state.readme_submited)
            else "Update README",
            on_click=upload_readme,
            use_container_width=True,
        )

        col3.button(
            "Clear",
            on_click=init_required_vars,
            args=[True],
            use_container_width=True,
        )
        set_var("info", "")
        if update_button:
            set_var("info", "Preview updated")
        elif submit_button:
            set_var("info", "README submited")
        if info := st.session_state.info:
            st.info(info)

        with st.expander("README Preview", expanded=True):
            st.markdown(st.session_state.readme_text)
    else:
        st.subheader(
            "Enter the repository URL and local path in the siderbar input fields"
        )


if __name__ == "__main__":
    main()
