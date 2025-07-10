import streamlit as st
import os
from utils.plag.pdf_to_image import pdf_to_stitched_image
from utils.plag.vision import extract_text_from_image
import json
import re

UPLOAD_DIR = "uploads"
STITCHED_DIR = "stitched"
DB_PATH = "vision_text_db.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(STITCHED_DIR, exist_ok=True)

def save_to_db(roll_no, name, pdf_path, stitched_path, extracted_text):
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
    else:
        db = []
    db.append({
        "roll_no": roll_no,
        "name": name,
        "pdf_path": pdf_path,
        "stitched_path": stitched_path,
        "extracted_text": extracted_text
    })
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def load_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def split_into_sentences(text):
    # Simple sentence splitter using regex (can be replaced with nltk if needed)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Remove empty sentences
    return [s.strip() for s in sentences if s.strip()]

def main():
    tab1, tab2 = st.tabs(["Assignment Submission", "Plagiarism Check"])

    with tab1:
        st.title(":material/assignment_add: Assignment Submission")
        uploaded_file = st.file_uploader("Upload Assignment PDF (Handwritten/Typed)", type=["pdf"])
        extracted_text = ""

        if uploaded_file is not None:
            with st.container(border=True):
                roll_no = st.text_input("Roll Number")
                name = st.text_input("Student Name")
                if st.button("Submit Assignment"):
                    if not (roll_no and name):
                        st.error("Roll number and name required.")
                        return

                    pdf_path = os.path.join(UPLOAD_DIR, f"{roll_no}_{uploaded_file.name}")
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    stitched_path = os.path.join(STITCHED_DIR, f"{roll_no}_stitched.png")
                    pdf_to_stitched_image(pdf_path, stitched_path)

                    st.toast(f"PDF stitched and saved as {stitched_path}")

                    from utils.plag.image_split import split_image_by_size
                    chunk_paths = split_image_by_size(stitched_path)
                    extracted_text = ""
                    for chunk_path in chunk_paths:
                        extracted_text += extract_text_from_image(chunk_path) + "\n"

                    with st.expander("Extracted Text"):
                        st.text_area("Extracted Text", extracted_text, height=300)
                    save_to_db(roll_no, name, pdf_path, stitched_path, extracted_text)
                    st.success("Text extracted and saved for plagiarism checking.")

    with tab2:
        st.title(":material/plagiarism: Plagiarism Check")
        db = load_db()
        if not db:
            st.info("No submissions in the database.")
            return
        roll_nos = sorted(set([entry["roll_no"] for entry in db]))
        selected_roll = st.selectbox("Select Student Roll Number", roll_nos, index=None)
        threshold = st.slider("Show matches above score", 0, 100, 60, 1, key="vision_faculty_threshold_sentence")
        if st.button(":material/document_scanner: Check Plagiarism"):
            target_entry = next((entry for entry in db if entry["roll_no"] == selected_roll), None)
            if not target_entry:
                st.error("Submission not found.")
                return
            text = target_entry["extracted_text"]
            if not text or len(text) < 50:
                st.warning("Could not extract sufficient text from the selected submission.")
                return
            set1 = set(split_into_sentences(text.lower()))
            other_entries = [entry for entry in db if entry["roll_no"] != selected_roll]
            matches = []
            for entry in other_entries:
                other_text = entry["extracted_text"]
                if not other_text or len(other_text) < 50:
                    continue
                set2 = set(split_into_sentences(other_text.lower()))
                jaccard_sim = len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0.0
                score = int(jaccard_sim * 100)
                if score >= threshold:
                    matches.append({
                        "roll_no": entry["roll_no"],
                        "name": entry["name"],
                        "score": score
                    })
            if not matches:
                st.warning("No significant plagiarism detected above the threshold. Try lowering the threshold if you expect a match.")
            else:
                best_match = max(matches, key=lambda x: x["score"])
                st.subheader("Most Similar Submission (Sentence Level)")
                st.write(f"Roll No: {best_match['roll_no']} | Name: {best_match['name']} | Score: {best_match['score']}%")
                st.info(f"Showing only the most similar match with score ≥ {threshold}")

if __name__ == "__main__":
    main()