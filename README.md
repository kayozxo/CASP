# CASP: AI-Powered Career, Plagiarism, and Study Assistant

CASP is a modern, full-stack Streamlit application that empowers students and educators with three powerful AI-driven features:

1. **Career DHI (Career Data, Highlights & Insights)**
2. **Plagiarism Checker (Vision-based, Sentence-level)**
3. **AI Buddy (Smart Notes Generator & Document Chatbot)**

## 🚀 Features Overview

### 1. Career DHI (Career Data, Highlights & Insights)

- **Grades Extractor:** Securely fetches academic results from your university portal using browser automation (Selenium). Parses semester-wise grades, SGPA, and CGPA.
- **GitHub Data Fetcher:** Connects to your GitHub profile, analyzes repositories, and identifies your most-used languages and tech stack.
- **Resume Extractor:** Upload your resume (PDF) and extract its content using advanced PDF parsing (PyMuPDF4LLM). No manual copy-paste needed.
- **AI-Powered Career Report:** Combines your academic, GitHub, and resume data. Uses a Groq LLM agent (via Agno) to generate a detailed, personalized career guidance report, including:
  - Strengths & weaknesses
  - GitHub improvement suggestions
  - Certification/course recommendations
  - Ideal career paths
  - Real online course links
  - Advanced project ideas

### 2. Plagiarism Checker (Vision-based, Sentence-level)

- **PDF-to-Image Conversion:** Converts assignment PDFs (handwritten or typed) into stitched images for robust OCR.
- **Vision LLM OCR:** Uses Groq's vision LLM to extract text from images, preserving handwriting and formatting.
- **Chunked Processing:** Splits large images into <20MB chunks for efficient and reliable OCR.
- **Sentence-Level Plagiarism Detection:**
  - Compares extracted text between submissions using Jaccard similarity on sentences.
  - Faculty can set a similarity threshold and instantly find the most similar (potentially plagiarized) submissions.
- **Database:** Stores all submissions, extracted text, and results for easy review and audit.

### 3. AI Buddy (Smart Notes Generator & Document Chatbot)

- **Notes Generator:**
  - Upload PDFs, DOCX, or PPTX files (lecture notes, textbooks, slides) or click a picture of the class board or your notes.
  - Extracts, cleans, and summarizes content into high-quality, bullet-point notes.
  - Download notes as a formatted PDF.
- **AI Document Chatbot:**
  - Ask questions about any uploaded document.
  - Uses Groq LLM to answer based only on the document content (contextual RAG-style QA).
  - Supports both text and voice input (speech-to-text).
  - Recent chat always appears at the top for a seamless experience.

## 📼 Demo

https://github.com/user-attachments/assets/f1d1cbb5-23de-451b-a72b-f0c067ba30f6

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit (custom tabs, containers, expander, chat UI)
- **AI/LLM:** Groq (via Agno for text, direct Groq API for vision and chat)
- **PDF/Image Processing:** PyMuPDF4LLM, PyPDF2, pdf2image, PIL
- **Plagiarism:** Custom sentence-level Jaccard similarity
- **Automation:** Selenium (for grade extraction)
- **Speech:** SpeechRecognition (STT)
- **Data Storage:** JSON (for submissions, results)
- **Environment:** Python 3.13, dotenv for secrets

## 📂 Project Structure

```
├── main.py                # Streamlit app entrypoint (navigation)
├── test-assignments/      # Assignments used for testing plagiarism
├── views/
│   ├── page1.py           # Career DHI (grades, github, resume, report)
│   ├── page2.py           # Plagiarism Checker (vision, sentence-level)
│   └── page3.py           # AI Buddy (notes, document chat)
├── utils/
│   ├── cdhi/              # Career DHI utilities (grades, github, resume, report)
│   └── plag/              # Plagiarism utilities (pdf/image, vision OCR)
├── uploads/, stitched/    # Uploaded assignments and stitched images
├── vision_text_db.json    # Plagiarism DB
├── .env                   # API keys (GROQ_API, GROQ_PLAG_API)
├── .gitignore             # Ignores .env, models, uploads, etc.
└── README.md
```

## 🔒 Security & Privacy

- All API keys are loaded from `.env` and never hardcoded.
- Uploaded files and extracted data are stored locally and never sent to third-party servers (except for LLM/vision inference).
- Plagiarism and career data are only accessible to authorized users (faculty/students).

## 🚦 How to Run

1. **Clone the repo:**

   ```bash
   git clone https://github.com/kayozxo/CASP.git
   cd intel
   ```

2. **Create Virtual Environment:**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # for macOS and Linux
   (or)
   myenv\Scripts\activate     # for windows

   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up .env:**

   - Add your Groq API keys:
     ```
     GROQ_API="your-groq-api-key"
     GROQ_PLAG_API="your-groq-plag-key"
     ```

5. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## 👩🏻‍💻 Contributors:

1. [@payalch-25](https://github.com/payalch-25) worked on **Plagiarism Checker**
2. [@abhijitha03](https://github.com/abhijitha03) worked on Study Assistant
