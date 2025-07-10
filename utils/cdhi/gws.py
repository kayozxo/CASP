import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def get_credentials(username, password):
    chrome_options = Options()

    # Setup Chrome headless
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Use desktop user-agent
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://login.gitam.edu")  # Use your actual URL

    # Login
    driver.find_element(By.ID, "txtusername").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    time.sleep(1)

    # Read captcha
    captcha_container = driver.find_element(By.CLASS_NAME, "preview")
    captcha_code = ''.join([span.text for span in captcha_container.find_elements(By.TAG_NAME, "span")])
    driver.find_element(By.ID, "captcha_form").send_keys(captcha_code)
    driver.find_element(By.ID, "Submit").click()

    time.sleep(1)
    driver.execute_script("loadConfigView('13')")

    all_semester_data = {}
    wait = WebDriverWait(driver, 10)
    time.sleep(4)

    select = Select(driver.find_element(By.ID, "semester"))
    semester_options = [opt.get_attribute("value") for opt in select.options if opt.get_attribute("value")]

    for sem_value in semester_options:
        print(f"Fetching Semester {sem_value}")
        select.select_by_value(sem_value)
        driver.execute_script("GetselectByType();")
        wait.until(EC.presence_of_element_located((By.ID, "example55")))
        time.sleep(2)

        table = driver.find_element(By.ID, "example55")
        rows = table.find_elements(By.TAG_NAME, "tr")
        semester_results = []

        for row in rows[:-1]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 2:
                subject = cols[0].text.strip()
                grade = cols[1].text.strip()
                semester_results.append((subject, grade))

        sgpa = cgpa = None
        last_row_text = rows[-1].text
        if "SGPA" in last_row_text and "CGPA" in last_row_text:
            parts = last_row_text.split()
            for i, part in enumerate(parts):
                if part == "SGPA:":
                    sgpa = parts[i + 1]
                if part == "CGPA:":
                    cgpa = parts[i + 1]

        all_semester_data[f"Semester {sem_value}"] = {
            "grades": semester_results,
            "SGPA": sgpa,
            "CGPA": cgpa
        }

    driver.quit()
    return all_semester_data


# ------------------------------
# Streamlit UI
# ------------------------------

def gws():

    st.title(":material/grading: Grades Extractor")

    with st.container(border=True):
        col1, col2 = st.columns(2, vertical_alignment="bottom", gap="small")
        with col1:
            username = st.text_input("Enter your username")
        with col2:
            password = st.text_input("Enter your password", type="password")

        if st.button("Fetch Results", use_container_width=True):
            if username and password:
                with st.spinner("Logging in and fetching results..."):
                    try:
                        semester_data = get_credentials(username, password)
                        st.session_state.semester_data = semester_data
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")
            else:
                st.warning("Please enter both username and password.")

    with st.expander("Results", expanded=True):
    # Show results if available
        if "semester_data" in st.session_state:
            semester_data = st.session_state.semester_data
            selected_sem = st.selectbox("Select a semester", list(semester_data.keys()))

            if selected_sem:
                data = semester_data[selected_sem]
                df = pd.DataFrame(data["grades"], columns=["Subject", "Grade"])
                st.subheader(f"Results for {selected_sem}")
                st.table(df)
                st.markdown(f"**SGPA:** {data['SGPA']}  **CGPA:** {data['CGPA']}")

if __name__ == "__main__":
    gws()