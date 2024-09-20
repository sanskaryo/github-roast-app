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


st.set_page_config(page_title="GitHub Roast App ")
st.header("GitHub Roast App")


github_username = st.text_input("Enter GitHub Username:")


submit = st.button("Roast Me!")


# roast_prompt = """

# Hey there! Roast this GitHub user in a funny, witty, and humorous way,make it short and summarised ,m  but keep it light-hearted. Dive deep into their repos, bio, and activity. Remember, most of them are college students and techies from India, so throw in some techie and student life humor. Make it personal and engaging!

#  Keep it short, sharp, and loaded with techie and college life humor! Dig into their repos, bio, and activity for some real gems. Just remember, most of them are college students or tech nerds from India, . make them into shambles 😜


# """

roast_prompt = """ keep it short and summarised
 Analyze this student/dev's GitHub, summarize their README, bio, and projects in the shortest way possible, and deliver a brutal roast. Tear into their messy code, weak commit history, and unfinished projects, keeping it sharp, snappy, and ruthless—while staying (barely) on the right side of savage
 """

# roast_prompt = """

# Analyze this student/dev's GitHub, summarize their README, bio, and projects in the shortest way possible, and deliver a brutal roast. Tear into their messy code, weak commit history, and unfinished projects, keeping it sharp, snappy, and ruthless—while staying (barely) on the right side of savage , also give slight motivation and constructive feedback at end
# keep it summaridsed nd short - Check out this student/dev's GitHub and give a quick summary of their README, bio, and projects. Then, go full Bollywood villain mode and roast them like you’re the villain in a movie! Call out their messy code like it's a failed Bollywood remake, laugh at their lazy commits like a ‘dialogue baazi,’ and mock their unfinished projects like a flop movie. Keep it short, savage,but with just enough humor 
# """

if submit:
    if github_username:
        try:
           
            github_data = get_github_profile(github_username)
            
           
            response = get_gemini_response(github_data, roast_prompt)
            
          
            st.subheader("The Roast:")
            st.write(response)
        except ValueError as e:
            st.write(str(e))
    else:
        st.write("Please enter a GitHub username.")





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