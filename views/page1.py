from utils.cdhi.gws import gws
from utils.cdhi.gh import gh
from utils.cdhi.resume import resume
from utils.cdhi.gr2 import generated_report  # new import
import streamlit as st
import streamlit_antd_components as sac

current_step = sac.steps(
  items=[
      sac.StepsItem(title="Grades Extractor"),
      sac.StepsItem(title="GitHub Data Fetcher"),
      sac.StepsItem(title="Resume Extractor"),
      sac.StepsItem(title="Career Report"),
  ],
  size="xs",
  return_index=True,
)

if current_step == 0:
    gws()

if current_step == 1:
    gh()

if current_step == 2:
    resume()

if current_step == 3:
    generated_report()