from typing import Any

import streamlit as st

REQUIRED_STATE_VARS = (
    "readme_text",
    "readme_submited",
    "repo_url",
    "repo_path",
    "has_readme",
    "info",
)


def init_required_vars(force: bool = False) -> None:
    for var in REQUIRED_STATE_VARS:
        if force or var not in st.session_state:
            st.session_state[var] = None


def generate_readme(repo_url: str, repo_path: str) -> str:
    output = f"""This is a generated README text for the repository.

INPUTS:
- repo_url = {repo_url}
- repo_path = {repo_path}"""

    return output


def set_var(var_name: str, var_value: Any) -> None:
    st.session_state[var_name] = var_value


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

    if st.session_state.has_readme:
        st.subheader(":red[WARNING: The selected repository already contains a README]")

    if (
        st.session_state.repo_url
        and st.session_state.repo_path
        and not st.session_state.readme_text
    ):
        st.button(
            "Generate README",
            on_click=set_var,
            args=["readme_text", generate_readme(repo_url, repo_path)],
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
            if not st.session_state.readme_submited
            else "Update README",
            on_click=set_var,
            args=["readme_submited", True],
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
