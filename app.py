import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import base64
import docx2txt
import time


load_dotenv()  # Load environment variables

# Function to add a custom background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_image});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function with your image file
add_bg_from_local('steve-johnson-QoJuScaZjkA-unsplash.jpg')  # Use a high-quality background image

# Read the CSS file for additional styling
with open("G:\VS_Code\ATS_SCORE_CHECKER_PROJECT\style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit app layout with a title and company name
st.markdown("<div class='title'> <span> HUBNEX LABS - SCORE MY RESUME </span> </div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>How good is your resume? </div>", unsafe_allow_html=True)

st.markdown("<div class='subtitle'>Find out instantly. Upload your resume and our free resume scanner will evaluate it against key criteria hiring managers and applicant tracking systems (ATS) look for. Get actionable feedback on how to improve your resume's success rate.</div>", unsafe_allow_html=True)

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

def extract_text_from_docx_file(uploaded_file):
    return docx2txt.process(uploaded_file)

# Prompt Template
st.header("ATS Tracking System")
input_text = st.text_area("Paste the Job Description: ", key="input", help="Paste the job description here to match with your resume.")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"], help="Upload your resume in PDF or DOCX format.")

# Select the analysis type (Detailed Review, ATS Match Evaluation, etc.)
analysis_type = st.radio(
    "Select Analysis Type",
    ("Detailed Review", "ATS Match Evaluation", "Skill Matching", "Experience Relevance", "Keyword Analysis", "Tone and Language", "Grammar and Formatting Check"),
    help="Choose the type of analysis you want to perform.",
    key="analysis"
)

# Function to show progress while processing
def show_progress_bar():
    with st.spinner('Processing...'):
        time.sleep(3)  # Simulate processing delay

submit = st.button("Evaluate Resume", key="submit")

# Additional Prompt Templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """
Please compare the skills listed in the resume to the skills required in the job description. Highlight any missing skills.
"""

input_prompt4 = """
Analyze the candidate's experience as mentioned in the resume in relation to the job description. Point out the relevance or mismatch.
"""

input_prompt5 = """
Identify keywords that are missing in the resume but are mentioned in the job description. Provide an analysis of these missing keywords.
"""

input_prompt6 = """
Evaluate the tone and language used in the resume and check its alignment with the tone and language required in the job description.
"""

input_prompt7 = """
Review the grammar and formatting of the resume. Point out any errors or areas of improvement to make the resume more professional.
"""

# Interactivity with buttons and feedback
if submit:
    if uploaded_file is not None:
        # Show a progress bar while file is being processed
        show_progress_bar()
        
        # Extract text based on the file type
        if uploaded_file.type == "application/pdf":
            resume_text = input_pdf_text(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)

        # Determine the appropriate prompt based on the analysis type
        if analysis_type == "Detailed Review":
            response = get_gemini_response(input_prompt1)
        elif analysis_type == "ATS Match Evaluation":
            response = get_gemini_response(input_prompt2)
        elif analysis_type == "Skill Matching":
            response = get_gemini_response(input_prompt3)
        elif analysis_type == "Experience Relevance":
            response = get_gemini_response(input_prompt4)
        elif analysis_type == "Keyword Analysis":
            response = get_gemini_response(input_prompt5)
        elif analysis_type == "Tone and Language":
            response = get_gemini_response(input_prompt6)
        elif analysis_type == "Grammar and Formatting Check":
            response = get_gemini_response(input_prompt7)

        # Show results in a collapsible section for a clean UI
        with st.expander("Show Evaluation Results"):
            st.subheader("The Response is: ")
            st.write(response)

        # Adding a success message
        st.success("Resume successfully analyzed! 🎉")
    else:
        st.warning("Please upload a resume file.")

# Custom Footer with additional styling
footer = """
<style>
a:link, a:visited{
    color: yellow;
    background-color: transparent;
    text-decoration: underline;
}

a:hover, a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #333;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    font-family: Arial, sans-serif;
}

.footer a {
    color: #ffcc00;
    font-weight: bold;
}

.footer a:hover {
    color: #ff6600;
}
</style>
<div class="footer">
    <p>Powered by VISHWAJIT SINGH | <a href="https://www.hubnex.in/" target="_blank">HUBNEX LABS</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
