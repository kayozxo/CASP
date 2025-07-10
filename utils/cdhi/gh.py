import streamlit as st
import requests
import pandas as pd
from collections import Counter

def fetch_repo_languages(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    response = requests.get(url)
    if response.status_code == 200:
        return list(response.json().keys())
    else:
        return []

def fetch_github_repos_with_languages(username):
    repo_url = f"https://api.github.com/users/{username}/repos"
    repo_response = requests.get(repo_url)

    if repo_response.status_code != 200:
        return None, None

    repos = repo_response.json()
    repo_data = []
    all_languages = []

    for repo in repos:
        name = repo['name']
        languages = fetch_repo_languages(username, name)
        all_languages.extend(languages)

        repo_data.append({
            "Name": name,
            "URL": repo['html_url'],
            "Description": repo['description'],
            "Primary Language": repo['language'],
            "Tech Stack": ", ".join(languages),
            "Stars ⭐": repo['stargazers_count'],
            "Forks 🍴": repo['forks_count'],
            "Last Updated 📅": repo['updated_at'][:10]
        })

    lang_counter = Counter(all_languages)
    most_common_lang = lang_counter.most_common(1)[0][0] if lang_counter else "N/A"

    return pd.DataFrame(repo_data), most_common_lang


# ------------------------------
# Streamlit UI
# ------------------------------

def gh():
    st.title(":material/deployed_code_update: GitHub Data Fetcher")

    if "github_user" not in st.session_state:
        st.session_state.github_user = ""
    if "repo_df" not in st.session_state:
        st.session_state.repo_df = None
    if "top_lang" not in st.session_state:
        st.session_state.top_lang = None

    col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom", gap="small")

    with col1:
        github_user = st.text_input("Enter GitHub username", st.session_state.github_user)

    with col2:
        analyse = st.button("Analyze GitHub")

    if analyse:
            if github_user:
                with st.spinner("Fetching GitHub data..."):
                    df, top_lang = fetch_github_repos_with_languages(github_user)
                    if df is not None and not df.empty:
                        st.session_state.github_user = github_user
                        st.session_state.repo_df = df
                        st.session_state.top_lang = top_lang
                        st.success(f"Found {len(df)} public repositories.")
                    else:
                        st.warning("No repositories found or user does not exist.")
            else:
                st.warning("Please enter a GitHub username.")

    # Display from session state
    if st.session_state.repo_df is not None:
        st.markdown(f"### :material/code: Most Used Language: `{st.session_state.top_lang}`")
        st.markdown("### :material/folder_data: Repository Details")
        st.dataframe(st.session_state.repo_df)


if __name__ == "__main__":
    gh()
