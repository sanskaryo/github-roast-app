from dotenv import load_dotenv
import base64
import streamlit as st
import os
import requests
import google.generativeai as genai


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(github_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    input_text = f"GitHub User {github_data['name']} has {github_data['public_repos']} repos, {github_data['followers']} followers. Bio: {github_data['bio']}. {prompt}"
    response = model.generate_content([input_text])
    return response.text


def get_github_profile(username):
    github_url = f'https://api.github.com/users/{username}'
    response = requests.get(github_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not fetch GitHub profile. Please check the username.")


st.set_page_config(page_title="GitHub Roast App")
st.header("GitHub Roast App")


github_username = st.text_input("Enter GitHub Username:")


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

            
            response = get_gemini_response(github_data, roast_prompt)
            
           
            st.subheader("The Roast:")
            st.write(response)
        except ValueError as e:
            st.write(str(e))
    else:
        st.write("Please enter a GitHub username.")

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        Made with ❤️ by <a href='https://github.com/sanskaryo' target='_blank'>Sanskar</a><br>
        Just for fun, don't take it seriously.
    </div>
    """,
    unsafe_allow_html=True
)
