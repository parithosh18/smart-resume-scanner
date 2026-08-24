import os
import streamlit as st
from google import genai
from pypdf import PdfReader


# =========================
# GEMINI API
# =========================

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing.")
    st.stop()

client = genai.Client(api_key=api_key)


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Smart Resume Scanner",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Smart Resume Scanner")
st.write("Upload your resume and compare it with a job description using AI.")


# =========================
# RESUME UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)


# =========================
# JOB DESCRIPTION
# =========================

job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Paste the complete job description here..."
)


# =========================
# ANALYZE
# =========================

if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter the job description.")

    else:

        with st.spinner("Analyzing your resume..."):

            # Read PDF
            reader = PdfReader(uploaded_file)

            resume_text = ""

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    resume_text += text + "\n"

            # Prompt
            prompt = f"""
You are a professional resume screening assistant.

Compare the resume with the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return the following:

1. Match Score out of 10
2. Extracted Skills
3. Missing Skills
4. Strengths
5. Weaknesses
6. Shortlist Recommendation (Yes/No)
7. Justification
8. Skills the candidate should learn to improve their chances
"""

            # Gemini
            chat = client.chats.create(
                model="gemini-3.6-flash"
            )

            response = chat.send_message(prompt)

        # Display result
        st.success("Analysis completed!")

        st.markdown("## 📊 Resume Analysis")

        st.markdown(response.text)

        st.divider()

        st.info(
            "💡 Tip: Use the missing skills identified above to improve "
            "your resume and prepare for the job."
        )