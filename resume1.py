import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
import os

st.set_page_config(page_title="Professional Resume Builder", layout="centered")

st.title("Professional Resume Builder")

option = st.radio("Select Option:", ["Generate Resume", "Verify Uploaded Resume"])


# ------------------ RESUME GENERATION ------------------

if option == "Generate Resume":

    st.header("Enter Candidate Details")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

    education = st.text_area("Education Details")
    skills = st.text_area("Technical Skills (comma separated)")
    projects = st.text_area("Projects Description")
    summary = st.text_area("Professional Summary")

    if st.button("Generate Resume"):

        file_path = "Professional_Resume.pdf"
        doc = SimpleDocTemplate(file_path, pagesize=pagesizes.A4)
        elements = []

        styles = getSampleStyleSheet()

        header_style = styles["Heading1"]
        normal_style = styles["Normal"]

        # Name
        elements.append(Paragraph(f"<b>{name}</b>", header_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Contact Table (Rows & Columns Format)
        contact_data = [
            ["Phone:", phone],
            ["Email:", email],
            ["LinkedIn:", linkedin],
            ["GitHub:", github]
        ]

        contact_table = Table(contact_data, colWidths=[1.2 * inch, 4 * inch])
        contact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        elements.append(contact_table)
        elements.append(Spacer(1, 0.3 * inch))

        # Professional Summary
        elements.append(Paragraph("<b>Professional Summary</b>", styles["Heading2"]))
        elements.append(Paragraph(summary, normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Education
        elements.append(Paragraph("<b>Education</b>", styles["Heading2"]))
        elements.append(Paragraph(education, normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Skills
        elements.append(Paragraph("<b>Technical Skills</b>", styles["Heading2"]))
        elements.append(Paragraph(skills, normal_style))
        elements.append(Spacer(1, 0.3 * inch))

        # Projects
        elements.append(Paragraph("<b>Projects</b>", styles["Heading2"]))
        elements.append(Paragraph(projects, normal_style))

        doc.build(elements)

        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Resume",
                data=file,
                file_name="Professional_Resume.pdf",
                mime="application/pdf"
            )

        st.success("Resume Generated Successfully!")


# ------------------ RESUME VERIFICATION ------------------

elif option == "Verify Uploaded Resume":

    st.header("Upload Resume for Basic Verification")

    uploaded_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

    if uploaded_file is not None:

        st.success("Resume Uploaded Successfully!")

        st.write("Basic Verification Result:")

        if uploaded_file.type == "application/pdf":
            st.info("PDF uploaded. Ensure your resume contains clear sections like Summary, Skills, Education, and Projects.")

        elif uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")

            checks = {
                "Summary": "summary" in content.lower(),
                "Skills": "skills" in content.lower(),
                "Education": "education" in content.lower(),
                "Projects": "project" in content.lower()
            }

            for section, present in checks.items():
                if present:
                    st.success(f"{section} section found.")
                else:
                    st.error(f"{section} section missing.")

        st.info("Tip: Use action verbs, measurable achievements, and keep formatting consistent.")
