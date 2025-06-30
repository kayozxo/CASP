import streamlit as st

st.set_page_config(
    page_title="ResumeX - Professional Resume Builder",
    page_icon="Static/icon.svg",
    initial_sidebar_state="collapsed"
)

cdhi_page = st.Page(
    page="views/page1.py",
    title="Career DHI",
    icon=":material/school:",
    default=True,
)

plag_page = st.Page(
    page="views/page2.py",
    title="Plagiarism Checker",
    icon=":material/check:",
)

'''
ai_page = st.Page(
    page="views/ai.py",
    title="Resume Enhancer",
    icon=":material/star:",
)
'''

pg = st.navigation(pages=[cdhi_page, plag_page])  # , ai_page])
pg.run()