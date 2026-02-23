import streamlit as st
from google import genai
from PyPDF2 import PdfReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable
from reportlab.lib import colors
import tempfile

# ================= ADMIN API KEY =================
GEMINI_API_KEY = "AIzaSyAUe2fXmoh1tnLbLruLA6xoAbmdFPkT6-cz"  # KEEP INSIDE QUOTES

# Initialize client safely
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    st.success("API Connected Successfully")
except Exception as e:
    st.error(f"API Initialization Failed: {e}")
    st.stop()

# ================= STREAMLIT UI =================
st.set_page_config(page_title="Professional Resume Builder")
st.title("Professional Resume Builder")

option = st.radio(
    "Choose an option:",
    ["Generate Resume", "Verify Uploaded Resume"]
)

# ================= AI FUNCTION =================
def generate_content(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error from Gemini API:\n{e}"

# ================= PDF CREATION =================
def create_pdf(name, email, phone, linkedin, github, content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>{name}</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    contact = [[email, phone], [linkedin, github]]
    table = Table(contact, colWidths=[3*inch, 3*inch])
    elements.append(table)
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    elements.append(Spacer(1, 12))

    for line in content.split("\n"):
        if line.strip():
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 6))

    doc.build(elements)
    return temp_file.name


# ================= GENERATE RESUME =================
if option == "Generate Resume":

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")
    details = st.text_area("Explain what you learned, projects, skills etc.")

    if st.button("Generate Resume"):

        if details.strip() == "":
            st.warning("Please enter your details.")
        else:
            with st.spinner("Generating..."):
                prompt = f"""
                Create a professional resume.
                Improve wording naturally.
                Structure into:
                Summary
                Projects
                Skills
                Certifications

                Candidate details:
                {details}
                """

                result = generate_content(prompt)

                if result.startswith("Error"):
                    st.error(result)
                else:
                    pdf_path = create_pdf(name, email, phone, linkedin, github, result)

                    st.success("Resume Generated Successfully!")

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download Resume PDF",
                            data=f,
                            file_name="Professional_Resume.pdf",
                            mime="application/pdf"
                        )

# ================= VERIFY RESUME =================
elif option == "Verify Uploaded Resume":

    uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

    if uploaded_file is not None:

        try:
            reader = PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text()

            st.info("Resume Extracted Successfully")

            if st.button("Verify Resume"):

                with st.spinner("Analyzing..."):

                    prompt = f"""
                    Review this resume.
                    Suggest improvements in:
                    - Summary
                    - Skills
                    - Projects
                    - Formatting

                    Resume:
                    {resume_text}
                    """

                    result = generate_content(prompt)

                    if result.startswith("Error"):
                        st.error(result)
                    else:
                        st.subheader("Resume Review")
                        st.write(result)

        except Exception as e:
            st.error(f"PDF Reading Error: {e}")