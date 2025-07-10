import streamlit as st
import PyPDF2
import os
import tempfile
import pymupdf4llm

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

def resume():

    st.title(":material/demography: Resume Extractor")
    st.write("Upload your resume to extract it's contents.")


    uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf")

    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())


        #import pymupdf
        #doc = pymupdf.open(path)
        #for page in doc:
            #resume_text = page.get_text()


        resume_text = pymupdf4llm.to_markdown(path)
        if resume_text:
            st.success(":material/check: Resume uploaded and processed successfully!")
            with st.expander("Extracted Resume Text"):
                st.markdown(resume_text)
            st.session_state['resume_text'] = resume_text
