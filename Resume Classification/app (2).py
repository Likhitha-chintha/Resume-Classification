import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import re

# Predefined list of technical skills (for example purposes)
technical_skills = ["Python", "Java", "JavaScript", "React", "SQL", "C#", "C++", "Ruby", "Node.js",
    "Django", "Flask", "HTML", "CSS", "Machine Learning", "Data Science", "Deep Learning",
    "TensorFlow", "Keras", "Pandas", "NumPy", "AWS", "Azure", "Git", "Linux", "Docker", "Kubernetes"]

# Helper function to extract text from .docx files
def extract_text_from_docx(file):
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return ""

# Helper function to extract text from PDF files
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    except Exception as e:
        return ""

# Helper function to extract experience from the resume text
def extract_experience_from_text(text):
    text = text.lower()
    match = re.search(r'\b(\d+(\.\d+)?)\s*(?:years?|yrs?)\b', text)
    if match:
        return float(match.group(1))  # Return the experience as a float
    return 0.0

# Helper function to extract skills from the resume text
def extract_skills_from_text(text, skills_list):
    skills_found = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills_found.append(skill)
    return skills_found

# Streamlit App Configuration
st.set_page_config(page_title="Resume Information Extractor", layout="wide")

st.title("Resume Information Extraction")

# Upload file (single .docx or .pdf file)
uploaded_file = st.file_uploader("Upload a .docx or .pdf file containing a resume 📂", type=["docx", "pdf"])

if uploaded_file:
    try:
        with st.spinner("Processing uploaded file... 🧑‍💻"):
            # Determine file type and extract text
            if uploaded_file.name.endswith('.docx'):
                text = extract_text_from_docx(uploaded_file)
            elif uploaded_file.name.endswith('.pdf'):
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = ""

            # Extract and display the details if text is found
            if text.strip():
                name = uploaded_file.name.split('.')[0]  # Assume name is in the filename (without extension)
                experience = extract_experience_from_text(text)
                skills = extract_skills_from_text(text, technical_skills)

                # Display extracted data
                st.write(f"### {name} 👨‍💻")
                st.write(f"**Experience**: {experience} years 📅")
                st.write(f"**Skills**: {', '.join(skills) if skills else 'No skills found'} 🛠️")
            else:
                st.warning("The uploaded file contains no extractable text.")

    except Exception as e:
        st.error(f"An error occurred: {e} ❌")
