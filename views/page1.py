from utils.cdhi.gws import gws
from utils.cdhi.gh import gh
from utils.cdhi.resume import resume
from utils.cdhi.gr2 import generated_report  # new import
import streamlit as st

tab1, tab2, tab3, tab4 = st.tabs([
  "Grades Extractor",
  "GitHub Data Fetcher",
  "Resume Extractor",
  "Career Report"
])

with tab1:
    gws()

with tab2:
    gh()

with tab3:
    resume()

with tab4:
    generated_report()
