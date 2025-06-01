import streamlit as st
import requests
import pandas as pd
from collections import Counter

def fetch_repo_languages(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
    response = requests.get(url)
    if response.status_code == 200:
        return list(response.json().keys())  # list of languages used
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

    # Calculate most used language
    lang_counter = Counter(all_languages)
    most_common_lang = lang_counter.most_common(1)[0][0] if lang_counter else "N/A"

    return pd.DataFrame(repo_data), most_common_lang


# ------------------------------
# Streamlit UI
# ------------------------------

st.title("🐙 GitHub Tech Stack Analyzer")

github_user = st.text_input("Enter GitHub username")

if st.button("Analyze GitHub"):
    if github_user:
        with st.spinner("Fetching GitHub data..."):
            df, top_lang = fetch_github_repos_with_languages(github_user)
            if df is not None and not df.empty:
                st.success(f"Found {len(df)} public repositories.")
                st.markdown(f"### 🚀 Most Used Language: `{top_lang}`")
                st.markdown("### 📦 Repository Details")
                st.dataframe(df)
            else:
                st.warning("No repositories found or user does not exist.")
    else:
        st.warning("Please enter a GitHub username.")
