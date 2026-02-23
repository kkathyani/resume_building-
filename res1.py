import streamlit as st
from google import genai
import PyPDF2
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

GEMINI_API_KEY = "AIzaSyDj7iKIk8TBmPurhjaUeIYBfKdp_tHIPws"
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Resume Builder")
st.title("Resume Builder")

option = st.radio("Select Option:", ["Generate Resume", "Verify Uploaded Resume"])

# =========================================================
# ================= GENERATE RESUME =======================
# =========================================================

if option == "Generate Resume":

    st.header("Enter Candidate Details")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")

    objective = st.text_area("Career Objective")
    education = st.text_area("Academic Details")
    technical_skills = st.text_area("Technical Skills")
    personal_skills = st.text_area("Personal Skills")
    projects = st.text_area("Projects / Experience")
    achievements = st.text_area("Achievements")
    personal_details = st.text_area("Personal Details")

    if st.button("Generate Resume"):

        with st.spinner("Preparing Resume..."):

            prompt = f"""
Rewrite and polish the content below.
Keep traditional Indian resume format.
Do NOT exaggerate.
Do NOT mention AI.
Keep headings in CAPS.
Improve grammar only.

Format exactly like this:

RESUME

{name}
{phone} | {email}

CAREER OBJECTIVE:
<content>

ACADEMIC PROFILE:
<content>

TECHNICAL SKILLS:
<content>

PERSONAL SKILLS:
<content>

PROJECTS / EXPERIENCE:
<content>

ACHIEVEMENTS:
<content>

PERSONAL DETAILS:
<content>

User Content:
Objective: {objective}
Education: {education}
Technical Skills: {technical_skills}
Personal Skills: {personal_skills}
Projects: {projects}
Achievements: {achievements}
Personal Details: {personal_details}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            resume_text = response.text

            st.text_area("Generated Resume", resume_text, height=600)

            # ================= PDF GENERATION =================
            file_path = "Professional_Resume.pdf"
            doc = SimpleDocTemplate(file_path, pagesize=pagesizes.A4)
            elements = []
            styles = getSampleStyleSheet()

            for line in resume_text.split("\n"):
                elements.append(Paragraph(line, styles["Normal"]))
                elements.append(Spacer(1, 0.2 * inch))

            doc.build(elements)

            with open(file_path, "rb") as pdf_file:
                st.download_button(
                    label="Download Resume (PDF)",
                    data=pdf_file,
                    file_name="Professional_Resume.pdf",
                    mime="application/pdf"
                )

# =========================================================
# ================= VERIFY RESUME =========================
# =========================================================

elif option == "Verify Uploaded Resume":

    st.header("Upload Resume for ATS Check")

    job_description = st.text_area("Job Description")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if st.button("Analyze Resume"):

        if uploaded_file is None:
            st.error("Please upload resume.")
        else:
            reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

            prompt = f"""
Analyze the resume against job description.

Give:
1. Percentage Match
2. Missing Skills
3. Suggestions to Improve
Keep response simple.

Resume:
{resume_text}

Job Description:
{job_description}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.write(response.text)
            