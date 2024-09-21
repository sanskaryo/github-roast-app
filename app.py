from dotenv import load_dotenv
import base64
import streamlit as st
import os
import requests
import google.generativeai as genai
import PyPDF2
from docx import Document

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    input_text_with_prompt = f"{input_text}. {prompt}"
    response = model.generate_content([input_text_with_prompt])
    return response.text

def get_github_profile(username):
    github_url = f'https://api.github.com/users/{username}'
    response = requests.get(github_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not fetch GitHub profile. Please check the username.")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

st.set_page_config(page_title="GitHub & Resume Roast App")
st.header("Welcome to the Roast App!")


github_username = st.text_input("Enter GitHub Username:")

# Roast Level
roast_level = st.radio("Choose your roast level:", ('Easy', 'Medium', 'Heavy Driver'))


easy_roast_prompt = """ 
Summarize this GitHub user's README, bio, and projects with light-hearted humor. Give them some gentle feedback, a few funny jabs, and wrap it up with motivation. Keep it witty and encouraging, like a coding buddy who teases but believes in them! , Keep it witty and encouraging, like a coding buddy who teases but believes in them! dont make it very long
"""

medium_roast_prompt = """
Summarize this GitHub user's README, bio, and projects. Add some harsh, sarcastic commentary on their lazy commits and unfinished projects. Don't go too soft, but offer some constructive feedback so they don’t cry… yet. dont make it very long , funny add emojis
"""

harsh_roast_prompt = """
Rip into this GitHub user's README, bio, and projects like you're out for revenge! Mock their spaghetti code, point out their non-existent commit history, and roast every unfinished project like a Bollywood villain burning their repo alive. No kindness, no mercy—just pure, brutal honesty.
"""


submit = st.button("Roast Me!")

if submit:
    if github_username:
        try:
          
            github_data = get_github_profile(github_username)
            
          
            if roast_level == 'Easy':
                roast_prompt = easy_roast_prompt
            elif roast_level == 'Medium':
                roast_prompt = medium_roast_prompt
            elif roast_level == 'Heavy Driver':
                roast_prompt = harsh_roast_prompt
            else:
                roast_prompt = easy_roast_prompt
            
            response = get_gemini_response(resume_text, roast_prompt)
            st.subheader("The Roast:")
            st.markdown(f'<div class="roast-output">{response}</div>', unsafe_allow_html=True)


# Footer
st.markdown(
    """
    <style>
/* General Styling */
body {
    background-color: #fef4f4;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3, h4 {
    color: #ff6347;
    text-align: center;
    font-weight: bold;
}

h2 {
    margin-bottom: 20px;
}

/* Sidebar Styling */
.stSidebar {
    background-color: #ffecb3;
    padding: 10px;
}

.stSidebar h2 {
    color: #333;
}

.stSidebar .stRadio > div > label {
    font-size: 16px;
    padding: 10px;
    background-color: #f0f0f0;
    margin-bottom: 5px;
    border-radius: 5px;
    border: 1px solid #ddd;
    transition: all 0.3s ease;
}



/* Buttons */
button {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    transition-duration: 0.4s;
    cursor: pointer;
    border-radius: 12px;
}

/* Button hover effects */
button:hover {
    background-color: white;
    color: black;
    border: 2px solid #4CAF50;
}

/* Input fields styling */
input[type="text"], input[type="file"] {
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 20px;
    width: 100%;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

input[type="file"] {
    background-color: #f0f0f0;
}

/* Roast output styling */
.roast-output {
    background-color: #ffe6e6;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #ff4d4d;
    font-size: 18px;
    line-height: 1.5;
}

/* Footer Styling */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: black;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}

.footer a {
    color: #ff6347;
    text-decoration: none;
}

.footer a:hover {
    color: #ffcc00;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    h1, h2 {
        font-size: 18px;
    }

    .stButton, .stTextInput {
        width: 100%;
    }
}

/* Loading animation */
.loading-animation {
    border: 16px solid #f3f3f3;
    border-top: 16px solid #3498db;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    animation: spin 2s linear infinite;
}

keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

</style>

<div class="footer">
    Made with ❤️ by <a href='https://github.com/sanskaryo' target='_blank'>Sanskar</a><br>
    Just for fun, don't cry after the roast 😄.
</div>
""",
unsafe_allow_html=True
)
