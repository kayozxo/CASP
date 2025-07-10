import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools


def generated_report():
    st.title(":material/monitoring: Career Guidance Report")

    # Load environment variables from .env file
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API")

    # — Load Agno LLM pipeline (Groq model)
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key),
        tools=[DuckDuckGoTools()],
        markdown=True,
        show_tool_calls=True,
        description="Career guidance and enrichment agent"
    )

    # — Load session data
    github_df = st.session_state.get("repo_df")
    top_lang = st.session_state.get("top_lang", "N/A")
    semester_data = st.session_state.get("semester_data")
    resume_text = st.session_state.get("resume_text", "")

    # — Early exit if needed data missing
    if github_df is None or github_df.empty \
       or semester_data is None \
       or resume_text.strip() == "":
        st.warning("Please populate GitHub, academic, and resume tabs first.")
        return

    # — Data Overview
    with st.expander(":material/deployed_code_update: GitHub Summary"):
        st.markdown(f"Most Used Language: **{top_lang}**")
        st.dataframe(github_df)
    with st.expander(":material/grading: Academic Summary"):
        for sem, info in semester_data.items():
            st.write(f"**{sem}** — SGPA: {info['SGPA']} | CGPA: {info['CGPA']}")
            st.table(pd.DataFrame(info["grades"], columns=["Subject", "Grade"]))
    with st.expander(":material/demography: Resume"):
        st.markdown(resume_text)


    # — Generate report
    if st.button(":material/school: Generate Career Report"):
        with st.spinner("Running Agno Agent..."):
            prompt = build_prompt(github_df, semester_data, resume_text, top_lang)
            report = agent.run(prompt)
            if hasattr(report, "content"):
                report = report.content
            st.session_state["career_report"] = report

    # — Display saved report
    if "career_report" in st.session_state:
        st.subheader(":material/assignment_late: Career Report")
        st.markdown(st.session_state["career_report"])

        # — Enrich via Agno search
        st.subheader(":material/lightbulb: Course Suggestions")

        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile", api_key=groq_api_key),
            tools=[DuckDuckGoTools()],
            markdown=True,
            show_tool_calls=True,
            description="Search for courses"
        )
        import json
        for topic in ["Machine Learning", "Web Development", "Cloud Computing"]:
            st.markdown(f"**🔹 {topic} Courses**")
            resp = agent.run(f"Top online {topic} courses for beginners:")
            # Try to extract structured data from tool output if available
            items = []
            if hasattr(resp, "tools") and resp.tools:
                for tool in resp.tools:
                    if hasattr(tool, "result") and tool.result:
                        try:
                            data = json.loads(tool.result)
                            if isinstance(data, list):
                                items.extend(data)
                        except Exception:
                            pass
            # Fallback: try to parse from text if not found
            if not items and hasattr(resp, "content"):
                st.markdown(resp.content)
                continue
            # Display structured results
            for item in items:
                name = item.get("title") or item.get("name")
                link = item.get("href") or item.get("link")
                body = item.get("body") or item.get("description")
                image = item.get("image")
                st.markdown(f"- [{name}]({link})")
                if image:
                    st.image(image, width=120)
                if body:
                    st.caption(body)


def build_prompt(github_df, semester_data, resume_text, top_lang):
    return f"""
You are a highly intelligent career mentor.

A student has provided their academic records, GitHub profile, and resume. Analyze the data and return a detailed personalized report with the following:

1. Identify the student's strengths and weaknesses from grades
2. Analyze GitHub repositories and suggest improvement areas
3. Based on resume, suggest certifications/internships/courses
4. Propose ideal career paths (e.g. Backend Developer, Data Scientist)
5. Suggest 3 real courses they can take online (search if needed)
6. Propose 3 advanced GitHub project ideas based on their interests

--- GitHub Summary (Most Used Language: {top_lang}) ---
{github_df.to_markdown(index=False)}

--- Academic Results ---
{format_semesters(semester_data)}

--- Resume Text ---
{resume_text}
"""

def format_semesters(data):
    result = ""
    for sem, values in data.items():
        grades = "\n".join([f"{subj}: {grade}" for subj, grade in values["grades"]])
        sgpa = values["SGPA"]
        cgpa = values["CGPA"]
        result += f"\n{sem}:\n{grades}\nSGPA: {sgpa} | CGPA: {cgpa}\n"
    return result
