##################################################
# Brian Lesko
# 2023-10-24
# In this Low code UI, we interact with a large language transformer model (LLM) through an Application Programming Interface (API).
# Practice Coding for concise software development for engineering in the fields of robotics, AI, and automation. 

# When running locally, the file directory is structured as follows:
'''
your-LOCAL-repository/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml # Make sure to gitignore this!
├── your_app.py
├── requirements.txt
├── .gitignore
└── bl.png
'''

##################################################
# About the author: Brian Lesko is a robotics engineer and recent graduate
def about():
    with st.sidebar:

        st.subheader("About")
        st.write('  ') 
        col1, col2, = st.columns([1,5], gap="medium")

        with col1:
            st.image('docs/bl.png')

        with col2:
            st.write(""" 
            Hey it's Brian,
                    
            This is a [Low-Code Python](https://github.com/BrianLesko/Low-Code-Chat/blob/main/low-code-chat.py) UI for ChatGPT.
                     
            It's written with less than 100 lines of code.
                    
            You'll need an OpenAI key to use this app, paste it below.
            """)

        col1, col2, col3, col4, col5, col6 = st.columns([1.1,1,1,1,1,1.5], gap="medium")
        with col2:
            # TWITTER
            "[![X](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/x-logo-blue.svg)](https://twitter.com/BrianJosephLeko)"
        with col3:
            # GITHUB
            "[![Github](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/github-mark-blue.svg)](https://github.com/BrianLesko)"
        with col4:
            # LINKEDIN
            "[![LinkedIn](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/linkedin-icon-blue.svg)](https://www.linkedin.com/in/brianlesko/)"
        with col5:
            # YOUTUBE
            "."
            #"[![LinkedIn](https://raw.githubusercontent.com/BrianLesko/BrianLesko/f7be693250033b9d28c2224c9c1042bb6859bfe9/.socials/svg-335095-blue/yt-logo-blue.svg)](https://www.linkedin.com/in/brianlesko/)" 
        with col6:
            # BLOG Visual Study Code
            "."
            #"[![VSC]()](https://www.visualstudycode.com/)"

##################################################
# Streamlit App

import streamlit as st
import openai

with st.sidebar:
    about()
    st.write('  ') 
    st.markdown("""---""")
    openai_api_key = st.text_input("# OpenAI API Key", key="chatbot_api_key", type="password")
    col1, col2 = st.columns([1,5], gap="medium")
    with col2:
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# use the openai api key from the TOML file in the original directory (also in git ignore) if it is available
if st.secrets["openai_api_key"]:
    openai_api_key = st.secrets["openai_api_key"]

# The app will be used as a template for further chat interfaces for low code UI development
st.title("Low Code Chat Interface") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display all the historical messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Write a message"):

    # Get an open ai key, the company behind the first popular LLM, GPT-3
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)

##################################################
# Related topics: OpenAI Generative Transformers, AI, Streamlit, Chatbot, Python, Low Code, UI, Low code UI, Large Language model