import streamlit as st

st.set_page_config(
    page_title="CASP",
    page_icon=":material/api:",
    initial_sidebar_state="collapsed"
)

pages = {
  "Faculty": [
        st.Page(page="views/page2.py", title="Plagiarism Checker", icon=":material/plagiarism:"),
  ],
  "Students": [
        st.Page(page="views/page1.py", title="Career DHI", icon=":material/work:", default=True),
        st.Page(page="views/page3.py", title="AI Buddy", icon=":material/robot_2:"),
  ]
}

pg = st.navigation(pages)
pg.run()