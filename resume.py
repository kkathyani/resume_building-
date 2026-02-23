import streamlit as st
from google import genai
import PyPDF2
import io

# ---------------- CONFIG ----------------
GEMINI_API_KEY = "AIzaSyAUe2fXmoh1tnLbLruLA6xoAbmdFPkT6-c"  # 🔴 Put your key here

client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="AI Resume Builder & ATS Checker")
st.title("AI Resume Builder & ATS Checker")

# ---------------- OPTION SELECT ----------------
option = st.radio(
    "Choose an option:",
    ["Generate Resume", "Verify Uploaded Resume"]
)

# =========================================================
# ================= RESUME GENERATOR ======================
# =========================================================

if option == "Generate Resume":

    st.subheader("Enter Your Details")

    name = st.text_input("Full Name")
    education = st.text_area("Education")
    skills = st.text_area("Skills (comma separated)")
    experience = st.text_area("Work Experience")
    projects = st.text_area("Projects (Optional)")
    job_description = st.text_area("Target Job Description")

    generate_button = st.button("Generate Resume")

    if generate_button:

        if not name or not education or not skills:
            st.error("Please fill required fields.")
        else:
            with st.spinner("Generating resume..."):
                try:
                    prompt = f"""
Create a professional ATS-friendly resume.

Name: {name}
Education: {education}
Skills: {skills}
Experience: {experience}
Projects: {projects}

Optimize it for this Job Description:
{job_description}

Format with:
- Professional Summary
- Education
- Skills
- Work Experience
- Projects
"""

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    resume_text = response.text

                    st.success("Resume Generated Successfully!")
                    st.text_area("Generated Resume", resume_text, height=400)

                    # Download option
                    resume_bytes = io.BytesIO()
                    resume_bytes.write(resume_text.encode())
                    resume_bytes.seek(0)

                    st.download_button(
                        label="Download Resume (.txt)",
                        data=resume_bytes,
                        file_name="AI_Generated_Resume.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Error: {e}")

# =========================================================
# ================= RESUME VERIFIER =======================
# =========================================================

elif option == "Verify Uploaded Resume":

    job_description = st.text_area("Enter Job Description")
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    analyze_button = st.button("Analyze Resume")

    if analyze_button:

        if uploaded_file is None:
            st.error("Please upload a resume.")
        else:
            with st.spinner("Analyzing resume..."):
                try:
                    reader = PyPDF2.PdfReader(uploaded_file)
                    resume_text = ""

                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            resume_text += text

                    prompt = f"""
You are an ATS system.

Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:
1. Percentage Match
2. Missing Keywords
3. Strengths
4. Weaknesses
"""

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.success("Analysis Complete!")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Error: {e}")
